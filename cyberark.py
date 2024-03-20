import json
import logging

requests_timeout_seconds = 30
requests_tls_verify = False

logger = logging.getLogger(__name__)


def cyberark_logon(session, base_url, cyberark_user, cyberark_pass):
    url = f"{base_url}/PasswordVault/api/auth/Cyberark/logon"
    headers = {"Content-Type": "application/json"}
    payload = {"username": cyberark_user, "password": cyberark_pass}
    json_payload = json.dumps(payload)

    json_response = session.post(
        url=url,
        headers=headers,
        data=json_payload,
        verify=requests_tls_verify,
        timeout=requests_timeout_seconds,
    ).json()

    session_token = json_response["CyberArkLogonResult"]
    logger.debug(json_response)
    logger.debug(f"session token: {session_token}")

    return session_token


def cyberark_get_account_id(session, session_token, base_url, ip, os_user):
    url = f"{base_url}/PasswordVault/api/accounts?search={ip},{os_user}"
    headers = {"Content-Type": "application/json", "Authorization": session_token}

    json_response = session.get(
        url=url,
        headers=headers,
        verify=requests_tls_verify,
        timeout=requests_timeout_seconds,
    ).json()

    account_id = json_response["value"][0]["id"]
    logger.debug(json_response)
    logger.info(f"found account id {account_id} for {ip} {os_user}")

    return account_id


def cyberark_get_password(session, session_token, base_url, account_id, reason):
    url = f"{base_url}/PasswordVault/api/Accounts/{account_id}/password/retrieve"
    headers = {"Content-Type": "application/json", "Authorization": session_token}
    payload = {"actionType": "Show", "reason": reason}
    json_payload = json.dumps(payload)

    response = session.post(
        url=url,
        headers=headers,
        data=json_payload,
        verify=requests_tls_verify,
        timeout=requests_timeout_seconds,
    )

    logger.debug(response.json())

    return response.text.strip('"')


def cyberark_logoff(session, session_token, base_url):
    url = f"{base_url}/PasswordVault/api/auth/logoff"
    headers = {"Content-Type": "application/json", "Authorization": session_token}
    payload = {}
    json_payload = json.dumps(payload)

    json_response = session.post(
        url=url,
        headers=headers,
        data=json_payload,
        verify=requests_tls_verify,
        timeout=requests_timeout_seconds,
    ).json()

    logger.debug(json_response)

    return json_response
