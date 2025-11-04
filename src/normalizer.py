#!/usr/bin/env python3
from typing import Any, Dict

def _parse_set_cookie(header: str) -> Dict[str, Any]:
    parts = header.split(";")
    name_val = parts[0].strip()
    name, val = name_val.split("=", 1)
    cookie_dict = {}
    cookie_dict["name"] = name
    cookie_dict["value"] = val
    for key_val in parts[1:]:
        key, val = key_val.split("=", 1)
        cookie_dict[key.strip().lower()] = val.strip()
    return cookie_dict

def normalize_cookie(obj) -> Dict[str, Any]:
    if isinstance(obj, dict):
        # assume CDP cookie dict
        return {
            "name": obj.get("name"),
            "value": obj.get("value"),
            "domain": obj.get("domain"),
            "path": obj.get("path", "/"),
            "expires": (float(obj["expires"]) if obj.get("expires") not in (None, 0) else None),
            "httpOnly": bool(obj.get("httpOnly")),
            "secure": bool(obj.get("secure")),
            "session": bool(obj.get("session")),
            "sameSite": obj.get("sameSite") #, "raw": obj
        }
    elif isinstance(obj, str):
        # assume Set-Cookie string
        parsed = _parse_set_cookie(obj)
        a = parsed["attrs"]
        # compute expiry using Max-Age or Expires
        if "max-age" in a:
            exp = int(a.get("max-age"))
        elif "expires" in a:
            exp = int(a.get("expires"))
        else:
            exp = None
        ss = a.get("samesite")
        if isinstance(ss, str):
            ss = ss.capitalize() if ss.capitalize() in ("Lax", "Strict", "None") else None
        return {
            "name": parsed["name"],
            "value": parsed["value"],
            "domain": a.get("domain"),
            "path": a.get("path", "/"),
            "expires": float(exp) if exp  else None,
            "httpOnly": bool(a.get("httponly", False)),
            "secure": bool(a.get("secure", False)),
            "session": (exp is None),
            "sameSite": ss #, "raw": obj
        }