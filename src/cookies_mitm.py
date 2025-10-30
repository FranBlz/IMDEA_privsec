import os

class CookieLogger:
    def __init__(self):
        self.path = "./output"

    def format(self, cookie):
        return str(cookie).replace("; ", "\n\t")

    def response(self, flow):
        # flow.response.headers.get_all --> list[str]
        if flow.response and flow.response.headers.get_all("Set-Cookie"):
            cookie_list = flow.response.headers.get_all("Set-Cookie")
            full_path = self.path + flow.request.pretty_url.replace("https:/", "")
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'a') as output:
                for cookie in cookie_list:
                    output.write(format(cookie)+'\n')
                output.close()

addons = [CookieLogger()]