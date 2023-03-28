import json
import logging
import os
import requests

base_url = ""
session = requests.Session()
session_token = ""
requests_timeout_seconds = 30


def make_cyberark_requests(cyberark_base_url, cyberark_user, cyberark_pass):
    global base_url
    base_url = cyberark_base_url
    global session_token
    session_token = cyberark_logon(cyberark_user, cyberark_pass)

    return


def cyberark_logon(cyberark_user, cyberark_pass):
    url = f"{base_url}/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon"
    headers = {"Content-Type": "application/json"}
    payload = {"username": cyberark_user, "password": cyberark_pass}
    json_payload = json.dumps(payload)

    json_response = session.post(
        url=url,
        headers=headers,
        data=json_payload,
        verify=False,
        timeout=requests_timeout_seconds,
    ).json()

    session_token = json_response["CyberArkLogonResult"]

    return session_token


def cyberark_get_account_id(ip, os_user):
    url = f"{base_url}/PasswordVault/api/accounts?search={ip},{os_user}"
    headers = {"Content-Type": "application/json", "Authorization": session_token}

    json_response = session.get(
        url=url, headers=headers, verify=False, timeout=requests_timeout_seconds
    ).json()

    account_id = json_response["value"][0]["id"]

    return account_id


def cyberark_get_password(account_id, reason):
    url = f"{base_url}/PasswordVault/api/Accounts/{account_id}/password/retrieve"
    headers = {"Content-Type": "application/json", "Authorization": session_token}
    payload = {"actionType": "Show", "reason": reason}
    json_payload = json.dumps(payload)
    response = session.get(
        url=url,
        headers=headers,
        data=json_payload,
        verify=False,
        timeout=requests_timeout_seconds,
    )

    return response.text
