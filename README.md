# IMDEA_privsec

Personal repository dedicated to my internship at IMDEA Software

---

## To-Do list

1. Remove hard-coded address and port from framework and enable some sort of automatic selection.
2. Complete the pipeline so it has simple input for navigation and extension and outputs basic results for each component and its comparison.
3. Re-read SoK paper and inspect sources to add references and extend last paragraphs of thesis proposal.
4. Check cookie location and readability on Chrome and Firefox.
5. Read about partitioning cookies.
6. Read about session cookies and develop a framework to inspect how prevalent they are.
7. Improve on cookie parsing in both CDP and mitmproxy scripts.
8. Find out how to distinguish the real top level domain and log all cookie files on that dir alone.

---

## Issues & Notes

### Makefile

1. Created a browser template at `/tmp/template` that has secure DNS disabled and mitmproxy's ca-certificate manually imported to "Custom certificates" (otherwise Chrome fails to pickup OS-wide certificates, tested against curl and Firefox).
2. Created another browser template that features the `I still don't care about cookies` extension for automatic cookie consent acceptance (?).

### cookies_mitm.py

1. How to add python script (page navigation and CDP usage) on the same `mitmproxy` addon?
2. > warn: [11:58:25.667] [127.0.0.1:33410] Client TLS handshake failed. The client does
not trust the proxy's certificate for clientservices.googleapis.com (OpenSSL Error([('SSL routines', '', 'ssl/tls alert certificate unknown')]))
3. > Exception in thread Thread-5 (_recv_loop):
Traceback (most recent call last):
  File "/usr/lib/python3.13/threading.py", line 1043, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.13/threading.py", line 994, in run
    self._target(*self._args, **self._kwargs)
  File "/home/francisco_bolzan/.venvs/imdea/lib/python3.13/site-packages/pychrome/tab.py", line 122, in _recv_loop
    message = json.loads(message_json)
  File "/usr/lib/python3.13/json/_init__.py", line 346, in loads
    return_default_decoder.decode(s)
  File "/usr/lib/python3.13/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python3.13/json/decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

### cookie_logger.py

1. Opted for `pychrome` library since it offers the `call_method` function which seems to work ok and follows CDP method names in its parameters.
2. Initially discarded copying the Cookie DB since it's encrypted, for now focusing only on CDP `getCookies`method as a full cookie jar.
3. Python venv aliased to "activate".
4. Changed CDP and `mitmdump` ports to avoid collisions.

### Template

1. Created a clean browser template with manually imported mitmproxy ca-certificate and secure DNS disabled (because of weird behaviours between Chrome and Debian OS certificates).
2. Created `template_2` to add extension "I still don't care about cookies" extension to browser template to bypass the consent requests on each site.
3. Some cookies are featured on a list stored in `template_2`, possibly coming from the extensions used to bypass cookie consent warnings.

### General

1. Google detected unusual requests from network while using mitmproxy but not intercepting anything?
2. Some TLS handshake error messages still appear.
3. What's the initial traffic shown by mitmproxy?
4. How to isolate traffic to only the desired webpage.
5. How to automate the "Accept all cookies option for all webpages".
6. How to automate setup (make commands) and navigation (python script)?
7. How to properly choose ports?
8. Secuential runs of the tool seem to stop working for some reason.
9. Decided to remove any sort of parsing from the initial cookie_logger script

---

## Relevant resources

- [Official mitmproxy http doc](https://docs.mitmproxy.org/stable/api/mitmproxy/http.html)
- [Pychrome library page](https://pypi.org/project/pychrome/)
- [I still don't care about cookies extension](https://chromewebstore.google.com/detail/i-still-dont-care-about-c/edibdbjcniadpccecjdfdjjppcpchdlm)
- [About partitioned cookies](https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Privacy_sandbox/Partitioned_cookies)
- [About session cookies](https://www.cookieyes.com/blog/session-cookies/)
- [Free cookie checker](https://www.cookieyes.com/cookie-checker/)
- [Similar cookie detection project](https://github.com/CookieChecker/CookieCheckSourceCode)
- [About subprocess](https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module)

---

## Author

Francisco Bolzan - Research Assistant @ IMDEA Software
