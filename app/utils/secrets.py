import os
from functools import lru_cache

from google.cloud import secretmanager


@lru_cache(maxsize=64)
def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Read a secret from Google Secret Manager.
    Works on App Engine / Cloud Run using the service account.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        return default

    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{project_id}/secrets/{name}/versions/latest"
        resp = client.access_secret_version(request={"name": secret_path})
        return resp.payload.data.decode("utf-8").strip()
    except Exception:
        return default
