# ansible-cyberark-utils

Tested with CyberArk 12.2.2

## Usage

```shell
$ docker run --rm -v "${PWD}:/workspace" ghcr.io/shinomineko/ansible-cyberark-utils:main --help
usage: main.py [-h]

options:
  -h, --help
              required environment variables:
              ANSIBLE_INVENTORY          path to ansible inventory file
              ANSIBLE_USE_VAULT          use ansible vault to encrypt passwords. if ANSIBLE_USE_VAULT='false', the passwords will be added to ANSIBLE_INVENTORY (defaults to 'true')
              ANSIBLE_USE_PRIVATE_KEY    use key file to authenticate rather than passwords (defaults to 'false')
              CYBERARK_URL               base url of CyberArk
              CYBERARK_USER              CyberArk username
              CYBERARK_PASS              CyberArk password
              CYBERARK_REASON            reason for retrieving passwords

              optional environment variables:
              ANSIBLE_VAULT_PASS   password for ansible vault. requires when ANSIBLE_USE_VAULT='true'
```
