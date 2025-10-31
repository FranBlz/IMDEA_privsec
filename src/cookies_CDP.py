import os
import sys
import socket
import pychrome # type: ignore
import subprocess

# function to format cookies, improve later if needed
def format(cookie):
    cookiestr = str(cookie)
    cookiestr = cookiestr.replace("{", "")
    cookiestr = cookiestr.replace("}", "\n")
    cookiestr = cookiestr.replace("'", "")
    cookiestr = cookiestr.replace(": ", "=")
    cookiestr = cookiestr.replace(", ", "\n\t")
    return cookiestr

# function to wait for a port to be open, to be deleted if full pipeline is achieved
def wait_for_port(host: str, port: int):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                return True
            except (socket.timeout, ConnectionRefusedError):
                pass

# function to launch a browser with specific profile and proxy/CDP settings
def launch_browser(address: str, port_proxy: int, port_cdp: int):
    return subprocess.Popen([
        f"google-chrome --user-data-dir=/tmp/profiles/{port_proxy} --remote-debugging-port={port_cdp} --no-first-run --no-default-browser-check --remote-debugging-address={address} --remote-allow-origins=*  > /dev/null 2>&1 &"],
        shell=True
    )


# Begin script ---------------------------------------------------------------------------------------
if len(sys.argv) < 4:
    print("Usage: python3 cookies_CDP.py <proxy_address> <proxy_port> <cdp_port> <site1> <site2> ... <siteN>")
else:    
    address = sys.argv[1]
    port_proxy = int(sys.argv[2])
    port_cdp = int(sys.argv[3])
    site_list = sys.argv[4:]
    cdp_url = f"http://{address}:{port_cdp}"

    # create and launch a browser instance with proxy @1234 and CDP @1235
    p = launch_browser(address, port_proxy, port_cdp)
    wait_for_port(address, port_cdp)
    browser = pychrome.Browser(url=cdp_url)

    for site in site_list:
        tab = browser.new_tab()
        tab.start()
        tab.wait(2)

        tab.call_method("Network.enable")
        tab.call_method("Page.navigate", url=site, _timeout=5)

        tab.wait(10)
        cookies = tab.call_method("Network.getCookies")
        with open("./output/CDP_cookies", 'a') as output:
            for cookie in cookies["cookies"]:
                output.write(format(cookie) + '\n')

        tab.stop()
        browser.close_tab(tab)