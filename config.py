import logging
import os


logger = logging.getLogger(__name__)


def load_env():
    envs = {}

    envs["cyberark_user"] = os.environ.get("CYBERARK_USER")
    envs["cyberark_pass"] = os.environ.get("CYBERARK_PASS")
    envs["cyberark_base_url"] = os.environ.get("CYBERARK_URL")
    envs["cyberark_request_reason"] = os.environ.get("CYBERARK_REASON")

    envs["ansible_inventory"] = os.environ.get("ANSIBLE_INVENTORY")

    logger.info(envs)
    return envs
