# ansible-cyberark-utils

## Usage
```shell
$ docker run --rm -v "${PWD}:/app" ghcr.io/shinomineko/ansible-cyberark-utils:main --help
usage: main.py [-h]

options:
  -h, --help
              required environment variables:
              ANSIBLE_INVENTORY    path to ansible inventory file
              ANSIBLE_USE_VAULT    use ansible vault to encrypt passwords. if ANSIBLE_USE_VAULT='false', the passwords will be added to ANSIBLE_INVENTORY (defaults to 'true')
              CYBERARK_URL         base url of CyberArk
              CYBERARK_USER        CyberArk username
              CYBERARK_PASS        CyberArk password
              CYBERARK_REASON      reason for retrieving passwords

              optional environment variables:
              ANSIBLE_VAULT_PASS   password for ansible vault. requires when ANSIBLE_USE_VAULT='true'
```
