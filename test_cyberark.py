import requests

from config import *
from cyberark import *


def test_cyberark_logon(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    requests_mock.post(
        f"{base_url}/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon",
        json={"CyberArkLogonResult": "some-session-token"},
    )

    session_token = cyberark_logon(requests.Session(), base_url, "user", "pass")

    assert session_token == "some-session-token"


def test_cyberark_get_account_id(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    ip = "192.168.2.2"
    user = "ansible"
    requests_mock.get(
        f"{base_url}/PasswordVault/api/accounts?search={ip},{user}",
        json={
            "value": [{"id": "123abc", "name": "some-name", "safeName": "some-safe"}]
        },
    )

    account_id = cyberark_get_account_id(
        requests.Session(), "some-session-token", base_url, ip, user
    )
    assert account_id == "123abc"


def test_cyberark_get_password(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    reason = "running test"
    account_id = "123abc"
    requests_mock.get(
        f"{base_url}/PasswordVault/api/Accounts/{account_id}/password/retrieve",
        text="P@ssw0rdzz",
    )

    password = cyberark_get_password(
        requests.Session(), "some-session-token", base_url, account_id, reason
    )

    assert password == "P@ssw0rdzz"
