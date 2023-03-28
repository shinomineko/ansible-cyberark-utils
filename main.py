#!/usr/bin/env python3

from config import *
from inventory import *
from cyberark import *
import logging
import os

log_level = os.environ.get("LOG_LEVEL", "INFO")

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

    inventory = load_inventory(envs["ansible_inventory"])

    make_cyberark_requests(cyberark_base_url, cyberark_user, cyberark_pass)


if __name__ == "__main__":
    main()
