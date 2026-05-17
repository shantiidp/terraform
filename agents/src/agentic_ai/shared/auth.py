from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

_credential: DefaultAzureCredential | None = None


def get_credential() -> DefaultAzureCredential:
    global _credential
    if _credential is None:
        _credential = DefaultAzureCredential()
    return _credential


def get_secret(vault_uri: str, secret_name: str) -> str:
    credential = get_credential()
    client = SecretClient(vault_url=vault_uri, credential=credential)
    return client.get_secret(secret_name).value or ""
