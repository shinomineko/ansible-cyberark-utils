import logging

from environs import Env

logger = logging.getLogger(__name__)


def load_env():
    env = Env()
    env.read_env()

    envs = {}

    envs["cyberark_user"] = env("CYBERARK_USER")
    envs["cyberark_pass"] = env("CYBERARK_PASS")
    envs["cyberark_base_url"] = env("CYBERARK_URL")
    envs["cyberark_request_reason"] = env("CYBERARK_REASON")

    envs["ansible_inventory"] = env("ANSIBLE_INVENTORY")
    envs["ansible_use_vault"] = env.bool("ANSIBLE_USE_VAULT", True)
    envs["ansible_vault_pass"] = env("ANSIBLE_VAULT_PASS")

    logger.info(envs)
    return envs
