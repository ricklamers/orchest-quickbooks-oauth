import os

from flask import Flask, request
from utils import get_shared_dict, get_quickbooks_client

app = Flask(__name__)

@app.route("/")
def index():
    return 'OAuth endpoint is running.'

@app.route("/confirm-settings")
def confirm_settings():
    
    shared_dict = get_shared_dict()
    shared_dict['confirmed_settings'] = True
    shared_dict.close()
    
    return 'Confirmed. You can close this window.'

@app.route("/callback")
def oauth_callback_endpoint():
    try:
        if "code" not in request.args or "realmId" not in request.args:
            raise Exception("Missing query arguments")
        
        state = request.args.get('state') # Optional, not used at the moment
        auth_code = request.args.get('code')
        realm_id = request.args.get('realmId')

        shared_dict = get_shared_dict()
        shared_dict["state"] = state
        shared_dict["realm_id"] = realm_id
        
        auth_client = get_quickbooks_client()
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)
        
        shared_dict["refresh_token"] = auth_client.refresh_token
        shared_dict["access_token"] = auth_client.access_token
        shared_dict["initial_auth_completed"] = True
        
        # Don't forget to close the shared_dict (it's backed by SQLite)
        shared_dict.close()
        
        return "Success: state, auth_code and realm_id have been stored. You can close this window."
    except Exception as e:
        raise e