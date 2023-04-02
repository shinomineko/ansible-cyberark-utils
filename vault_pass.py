#!/usr/bin/env python3

import os

vault_pass = os.environ.get("ANSIBLE_VAULT_PASS")

if vault_pass:
    print(vault_pass)
else:
    print("no ANSIBLE_VAULT_PASS found")
    raise SystemExit(1)
