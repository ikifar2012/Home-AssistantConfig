"""Constants for ESXi Stats."""
DOMAIN = "esxi_stats"
DOMAIN_DATA = "{}_data".format(DOMAIN)

PLATFORMS = ["sensor"]
REQUIRED_FILES = [
    "const.py",
    "esxi.py",
    "manifest.json",
    "sensor.py",
    "config_flow.py",
    "services.yaml",
    ".translations/en.json",
]
VERSION = "0.4.1"
ISSUE_URL = "https://github.com/wxt9861/esxi_stats/issues"

STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

CONF_NAME = "name"

DEFAULT_NAME = "ESXi Stats"
DEFAULT_PORT = 443

SUPPORTED_PRODUCTS = ["VMware ESX Server", "VMware VirtualCenter Server"]
AVAILABLE_CMND_VM_POWER = ["on", "off", "reboot", "reset", "shutdown", "suspend"]
AVAILABLE_CMND_VM_SNAP = ["all", "first", "last"]
VM = "vm"
COMMAND = "command"
