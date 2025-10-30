import os
import socket
import pychrome # type: ignore

def format(cookie):
    cookiestr = str(cookie)
    cookiestr = cookiestr.replace("{", "")
    cookiestr = cookiestr.replace("}", "\n")
    cookiestr = cookiestr.replace("'", "")
    cookiestr = cookiestr.replace(": ", "=")
    cookiestr = cookiestr.replace(", ", "\n\t")
    return cookiestr

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


wait_for_port("127.0.0.1", 1235)

# create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:1235")

URL_list = ["https://elpais.com", "https://lanacion.com", "https://instagram.com"]

for url in URL_list:
    # create a tab
    tab = browser.new_tab()
    tab.start()
    tab.wait(2)

    # navigate
    tab.call_method("Network.enable")
    tab.call_method("Page.navigate", url=url, _timeout=5)

    # wait for loading
    tab.wait(6)


    # get cookies
    cookies = tab.call_method("Network.getCookies")
    with open("./output/CDP_cookies", 'a') as output:
        for cookie in cookies["cookies"]:
            output.write(format(cookie) + '\n')

    # stop and close the tab
    tab.stop()
    browser.close_tab(tab)