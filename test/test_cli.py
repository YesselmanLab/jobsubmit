import yaml
from jobsubmit.cli import (
    fill_in_missing_default_dict_values,
    fill_in_missing_default_params,
)


def test_fill_in_missing_default_dict_values():
    # Test case 1: Default dictionary is empty
    default = {}
    current = {"a": 1, "b": 2}
    expected = {"a": 1, "b": 2}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 2: Default dictionary has missing values
    default = {"a": 1, "b": 2, "c": 3}
    current = {"a": 1}
    expected = {"a": 1, "b": 2, "c": 3}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 3: Default dictionary has nested dictionaries
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 4: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 5: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 6: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 7: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 8: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 9: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 10: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 11: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 12: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 13: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 14: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 15: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 16: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 17: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 18: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 19: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected

    # Test case 20: Default dictionary has nested dictionaries with missing values
    default = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
    current = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    expected = {"a": {"x": 1, "y": 2}, "b": {"z": 3}, "c": {"w": 4}}
    assert fill_in_missing_default_dict_values(default, current) == expected


def test_fill_in_missing_default_params():
    params = {
        "custom_args": {"filename": "*.txt", "range_arg": "1-3,5,7-10"},
    }
    default_params = {
        "job_dir": "jobs",
        "output_dir": "outputs",
        "error_dir": "errors",
        "tasks_per_job": 1,
        "repeat": 1,
        "slurm_args": {
            "job_name": "test",
            "time": "01:00:00",
            "nodes": 1,
            "ntasks_per_node": 1,
            "mem": "2GB",
        },
    }
    current = fill_in_missing_default_params(params)
    assert current["job_dir"] == default_params["job_dir"]
    assert current["output_dir"] == default_params["output_dir"]
    assert current["error_dir"] == default_params["error_dir"]
    assert current["tasks_per_job"] == default_params["tasks_per_job"]
    assert current["repeat"] == default_params["repeat"]
    assert current["slurm_args"]["job_name"] == default_params["slurm_args"]["job_name"]
    assert current["slurm_args"]["time"] == default_params["slurm_args"]["time"]
    assert current["slurm_args"]["nodes"] == default_params["slurm_args"]["nodes"]
    assert (
        current["slurm_args"]["ntasks_per_node"]
        == default_params["slurm_args"]["ntasks_per_node"]
    )
