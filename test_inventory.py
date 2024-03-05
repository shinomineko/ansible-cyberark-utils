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
    got = load_inventory(load_env()["ansible_inventory"])

    assert got == want


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
    got = inventory_file.read()

    assert got == want


def test_create_host_vars_password_vault(tmpdir):
    inventory = [{"ip": "192.168.2.2", "user": "ansible", "password": "P@ssw0rdzz"}]
    host_var_file = tmpdir.join("host_vars/192.168.2.2.yml")
    create_host_vars_password_vault(inventory, tmpdir)

    vault = Vault(load_env()["ansible_vault_pass"])
    want = {"ansible_password": "P@ssw0rdzz"}
    got = vault.load(open(host_var_file).read())

    assert got == want


def test_create_host_vars_private_key(tmpdir):
    inventory = [
        {
            "ip": "192.168.3.3",
            "user": "ansible",
            "password": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAtHD3NoEryvsUhguqyqFVU9cSRJSJ13ZeoeLuLO0rsuZPQP1J\nuqLTNT39yrHnbVKbX2BDbqlL38+YpRfNI3NqDkPmYTHdtAgSiFxBqzZdLgcaSVxY\nJoDny3+u9TKYGvHr+Jl4ELoxhzYc7I8GDVwWdc34x+oC4Cct7487MxSjJNiVh7Td\nG6O1O6cxPG9+wz5GVH/yzgMNTBYXCEay9gVqws+3Q3nRHA2wdudytw7NngC+bLtt\n0EU0xtSllGZGWeSnXZKSPC9/wthAEQTMzoEvKa1lRyyFEcJpfY4XnOx79A+P26/k\nVeMbT+/KXI5Qj5fQGKaSB2IILvVoGBAp8ZdCGQIDAQABAoIBABjczeYSiKcNzzyk\nbpKVW01TlPP30ZcWJiDr71cnu33e3RcT2he00sxYb9gA3mYCXAqZbYEvI5dsTS3w\n/cuU3g1ReXTKqwU2Qt4gyXhJY9pxO8PVolx1Jjs0gIt5lAV2cHC52MDZSZ9wqy3v\nNm1wfbRwE9zxQhctCYJ45mEkm/wkqJ+HCRf8AIAZ5mTGkK3X0rvYH55MTF3WLyOr\nF/KN/j5RydUaQ7bsbKWFuAGI8mYtssZ6y5uDefmstS5gDp9L77lfXFZdC+7mj+yD\nZ1aTE0c8RPTEz9UhTqapFN+vGL9XY6qvGbFYsdZeLOHjCYoqV+VKovx/RQhiYIg6\nTx7C6ZcCgYEA9AbZ87GorYn5vbTnrjx+AEGGlWIpseAgq0GT3dNBqKIy6T261cX9\nWYUAa6alCCgoLlFMJIPWF8PyuJCLnfVAfTbO/p5Dm/DS0PCw2htLL9z05X77LQo+\nU11KsZus/OcxeTyFO53qXo38XRxOnSHlAAOTqydn4U1BV2exMoKgAv8CgYEAvUtv\nguNC7LPVvZ2bP9aXqTd8yge3bq+glzw7v15inE4cyK+3il9h0sWhExiR1yMqtOi8\nB8xExhZwPUKt3G2Lyc1IBh5aMtTsJYsQS955fybIeSzt9r/9uwV3ay45qINXMmW6\nVStv8jfXcr++QToAfQ6lpQ7U3LJA9GmC6JEhcucCgYEAjejuFqnaThFPCuOJV+oV\n3FA+0+CiHq8YUH9yXi3coRSyRrF/VZIuI0EVXYUrs/Kma0kb3qBMgMWTAYINr25Q\ncoDNH4UqDCWgc6GFN1FoCA2W3V9a8nZiiFhYd7DwiKJqQvbPBDxxb0ti10L+9KIh\nakCqP35LCtrChPHoOld8dkECgYA89L3D+ErkzkRV+xqzQ/cylpuoszNugT/Fc7AJ\nv+shSkYamfsQpAZsSRfFfnP4Q2rNNuTV3gGHiFI8Z+x0vxH0uhYnYj7Jf6dLr6xf\nwhR9zY9g9gbrHogmYWxDJ2+JxEGgCQInywURisnmObiaaIMfwke1D0GckAo6qn9t\nRM7woQKBgDXya2Gna+/ZnwnFrpG6JktKpzfmXTWHmUdSGlMHvc8ajKgtNLFnmZl2\nfMNh0cOKIBpsqDOk+kkdL7RNkQq/cBRn2hS5cV2PRoxbF0hND9DZ4oxNsTIAt8hp\nK2rqktr2JPMynWBjFOSGaQWOouUSlRXzvUBf4Dq2zBKHhzzc+Zv+\n-----END RSA PRIVATE KEY-----\n",
        }
    ]
    host_var_file = tmpdir.join("host_vars/192.168.3.3.yml")
    key_file = tmpdir.join("host_vars/keys/192.168.3.3.pem")
    create_host_vars_private_key(inventory, tmpdir)
    want = {}
    got = {}
    want['host_vars'] = """ansible_ssh_private_key_file: host_vars/keys/192.168.3.3.pem
"""
    want['key'] = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAtHD3NoEryvsUhguqyqFVU9cSRJSJ13ZeoeLuLO0rsuZPQP1J
