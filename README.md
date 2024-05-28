# jobsubmit

[![PYPI status]( https://badge.fury.io/py/jobsubmit.png)](http://badge.fury.io/py/jobsubmit)[![Build status](https://travis-ci.com/jyesselm/jobsubmit.png?branch=main)](https://travis-ci.com/jyesselm/jobsubmit)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An automated way to multieplex commandssdss for job submission

## Install

To install rna_draw 

```shell
python -m pip install git+https://github.com/jyesselm/jobsubmit
```


## How to use 

```shell
jobsubmit --help

```


Takes a config file (config.yml)

```yaml
run_dir: "runs"
tasks_per_job:  1
repeat: 1
slurm_args:
  job_name: "test"
  time: "01:00:00"
  nodes: 1
  ntasks_per_node: 1
  mem: "2GB"
custom_args:
  filename: "*.txt"
  range_arg: "1-3,5,7-10"
```

Takes a template file (template.txt)

```shell
export VAR=/test
echo $VAR
echo "Processing filename: {filename}"
echo "Processing range argument: {range_arg}"
```
Runs as 

```shell
jobsubmit template.txt config.yaml
```