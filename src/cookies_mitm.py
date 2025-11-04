#!/usr/bin/env python3
import os
import hashlib

class CookieLogger:
    # Initialize with base output path
    def __init__(self, base_path="./src/output"):
        self.base_path = base_path
        self.current_path = "./src/output/unknown"
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.current_path, exist_ok=True)

    # Generate a numeric hash for the full cookie set URL
    def _numeric_hash_for_url(self, url: str) -> str:
        h = hashlib.sha256(url.encode("utf-8")).digest()[:8]
        num = int.from_bytes(h, "big")
        return str(num)

    # Create directory for top-level site on request
    def request(self, flow):
        site = getattr(flow.request, "pretty_host", None)
        if site in ["www.instagram.com", "elpais.com", "lanacion.com"]:
            site_dir = os.path.join(self.base_path, site)
            os.makedirs(site_dir, exist_ok=True)
            self.current_path = site_dir

    # Log Set-Cookie headers on response with format ./output/<top-site>/<numeric-hash>.txt
    def response(self, flow):
        if not (hasattr(flow, "response") and flow.response):
            return

        cookies = flow.response.headers.get_all("Set-Cookie")
        if not cookies:
            return

        url = getattr(flow.request, "pretty_url", getattr(flow.request, "url", ""))
        
        filename = self._numeric_hash_for_url(url) + ".txt"
        full_path = os.path.join(self.current_path, filename)

        with open(full_path, "a", encoding="utf-8") as fh:
            fh.write(f"{url}\n")
            for c in cookies:
                fh.write(f"{c}\n")
            fh.write("\n")

addons = [CookieLogger()]