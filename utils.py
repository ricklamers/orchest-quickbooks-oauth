import os
from orchest import services

from sqlitedict import SqliteDict
from intuitlib.client import AuthClient

def get_shared_dict():
    sqlite_dict_path = os.environ.get("SQLITE_LOCATION", "/data/quickbooks-oauth.sqlite")
    return SqliteDict(sqlite_dict_path, autocommit=True)

def construct_oauth_server_url():
    host = os.environ.get("HOST")
    return services.get_service("flask-oauth")["external_urls"][80].format(host_name=host, port=80).replace(":80/", "/")

def construct_redirect_url():
    return construct_oauth_server_url() + "callback"

def get_quickbooks_client():
    
    shared_dict = get_shared_dict()

    client_id = os.environ.get("QB_CLIENT_ID")
    client_secret = os.environ.get("QB_CLIENT_SECRET")
    
    try:
        redirect_uri = construct_redirect_url()
    except Exception:
        redirect_uri = None
    
    environment = os.environ.get("QB_CLIENT_ENVIRONMENT")

    return AuthClient(
        client_id,
        client_secret,
        redirect_uri,
        environment,
        refresh_token = shared_dict.get("refresh_token"),
        realm_id = shared_dict.get("realm_id"),
        access_token = shared_dict.get("access_token")
    )

