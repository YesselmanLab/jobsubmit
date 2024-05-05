import re
import glob
import click
import yaml
import itertools
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Union

from jobsubmit.logger import get_logger, setup_applevel_logger
from jobsubmit.settings import get_lib_path

log = get_logger("cli")


@dataclass
class SlurmJobConfig:
    job_name: str = "test"
    time: str = "01:00:00"
    nodes: int = 1
    ntasks_per_node: int = 1
    mem: str = "2GB"


def generate_slurm_header(
    config: SlurmJobConfig, job_num=-1, output_dir="", error_dir=""
):
    path = get_lib_path() + "/jobsubmit/resources/job_header.txt"
    f = open(path)
    header = f.read()
    f.close()
    args = asdict(config)
    if job_num == -1:
        name = args["job_name"]
    else:
        name = args["job_name"] + "-" + str(job_num)
    if output_dir != "" and output_dir[-1] != "/":
        output_dir += "/"
    if error_dir != "" and error_dir[-1] != "/":
        error_dir += "/"
    args["output"] = output_dir + f"{name}.out"
    args["error"] = error_dir + f"{name}.err"
    args["job_name"] = f"{name}"

    header = re.sub(r"\$(\w+)", lambda m: str(args.get(m.group(1), "")), header)
    return header


def create_slurm_script(
    template_path: str, config: SlurmJobConfig, custom_args: Dict[str, Union[str, int]]
):
    """
    Create a SLURM script from the given template and configuration.
    """
    with open(template_path, "r") as template_file:
        template = template_file.read()

    combined_args = {**asdict(config), **custom_args}

    # Substitute placeholders
    script = re.sub(
        r"\$(\w+)", lambda m: str(combined_args.get(m.group(1), "")), template
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
        else:
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


@click.command()
@click.argument("template", type=click.Path(exists=True))
@click.argument("yaml_config", type=click.Path(exists=True))
def main(template, yaml_config):
    """
    Generate multiple SLURM job scripts.
    """
    setup_applevel_logger()
    log.info("Generating SLURM job scripts")
    log.info(f"Template: {template}")
    log.info(f"YAML config: {yaml_config}")
    with open(yaml_config, "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)
    exit()
    config = SlurmJobConfig(**config_data["slurm_args"])
    log.info(f"Slurm job parameters: {config}")
    job_count = 1
    for custom_args in generate_custom_args(config):
        for _ in range(config.repeat):
            config.job_name = f"{config_data['job_name']}_{job_count}"
            script_content = create_slurm_script(template, config, custom_args)
            script_filename = f"{config.job_name}.slurm"
            write_slurm_script(script_filename, script_content)
            click.echo(f"SLURM script written to {script_filename}")
            job_count += 1


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
