import socket
import pychrome # type: ignore

def wait_for_port(host: str, port: int):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                print("Port open.")
                return True
            except (socket.timeout, ConnectionRefusedError):
                pass

wait_for_port("127.0.0.1", 1234)

# create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:1234")

# create a tab
tab = browser.new_tab()
tab.start()

# navigate
tab.call_method("Network.enable")
tab.call_method("Page.navigate", url="https://instagram.com", _timeout=5)

# wait for loading
tab.wait(10)

# get cookies
cookies = tab.call_method("Network.getCookies")
for cookie in cookies["cookies"]:
    print ("Cookie:")
    print ("\tName:", cookie["name"])
    print ("\tValue:", cookie["value"])
    print ("\tDomain:", cookie["domain"])
    print ("\n")

# stop and close the tab
tab.stop()
browser.close_tab(tab)