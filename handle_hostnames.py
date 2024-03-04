# Importing the custom WebDriver class from the web_driver module
from web_driver import WebDriver

# List to store the hosts
hosts = []


def add_hosts(host):
    """
    Add a host to the list if it's not already present.

    Args:
        host (str): The hostname to add.

    Returns:
        bool: True if the host is added successfully, False if it already exists.
    """
    if host not in hosts:
        hosts.append(host)
        return True
    else:
        return False


def run_driver(hostname):
    """
    Initialize a WebDriver object for the given hostname.

    Args:
        hostname (str): The hostname to initialize the WebDriver for.

    Returns:
        WebDriver: The initialized WebDriver object.
    """
    # Initialize a WebDriver object for the given hostname
    driver = WebDriver(hostname)
    return driver
