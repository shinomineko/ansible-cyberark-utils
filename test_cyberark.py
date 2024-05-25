import requests

from config import *
from cyberark import *


def test_cyberark_logon(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    want = "some-session-token"
    requests_mock.post(
        f"{base_url}/PasswordVault/api/auth/Cyberark/logon",
        json={"CyberArkLogonResult": want},
    )

    got = cyberark_logon(requests.Session(), base_url, "user", "pass")

    assert (
        got == want
    )  # broken test, the response was a json without a key: {'some-session-token'}


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


def test_cyberark_logoff(requests_mock):
    base_url = load_env()["cyberark_base_url"]
    want = {}
    requests_mock.post(f"{base_url}/PasswordVault/api/auth/logoff", json={})

    got = cyberark_logoff(requests.Session(), "some-session-token", base_url)

    assert got == want
