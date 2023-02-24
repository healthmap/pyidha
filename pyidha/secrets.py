import os

import hvac


def get_vault_secrets(path):
    """Retrieves a dictionary of secrets from Hashicorp Vault.

    Requires VAULT_URL and VAULT_TOKEN as environment variables.

    Parameters
    __________
    path : str
        Path for Vault secrets, not including base URL.

    Returns
    _______
    secrets : dict
        Secrets retrieved from path.

    """
    vault_url = os.environ.get("VAULT_URL")
    vault_token = os.environ.get("VAULT_TOKEN")
    if not all([vault_url, vault_token]):
        missing_variables = []
        if not vault_url:
            missing_variables.append("VAULT_URL")
        if not vault_token:
            missing_variables.append("VAULT_TOKEN")
        missing_variables = str(missing_variables)
        raise EnvironmentError(
            f"Missing required environment variables: {missing_variables}"
        )
    client = hvac.Client(url=vault_url, token=os.environ.get("VAULT_TOKEN"))
    response = client.secrets.kv.v2.read_secret_version(path=path, mount_point="kv")
    secrets = response["data"]["data"]
    return secrets


def set_env_variables(secrets):
    """Sets environment variables from dictionary of secrets.

    Parameters
    __________
    secrets : dict
        Dictionary of secrets to be set as environment variables.

    Returns
    _______
    boolean
        True if at least one secret has been set, otherwise False.

    """
    if not secrets:
        return False
    os.environ.update(secrets)
    return True


def load_secrets(path, to_dict=True, to_env=False):
    """Loads secrets from Hashicorp Vault.

    Requires VAULT_URL and VAULT_TOKEN as environment variables.

    At least one of `to_dict` or `to_env` must be set to True, or
    this function will do nothing.

    Parameters
    __________
    path : str
        Path for Vault secrets, not including base URL.
    to_dict : boolean
        Returns a dictionary of secrets if True. True by default.
    to_env : boolean
        Sets all secrets as environment variables if True. False by default.

    Returns
    _______
    dict or None
        Dictionary containing secrets if `to_dict` is True, otherwise None.

    """
    if not any((to_dict, to_env)):
        raise ValueError("At least one of `to_dict` or `to_env` must be True.")
    secrets = get_vault_secrets(path)
    if to_env:
        result = set_env_variables(secrets)
        print(f"Secrets loaded into environment?: {result}")
    if to_dict:
        return secrets
