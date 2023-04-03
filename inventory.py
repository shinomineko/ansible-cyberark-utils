import logging
import os

import requests
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible_vault import Vault
from environs import Env

from cyberark import *

logger = logging.getLogger(__name__)


def load_inventory(inventory_file):
    loader = DataLoader()
    inventory_manager = InventoryManager(loader=loader, sources=inventory_file)
    vars_manager = VariableManager(loader=loader, inventory=inventory_manager)

    logger.debug(f"host list: {inventory_manager.get_hosts('all')}")
    logger.debug(f"vars: {vars_manager.get_vars()}")

    inventory = []

    for host in inventory_manager.get_hosts("all"):
        try:
            logger.debug(
                f"ip: {str(host)}, ansible_user: {vars_manager.get_vars(host=host)['ansible_user']}"
            )
            inventory.append(
                {
                    "ip": str(host),
                    "user": vars_manager.get_vars(host=host)["ansible_user"],
                }
            )
        except:
            logger.error(
                f"failed to parse inventory for host {str(host)}, no ansible_user provided"
            )

    logger.info(inventory)

    return inventory


def build_inventory(
    inventory_file,
    use_vault,
    cyberark_base_url,
    cyberark_user,
    cyberark_pass,
    cyberark_request_reason,
):
    inventory = load_inventory(inventory_file)

    session = requests.Session()
    session_token = cyberark_logon(
        session=session,
        base_url=cyberark_base_url,
        cyberark_user=cyberark_user,
        cyberark_pass=cyberark_pass,
    )

    for item in inventory:
        logger.info(item)
        account_id = cyberark_get_account_id(
            session=session,
            session_token=session_token,
            base_url=cyberark_base_url,
            ip=item["ip"],
            os_user=item["user"],
        )

        item.update({"account_id": account_id})

        password = cyberark_get_password(
            session=session,
            session_token=session_token,
            base_url=cyberark_base_url,
            account_id=account_id,
            reason=cyberark_request_reason,
        )

        item.update({"password": password})

    logger.debug(f"inventory: {inventory}")
    if use_vault:
        create_host_vars_vault(inventory=inventory, base_dir=".")
    else:
        logger.warning(
            "!!! updating plaintext passwords in an inventory only works with ini format inventories. please set ANSIBLE_USE_VAULT=true for non-ini format !!!"
        )
        update_password_to_ini_inventory(
            inventory=inventory, inventory_file=inventory_file
        )

    return


def update_password_to_ini_inventory(inventory, inventory_file):
    inventory_lines = []

    with open(inventory_file, "r") as file:
        inventory_lines = [line.strip() for line in file]
    file.close()

    for idx, line in enumerate(inventory_lines):
        for item in inventory:
            if item["ip"] in line:
                inventory_lines[idx] = f"{line} ansible_password=\"{item['password']}\""

    logger.debug(inventory_lines)

    os.remove(inventory_file)

    with open(inventory_file, "w") as file:
        for line in inventory_lines:
            file.write(f"{line}\n")
    file.close()

    return


def create_host_vars_vault(inventory, base_dir):
    host_vars_dir = f"{base_dir}/host_vars"
    env = Env()
    env.read_env()
    vault_pass = env("ANSIBLE_VAULT_PASS")

    vault = Vault(vault_pass)

    if not os.path.exists(host_vars_dir):
        logger.info(f"{host_vars_dir}s does not exist. creating...")
        os.makedirs(host_vars_dir)
        logger.info(f"created {host_vars_dir}s")

    for host in inventory:
        json_data = {"ansible_password": host["password"]}

        logger.info(
            f"creating host_vars file for {host['ip']} at {host_vars_dir}/{host['ip']}.yml"
        )
        with open(f"{host_vars_dir}/{host['ip']}.yml", "w") as vf:
            vault.dump_raw(json.dumps(json_data).encode("utf-8"), vf)

    return
