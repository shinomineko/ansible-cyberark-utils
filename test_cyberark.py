import requests

from config import *
from cyberark import *


def test_cyberark_logon(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    want = "some-session-token"
    requests_mock.post(
        f"{base_url}/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon",
        json={"CyberArkLogonResult": want},
    )

    got = cyberark_logon(requests.Session(), base_url, "user", "pass")

    assert got == want


def test_cyberark_get_account_id(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    ip = "192.168.2.2"
    user = "ansible"
    want = "123abc"
    requests_mock.get(
        f"{base_url}/PasswordVault/api/accounts?search={ip},{user}",
        json={"value": [{"id": want, "name": "some-name", "safeName": "some-safe"}]},
    )

    got = cyberark_get_account_id(
        requests.Session(), "some-session-token", base_url, ip, user
    )
    assert got == want


def test_cyberark_get_password(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    reason = "running test"
    account_id = "123abc"
    want = "P@ssw0rdzz"
    requests_mock.post(
        f"{base_url}/PasswordVault/api/Accounts/{account_id}/password/retrieve",
        text='"P@ssw0rdzz"',
    )

    got = cyberark_get_password(
        requests.Session(), "some-session-token", base_url, account_id, reason
    )

    assert got == want
