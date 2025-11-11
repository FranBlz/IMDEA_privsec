# IMDEA_privsec

Personal repository dedicated to my internship at IMDEA Software

---

## To-Do list

1. Revise port selection to support parallel instances and avoid hard coded values whenever possible.
2. Find out how to get the cookie DB values while the browser is open (avoid DB lock condition).
3. Modify framework to allow parallelism.
4. Restructure `Makefile` and `cookie_logger.py` to avoid over-dependancy and hard coded values.
5. Revise page loading conditions to avoid using `wait` calls.
6. Instrument `CDP` via `Selenium` to avoid using iffy python libraries.
7. Remove google's translate pop-up.
8. Find out a way to avoid opening the `google` tab on each fresh browser session.
9. Move the project to `IMDEA's` GitLab.
10. How to automate the "Accept all cookies option for all webpages" without browser extensions.
11. Fix pending `TLS`, `pychrome` and `CDP` related errors.

---

## Issues & Notes

### Makefile

1. Created a browser template at `/tmp/template` that has secure DNS disabled and mitmproxy's ca-certificate manually imported to "Custom certificates" (otherwise Chrome fails to pickup OS-wide certificates, tested against curl and Firefox).
2. Created another browser template that features the `I still don't care about cookies` extension for automatic cookie consent acceptance (?).
3. Catalogued `make` calls by manual or scripted use.

### cookies_mitm.py

1. > warn: [11:58:25.667] [127.0.0.1:33410] Client TLS handshake failed. The client does
not trust the proxy's certificate for clientservices.googleapis.com (OpenSSL Error([('SSL routines', '', 'ssl/tls alert certificate unknown')]))
2. > Exception in thread Thread-5 (_recv_loop):
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

1. Avoided cookie formatting as much as possible.
2. Python venv aliased to "activate".
3. Changed CDP and `mitmdump` ports to avoid collisions.

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
