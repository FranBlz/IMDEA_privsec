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

    # Log Set-Cookie headers on response
    def response(self, flow):
        os.makedirs(self.base_path, exist_ok=True)
        if not (hasattr(flow, "response") and flow.response):
            return

        cookies = flow.response.headers.get_all("Set-Cookie")
        if not cookies:
            return

        with open(f"{self.base_path}/mitm_cookies.txt", "a", encoding="utf-8") as fh:
            for c in cookies:
                fh.write(f"{c}\n")

addons = [CookieLogger()]