import os
import pytest

from pyidha.secrets import get_vault_secrets, set_env_variables, load_secrets


def test_get_vault_secrets_requires_credentials():
    del os.environ["VAULT_TOKEN"]
    with pytest.raises(EnvironmentError):
        get_vault_secrets("test/path")


def test_set_env_variables_returns_false_with_empty_dict():
    test_secrets = {}
    assert not set_env_variables(test_secrets)


def test_set_env_variables_returns_true_with_one_secret():
    test_secrets = {"SECRET_CODE": "xmarksthespot"}
    assert set_env_variables(test_secrets)


def test_set_env_variables_can_retrieve_set_variables():
    test_secrets = {"SECRET_CODE": "rosebud"}
    set_env_variables(test_secrets)
    assert os.environ.get("SECRET_CODE") == "rosebud"


def test_load_secrets_requires_credentials():
    if "VAULT_URL" in os.environ.keys():
        del os.environ["VAULT_URL"]
    with pytest.raises(EnvironmentError):
        load_secrets("test/path")


def test_load_secrets_requires_at_least_one_destination():
    with pytest.raises(ValueError):
        load_secrets("test/path", to_dict=False, to_env=False)
