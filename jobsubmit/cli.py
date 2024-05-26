import re
import os
import glob
import click
import yaml
import itertools
import pandas as pd
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Union

from jobsubmit.logger import get_logger, setup_applevel_logger
from jobsubmit.settings import get_lib_path

log = get_logger("cli")


@dataclass
class SlurmJobConfig:
    """
    Represents the configuration for a Slurm job.

    Attributes:
        job_name (str): The name of the job.
        time (str): The maximum time for the job to run.
        nodes (int): The number of nodes to allocate for the job.
        ntasks_per_node (int): The number of tasks to run per node.
        mem (str): The amount of memory to allocate for the job.
    """

    job_name: str = "test"
    time: str = "01:00:00"
    nodes: int = 1
    ntasks_per_node: int = 1
    mem: str = "2GB"


def generate_slurm_header(config: SlurmJobConfig, job_dir="", job_num=-1):
    """
    Generate the SLURM header for a job submission.

    Args:
        config (SlurmJobConfig): The configuration object for the SLURM job.
        job_dir (str, optional): The directory where the job output files will be stored. Defaults to "".
        job_num (int, optional): The job number. Defaults to -1.

    Returns:
        str: The generated SLURM header as a string.
    """
    path = get_lib_path() + "/jobsubmit/resources/job_header.txt"
    f = open(path)
    header = f.read()
    f.close()
    args = asdict(config)
    if job_num == -1:
        name = args["job_name"]
    else:
        name = args["job_name"] + "-" + str(job_num)
    if not job_dir == "" and not job_dir.endswith("/"):
        job_dir = job_dir + "/"
    args["output"] = job_dir + f"{name}.out"
    args["error"] = job_dir + f"{name}.err"
    args["job_name"] = f"{name}"

    header = (
        re.sub(r"\$(\w+)", lambda m: str(args.get(m.group(1), "")), header) + "\n\n"
    )
    return header


def generate_task_str(template_str, custom_args):
    """
    Create a SLURM script from the given template and configuration.
    """
    # Substitute placeholders
    script = re.sub(
        r"\$(\w+)", lambda m: str(custom_args.get(m.group(1), "")), template_str
    )
    return script


def write_slurm_script(filename, script_content):
    """
    Write the SLURM script content to a file.
    """
    with open(filename, "w") as f:
        f.write(script_content)


def parse_custom_arg(arg: str) -> List[Union[str, int]]:
    """
    Parse a custom argument that can be a list of strings, a wildcard pattern,
    or a range.
    """
    if "*" in arg or "?" in arg or "[" in arg:
        return glob.glob(arg)
    elif "-" in arg or "," in arg:
        # Process a range or a comma-separated list of ranges/numbers
        ranges = [range_item.strip() for range_item in arg.split(",")]
        numbers = set()
        for r in ranges:
            if "-" in r:
                start, end = map(int, r.split("-"))
                numbers.update(range(start, end + 1))
            else:
                numbers.add(int(r))
        return sorted(numbers)
    else:
        return [arg]


def generate_custom_args(custom_args):
    """
    Generate custom arguments based on ranges or lists in the custom_args field.
    """
    keys = list(custom_args.keys())
    values = [parse_custom_arg(str(v)) for v in custom_args.values()]
    for item in itertools.product(*values):
        yield dict(zip(keys, item))


def fill_in_missing_default_dict_values(default, current):
    """
    Recursively fill in missing values in the current dictionary with values
    from the default dictionary.

    Parameters:
    - default (dict): The default dictionary containing the values to fill in.
    - current (dict): The current dictionary to be updated with missing values.

    Returns:
    - dict: The updated current dictionary with missing values filled in.
    """
    for key, value in default.items():
        if isinstance(value, dict):
            # If the value is a dictionary, recurse into it
            node = current.setdefault(key, {})
            fill_in_missing_default_dict_values(value, node)
        elif key not in current:
            # Set value if key is missing
            current[key] = value
    return current


def fill_in_missing_default_params(config_data):
    """
    Fills in missing default parameters in the given config_data dictionary.

    Parameters:
    - config_data (dict): The dictionary containing the configuration data.

    Returns:
    - dict: The updated config_data dictionary with missing default parameters filled in.
    """
    path = get_lib_path() + "/jobsubmit/resources/default.yml"
    with open(path, "r") as yaml_file:
        default_data = yaml.safe_load(yaml_file)
    fill_in_missing_default_dict_values(default_data, config_data)
    return config_data


def chunk_list(input_list, chunk_size):
    """
    Breaks a list into chunks of a given size.

    Parameters:
    - input_list (list): The list to be chunked.
    - chunk_size (int): The size of each chunk.

    Returns:
    - list of lists: A list where each element is a chunk of the input list.
    """
    return [
        input_list[i : i + chunk_size] for i in range(0, len(input_list), chunk_size)
    ]


@click.command()
@click.argument("template", type=click.Path(exists=True))
@click.argument("yaml_config", type=click.Path(exists=True))
@click.option("--extra-header-cmds", type=click.Path(exists=True), default=None)
@click.option("--dataframe", default=None, type=click.Path(exists=True))
def main(template, yaml_config, dataframe=None, extra_header_cmds=None):
    """
    Generate multiple SLURM job scripts.
    """
    setup_applevel_logger()
    log.info("Generating SLURM job scripts")
    log.info(f"Template: {template}")
    log.info(f"YAML config: {yaml_config}")
    with open(yaml_config, "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)
    with open(template, "r") as template_file:
        template_str = template_file.read()
    header_cmds = ""
    if extra_header_cmds:
        with open(extra_header_cmds, "r") as f:
            header_cmds = f.read()
    config_data = fill_in_missing_default_params(config_data)
    slurm_config = SlurmJobConfig(**config_data["slurm_args"])
    log.info(f"Slurm job parameters: {slurm_config}")
    if "custom_args" not in config_data:
        config_data["custom_args"] = {}
    custom_args = config_data["custom_args"]
    if dataframe and len(custom_args) > 0:
        raise ValueError("Cannot use both custom_args and dataframe")
    if dataframe:
        log.info(f"Reading custom arguments from dataframe: {dataframe}")
        df = pd.read_csv(dataframe)
        all_custom_args = df.to_dict(orient="records")
    else:
        log.info("Generating custom arguments")
        all_custom_args = list(generate_custom_args(custom_args))
    all_custom_args = all_custom_args * config_data["repeat"]
    os.makedirs(config_data["run_dir"], exist_ok=True)
    arg_chunks = chunk_list(all_custom_args, config_data["tasks_per_job"])
    f = open("README_SUBMIT", "w")
    for i, custom_args_chunk in enumerate(arg_chunks):
        job_dir = os.path.abspath(config_data["run_dir"]) + "/" + str(i)
        os.makedirs(job_dir, exist_ok=True)
        script_content = generate_slurm_header(slurm_config, job_dir, i) + "\n\n"
        if header_cmds != "":
            script_content += header_cmds + "\n\n"
        script_content += f"cd {job_dir}\n\n"
        for chunk in custom_args_chunk:
            script_content += generate_task_str(template_str, chunk) + "\n\n"
        job_file = slurm_config.job_name + "-" + str(i) + ".sh"
        write_slurm_script(job_dir + "/" + job_file, script_content)
        f.write(f"sbatch {job_dir}/{job_file}\n")
    f.close()


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
