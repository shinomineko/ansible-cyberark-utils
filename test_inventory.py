from inventory import *
from config import *


def test_load_inventory():
    assert load_inventory(load_env()["ansible_inventory"]) == [
        {"ip": "192.168.2.2", "user": "ansible"},
        {"ip": "192.168.3.3", "user": "ansible"},
        {"ip": "192.168.4.4", "user": "ansible1"},
        {"ip": "192.168.5.5", "user": "ansible2"},
    ]
