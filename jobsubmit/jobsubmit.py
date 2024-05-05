import re
import yaml
import click
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class SlurmJobConfig:
    job_name: str
    output: str = "slurm-%j.out"
    error: str = "slurm-%j.err"
    time: str = "01:00:00"
    partition: str = "general"
    nodes: int = 1
    ntasks_per_node: int = 1
    mem: str = "4GB"
    custom_args: Dict[str, str] = None


def create_slurm_script(template_path: str, config: SlurmJobConfig):
    """
    Create a SLURM script from the given template and configuration.
    """
    with open(template_path, "r") as template_file:
        template = template_file.read()

    combined_args = {**asdict(config), **(config.custom_args or {})}

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


@click.command()
@click.argument("template", type=click.Path(exists=True))
@click.argument("yaml_config", type=click.Path(exists=True))
def main(template, yaml_config):
    """
    Generate SLURM job scripts.
    """
    with open(yaml_config, "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    config = SlurmJobConfig(**config_data)

    script_content = create_slurm_script(template, config)
    script_filename = f"{config.job_name}.slurm"
    write_slurm_script(script_filename, script_content)

    click.echo(f"SLURM script written to {script_filename}")


if __name__ == "__main__":
    main()
