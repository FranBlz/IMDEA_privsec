#!/usr/bin/env python3
import os
import sys
import time
import socket
import pychrome  # type: ignore
import subprocess

# ---------- helpers ----------
def wait_for_port(host: str, port: int):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                return True
            except (socket.timeout, ConnectionRefusedError):
                pass

def launch_mitmdump(script_path: str, listen_host: str, listen_port: int):
    cmd = ["mitmdump", "-s", script_path, "-p", str(listen_port), "--listen-host", listen_host]
    return subprocess.Popen(cmd, stdout=None, stderr=None)

def launch_browser(address: str, port_proxy: int, port_cdp: int):
    cmd = ["google-chrome",
           f"--user-data-dir=/tmp/profiles/{port_proxy}",
           f"--remote-debugging-port={port_cdp}",
           "--no-first-run",
           "--no-default-browser-check",
           f"--remote-debugging-address={address}",
           "--remote-allow-origins=*",
           f"--proxy-server={address}:{port_proxy}"]
    return subprocess.Popen(cmd, stdout=None, stderr=None)

# ---------- main ----------
if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python3 cookie_logger.py <mitm_script.py> <proxy_address> <proxy_port> <cdp_port> <sites_file> <output_folder>")
        print("Example: python3 cookie_logger.py cookies_mitm.py 127.0.0.1 1234 9222 sites.txt ./src/output/")
        sys.exit(1)

    mitm_script = sys.argv[1]
    address = sys.argv[2]
    port_proxy = int(sys.argv[3])
    port_cdp = int(sys.argv[4])
    cdp_url = f"http://{address}:{port_cdp}"

    # Transform sites file into list
    sites_file = sys.argv[5]
    with open(sites_file, 'r') as f:
        sites = f.readlines()

    # Ensure output folder exists
    output_folder = sys.argv[6]
    os.makedirs(output_folder, exist_ok=True)

    # Start mitmdump, wait and launch browser
    mitm_proc = launch_mitmdump(mitm_script, address, port_proxy)
    wait_for_port(address, port_proxy)
    browser_proc = launch_browser(address, port_proxy, port_cdp)
    wait_for_port(address, port_cdp)

    # Begin navigation and cookie extraction
    browser = pychrome.Browser(url=cdp_url)

    # For each site, navigate, extract cookies, and save the output present in generic folder into a named folder
    for site in sites:
        tab = browser.new_tab()
        tab.start()
        tab.call_method("Network.enable")
        tab.call_method("Page.navigate", url=site, _timeout=10)
        tab.wait(10)

        cookies = tab.call_method("Network.getCookies")
        os.makedirs("./src/output", exist_ok=True)
        with open("./src/output/CDP_cookies", 'a') as output:
            for cookie in cookies.get("cookies", []):
                output.write(str(cookie) + '\n')

        tab.stop()
        browser.close_tab(tab)
        os.rename("./src/output/generic", f"./src/output/{site.replace("https://", "")}")
        time.sleep(2)
    

    # Cleanup
    mitm_proc.kill()
    browser_proc.kill()
