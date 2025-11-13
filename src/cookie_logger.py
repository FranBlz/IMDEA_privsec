#!/usr/bin/env python3
import os
import sys
import json
import time
import socket
import sqlite3
import subprocess
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore

# ---------- helpers ----------
# Auxiliary function to wait for ports
def wait_for_port(host: str, port: int):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                return True
            except (socket.timeout, ConnectionRefusedError):
                pass

# Auxiliary function to launch mitmdump with parameters
def launch_mitmdump(script_path: str, listen_host: str, listen_port: int):
    cmd = ["mitmdump", "-s", script_path, "-p", str(listen_port), "--listen-host", listen_host]
    return subprocess.Popen(cmd, stdout=None, stderr=None)

# Auxiliary function to launch Chrome with parameters using selenium
def launch_browser(user_data_dir: str, address: str, port_proxy: int, port_cdp: int):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--proxy-server=http://{address}:{port_proxy}")
    chrome_options.add_argument(f"--remote-debugging-port={port_cdp}")
    chrome_options.add_argument(f"--remote-debugging-address={address}")
    chrome_options.add_argument("--remote-allow-origins=*")

    # Optional preferences (prevents "Chrome is being controlled by automated test software" from hiding UI elements)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Auxiliary function to fecth cookies from sqlite3 database stored in browser profile
def fetch_sqlite3_cookies(profile_path: str):
    conn = sqlite3.connect(os.path.join(profile_path, "Default", "Cookies"))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, top_frame_site_key, name, expires_utc FROM cookies")
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    json_data = json.dumps(data, indent=4)
    return json_data

# Auxiliary function to format cookies from mitmdump into a JSON array of dicts
def format_cookies(input_path: str):
    dict_list = []
    with open(input_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                fields = line.split(';')
                cookie_dict = {}
                (name, value) = fields[0].split('=', 1)
                cookie_dict['name'] = name.strip()
                cookie_dict['value'] = value.strip()
                for field in fields[1:]:
                    if '=' in field:
                        key, value = field.split('=', 1)
                        cookie_dict[key.strip()] = value.strip()
                    else:
                        cookie_dict[field.strip()] = True
                dict_list.append(cookie_dict)
    formatted = json.dumps(dict_list, indent=4)
    return formatted

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
    output_generic = f"{output_folder}/generic"

    # For each site launch a clean browser and mitmdump session and extract CDP and sqlite3 cookies
    for site in sites:
        # 1. Start mitmdump and fresh browser instance, use ports as semaphores
        mitm_proc = launch_mitmdump(mitm_script, address, port_proxy)
        wait_for_port(address, port_proxy)
        browser_proc = launch_browser(f"/tmp/profiles/{port_proxy}", address, port_proxy, port_cdp)
        wait_for_port(address, port_cdp)

        # 2. Begin navigation, give time for page load and accept cookie banner
        browser_proc.get(site.strip())
        time.sleep(10)
        browser_proc.find_element(By.XPATH, '//*[@class="pmConsentWall-button"]').click()
        time.sleep(10)

        # 3. Close mitmproxy to stop network traffic
        mitm_proc.kill()
        time.sleep(2)

        # 4. Fetch cookies via CDP
        cdp_cookies = browser_proc.execute_cdp_cmd("Network.getAllCookies", {})
        json_cookies = json.dumps(cdp_cookies["cookies"], indent=4)
        os.makedirs(output_generic, exist_ok=True)
        with open(f"{output_generic}/CDP_cookies", 'a') as output:
            output.write(json_cookies)

        # 5. Fetch cookies via Selenium
        selenium_cookies = browser_proc.get_cookies()
        json_cookies = json.dumps(selenium_cookies, indent=4)
        os.makedirs(output_generic, exist_ok=True)
        with open(f"{output_generic}/Selenium_cookies", 'a') as output:
            output.write(json_cookies)

        # 6. Fetch cookies via sqlite3 before browser closure
        before_cookies = fetch_sqlite3_cookies(f"/tmp/profiles/{port_proxy}")
        with open(f"{output_generic}/sqlite3_cookies_before", 'a') as output:
            output.write(before_cookies)

        # 7. Close browser
        browser_proc.quit()
        time.sleep(5)

        # 8. Fetch cookies via sqlite3 after browser closure
        after_cookies = fetch_sqlite3_cookies(f"/tmp/profiles/{port_proxy}")
        with open(f"{output_generic}/sqlite3_cookies_after", 'a') as output:
            output.write(after_cookies)        

        # 9. Format cookies logged via mitmdump
        formatted_cookies = format_cookies(f"{output_generic}/mitm_cookies.txt")
        with open(f"{output_generic}/mitm_cookies_formatted", 'a') as output:
            output.write(formatted_cookies)

        # 10. Save named folder and reset browser profile for next site
        subprocess.Popen(["make", "fresh"], stdout=None, stderr=None)
        os.rename(output_generic, f"./src/output/{site.replace("https://", "")}")
        time.sleep(2)