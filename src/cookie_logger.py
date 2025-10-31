import os
import sys
import socket
import subprocess
import time
import pychrome  # type: ignore
from typing import List

# ---------- helpers ----------
def format_cookie(cookie):
    s = str(cookie)
    s = s.replace("{", "")
    s = s.replace("}", "\n")
    s = s.replace("'", "")
    s = s.replace(": ", "=")
    s = s.replace(", ", "\n\t")
    return s

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
    cmd = f"mitmdump -s {script_path} -p {listen_port} --listen-host {listen_host}"
    return subprocess.Popen(cmd, shell=True)

def launch_browser(address: str, port_proxy: int, port_cdp: int):
    return subprocess.Popen([
        f"google-chrome --user-data-dir=/tmp/profiles/{port_proxy} --remote-debugging-port={port_cdp} --no-first-run --no-default-browser-check --remote-debugging-address={address} --remote-allow-origins=*  > /dev/null 2>&1 &"],
        shell=True
    )

# ---------- main ----------
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python3 cookie_logger.py <mitm_script.py> <proxy_address> <proxy_port> <cdp_port> <site1> [site2 ...]")
        print("Example: python3 cookie_logger.py cookies_mitm.py 127.0.0.1 1234 9222 https://example.com")
        sys.exit(1)

    mitm_script = sys.argv[1]
    address = sys.argv[2]
    port_proxy = int(sys.argv[3])
    port_cdp = int(sys.argv[4])
    sites: List[str] = sys.argv[5:]
    cdp_url = f"http://{address}:{port_cdp}"


    # Start mitmdump, wait and launch browser
    mitm_proc = launch_mitmdump(mitm_script, address, port_proxy)
    time.sleep(3)
    browser_proc = launch_browser(address, port_proxy, port_cdp)
    wait_for_port(address, port_cdp)

    # Begin navigation and cookie extraction
    browser = pychrome.Browser(url=cdp_url)

    try:
        for site in sites:
            tab = browser.new_tab()
            tab.start()
            tab.wait(2)
            tab.call_method("Network.enable")
            tab.call_method("Page.navigate", url=site, _timeout=10)
            tab.wait(8)

            cookies = tab.call_method("Network.getCookies")
            os.makedirs("./output", exist_ok=True)
            with open("./output/CDP_cookies", 'a') as output:
                for cookie in cookies.get("cookies", []):
                    output.write(format_cookie(cookie) + '\n')

            tab.stop()
            browser.close_tab(tab)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    except Exception as e:
        print("[!] Exception:", e)
    finally:
        try:
            browser_proc.kill()
        except Exception:
            pass
        try:
            mitm_proc.terminate()
            time.sleep(1)
            if mitm_proc.poll() is None:
                mitm_proc.kill()
        except Exception:
            pass
