import os

from ansible_vault import Vault

from config import *
from inventory import *


def test_load_inventory():
    want = [
        {"ip": "192.168.2.2", "user": "ansible"},
        {"ip": "192.168.3.3", "user": "ansible"},
        {"ip": "192.168.4.4", "user": "ansible1"},
        {"ip": "192.168.5.5", "user": "ansible2"},
    ]

    assert load_inventory(load_env()["ansible_inventory"]) == want


def test_update_password_to_ini_inventory(tmpdir):
    inventory = [{"ip": "192.168.2.2", "user": "ansible", "password": "P@ssw0rdzz"}]
    inventory_file = tmpdir.join(load_env()["ansible_inventory"])
    inventory_content = """[alpha]
192.168.2.2

[alpha:vars]
ansible_user=ansible
"""

    with open(inventory_file, "w") as f:
        f.write(inventory_content)

    want = """[alpha]
192.168.2.2 ansible_password="P@ssw0rdzz"

[alpha:vars]
ansible_user=ansible
"""

    update_password_to_ini_inventory(inventory, inventory_file)

    assert inventory_file.read() == want


def test_create_host_vars_vault(tmpdir):
    inventory = [{"ip": "192.168.2.2", "user": "ansible", "password": "P@ssw0rdzz"}]
    host_var_file = tmpdir.join("host_vars/192.168.2.2.yml")
    create_host_vars_vault(inventory, tmpdir)

    vault = Vault(load_env()["ansible_vault_pass"])
    got = vault.load(open(host_var_file).read())
    want = {"ansible_password": "P@ssw0rdzz"}

    assert got == want
