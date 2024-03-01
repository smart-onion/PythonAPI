from web_driver import WebDriver

hosts = []


def add_hosts(host):
    if host not in hosts:
        hosts.append(host)
        return True
    else:
        return False


def run_driver(hostname):
    driver = WebDriver(hostname)
    return driver

