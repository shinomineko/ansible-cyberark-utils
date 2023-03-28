import logging
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

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
