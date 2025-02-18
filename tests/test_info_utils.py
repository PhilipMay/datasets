import pytest

import datasets.config
from datasets.utils.info_utils import is_small_dataset


@pytest.fixture(params=[None, 0, 100 * 2 ** 20, 900 * 2 ** 20])
def env_max_in_memory_dataset_size(request, monkeypatch):
    if request.param:
        monkeypatch.setenv("HF_MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES", request.param)


@pytest.mark.parametrize("dataset_size", [None, 400 * 2 ** 20, 600 * 2 ** 20])
@pytest.mark.parametrize("config_max_in_memory_dataset_size", ["default", 0, 100 * 2 ** 20, 900 * 2 ** 20])
def test_is_small_dataset(
    dataset_size, config_max_in_memory_dataset_size, env_max_in_memory_dataset_size, monkeypatch
):
    if config_max_in_memory_dataset_size != "default":
        monkeypatch.setattr(
            datasets.config, "HF_MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES", config_max_in_memory_dataset_size
        )

    max_in_memory_dataset_size = datasets.config.HF_MAX_IN_MEMORY_DATASET_SIZE_IN_BYTES
    if config_max_in_memory_dataset_size == "default":
        if env_max_in_memory_dataset_size:
            assert max_in_memory_dataset_size == env_max_in_memory_dataset_size
        else:
            assert max_in_memory_dataset_size == 250 * 2 ** 20
    else:
        assert max_in_memory_dataset_size == config_max_in_memory_dataset_size
    if dataset_size and max_in_memory_dataset_size:
        expected = dataset_size < max_in_memory_dataset_size
    else:
        expected = False
    result = is_small_dataset(dataset_size)
    assert result == expected
