#!/usr/bin/env python3
import os
import hashlib

class CookieLogger:
    # Initialize with base output path
    def __init__(self, base_path="./src/output/generic"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    # Generate a numeric hash for the full cookie set URL
    def _numeric_hash_for_url(self, url: str) -> str:
        h = hashlib.sha256(url.encode("utf-8")).digest()[:8]
        num = int.from_bytes(h, "big")
        return str(num)

    # Log Set-Cookie headers on response with format ./src/output/generic/<numeric-hash>.txt
    def response(self, flow):
        os.makedirs(self.base_path, exist_ok=True)
        if not (hasattr(flow, "response") and flow.response):
            return

        cookies = flow.response.headers.get_all("Set-Cookie")
        if not cookies:
            return

        url = getattr(flow.request, "pretty_url", getattr(flow.request, "url", ""))
        
        filename = self._numeric_hash_for_url(url) + ".txt"
        full_path = f"{self.base_path}/{filename}"

        with open(full_path, "a", encoding="utf-8") as fh:
            fh.write(f"{url}\n")
            for c in cookies:
                fh.write(f"{c}\n")
            fh.write("\n")

addons = [CookieLogger()]