uqLTNT39yrHnbVKbX2BDbqlL38+YpRfNI3NqDkPmYTHdtAgSiFxBqzZdLgcaSVxY
JoDny3+u9TKYGvHr+Jl4ELoxhzYc7I8GDVwWdc34x+oC4Cct7487MxSjJNiVh7Td
G6O1O6cxPG9+wz5GVH/yzgMNTBYXCEay9gVqws+3Q3nRHA2wdudytw7NngC+bLtt
0EU0xtSllGZGWeSnXZKSPC9/wthAEQTMzoEvKa1lRyyFEcJpfY4XnOx79A+P26/k
VeMbT+/KXI5Qj5fQGKaSB2IILvVoGBAp8ZdCGQIDAQABAoIBABjczeYSiKcNzzyk
bpKVW01TlPP30ZcWJiDr71cnu33e3RcT2he00sxYb9gA3mYCXAqZbYEvI5dsTS3w
/cuU3g1ReXTKqwU2Qt4gyXhJY9pxO8PVolx1Jjs0gIt5lAV2cHC52MDZSZ9wqy3v
Nm1wfbRwE9zxQhctCYJ45mEkm/wkqJ+HCRf8AIAZ5mTGkK3X0rvYH55MTF3WLyOr
F/KN/j5RydUaQ7bsbKWFuAGI8mYtssZ6y5uDefmstS5gDp9L77lfXFZdC+7mj+yD
Z1aTE0c8RPTEz9UhTqapFN+vGL9XY6qvGbFYsdZeLOHjCYoqV+VKovx/RQhiYIg6
Tx7C6ZcCgYEA9AbZ87GorYn5vbTnrjx+AEGGlWIpseAgq0GT3dNBqKIy6T261cX9
WYUAa6alCCgoLlFMJIPWF8PyuJCLnfVAfTbO/p5Dm/DS0PCw2htLL9z05X77LQo+
U11KsZus/OcxeTyFO53qXo38XRxOnSHlAAOTqydn4U1BV2exMoKgAv8CgYEAvUtv
guNC7LPVvZ2bP9aXqTd8yge3bq+glzw7v15inE4cyK+3il9h0sWhExiR1yMqtOi8
B8xExhZwPUKt3G2Lyc1IBh5aMtTsJYsQS955fybIeSzt9r/9uwV3ay45qINXMmW6
VStv8jfXcr++QToAfQ6lpQ7U3LJA9GmC6JEhcucCgYEAjejuFqnaThFPCuOJV+oV
3FA+0+CiHq8YUH9yXi3coRSyRrF/VZIuI0EVXYUrs/Kma0kb3qBMgMWTAYINr25Q
coDNH4UqDCWgc6GFN1FoCA2W3V9a8nZiiFhYd7DwiKJqQvbPBDxxb0ti10L+9KIh
akCqP35LCtrChPHoOld8dkECgYA89L3D+ErkzkRV+xqzQ/cylpuoszNugT/Fc7AJ
v+shSkYamfsQpAZsSRfFfnP4Q2rNNuTV3gGHiFI8Z+x0vxH0uhYnYj7Jf6dLr6xf
whR9zY9g9gbrHogmYWxDJ2+JxEGgCQInywURisnmObiaaIMfwke1D0GckAo6qn9t
RM7woQKBgDXya2Gna+/ZnwnFrpG6JktKpzfmXTWHmUdSGlMHvc8ajKgtNLFnmZl2
fMNh0cOKIBpsqDOk+kkdL7RNkQq/cBRn2hS5cV2PRoxbF0hND9DZ4oxNsTIAt8hp
K2rqktr2JPMynWBjFOSGaQWOouUSlRXzvUBf4Dq2zBKHhzzc+Zv+
-----END RSA PRIVATE KEY-----
"""
    got['host_vars'] = host_var_file.read()
    got['key'] = key_file.read()
    assert got == want
