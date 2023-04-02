#!/usr/bin/env python3

import logging

from environs import Env

from config import *
from cyberark import *
from inventory import *

env = Env()
env.read_env()
log_level = env.log_level("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    envs = load_env()
    cyberark_base_url = envs["cyberark_base_url"]
    cyberark_user = envs["cyberark_user"]
    cyberark_pass = envs["cyberark_pass"]
    cyberark_request_reason = envs["cyberark_request_reason"]
    ansible_use_vault = envs["ansible_use_vault"]

    build_inventory(
        envs["ansible_inventory"],
        ansible_use_vault,
        cyberark_base_url,
        cyberark_user,
        cyberark_pass,
        cyberark_request_reason,
    )


if __name__ == "__main__":
    main()
