#!/usr/bin/env python3

import argparse
import logging
import textwrap

from environs import Env

from config import *
from cyberark import *
from inventory import *

env = Env()
env.read_env()
log_level = env.log_level("LOG_LEVEL", "INFO")

logging.captureWarnings(True)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.RawTextHelpFormatter
    )
    help_msg = textwrap.dedent(
        """
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
    """
    )
    parser.add_argument("-h", "--help", action="help", help=help_msg)
    parser.parse_args()

    envs = load_env()
    build_inventory(
        envs["ansible_inventory"],
        envs["ansible_use_vault"],
        envs["ansible_use_private_key"],
        envs["cyberark_base_url"],
        envs["cyberark_user"],
        envs["cyberark_pass"],
        envs["cyberark_request_reason"],
    )


if __name__ == "__main__":
    main()
