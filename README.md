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
7. Move the project to `IMDEA's` GitLab.
8. How to automate the "Accept all cookies option for all webpages" without browser extensions.
9. Revise chrome flags to reduce to only impactful ones.
10. Starting the session on the new tab already loads cookies from google bar in new tab.

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

### Cookies sqlite3 DB

Values:

> 0. |creation_utc|INTEGER|1||0
> 1. |host_key|TEXT|1||0
> 2. |top_frame_site_key|TEXT|1||0
> 3. |name|TEXT|1||0
> 4. |value|TEXT|1||0
> 5. |encrypted_value|BLOB|1||0
> 6. |path|TEXT|1||0
> 7. |expires_utc|INTEGER|1||0
> 8. |is_secure|INTEGER|1||0
> 9. |is_httponly|INTEGER|1||0
> 10. |last_access_utc|INTEGER|1||0
> 11. |has_expires|INTEGER|1||0
> 12. |is_persistent|INTEGER|1||0
> 13. |priority|INTEGER|1||0
> 14. |samesite|INTEGER|1||0
> 15. |source_scheme|INTEGER|1||0
> 16. |source_port|INTEGER|1||0
> 17. |last_update_utc|INTEGER|1||0
> 18. |source_type|INTEGER|1||0
> 19. |has_cross_site_ancestor|INTEGER|1||0

### Partitioned cookies

Uses a secondary key `top_frame_site_key` to partition the cookie jar.

### Session cookies

Uses the `expiration_utc` value to determine persistence (0 and very large numbers means session cookies). What about negative values?

### Automatic cookie acceptance

Extensions fail to accept all cookie banners presenting different behaviour from manual browsing and accepting (see images).
`Intractable Cookie Crumbs` mentions and modifies `BannerClick` which at the same time runs on `Selenium` and `OpenWPM` which runs on `Firefox`.
`Thou Shalt Not Reject` mentions `Priv-Accept` and `BannerClick` and modifies the latter heavily to detect and interact with `Cookiewalls`.
`Cookieverse` builds tool on top of `OpenWPM`.

### OpenWPM

- Added `openWPM` repo on `/home/`
- Installed `conda` and `openWPM` successfully
- Added `openWPM` as library under the `openWPM` pip profile
- Added alias for `openWPM` pip profile under `openwpm`
- Pending tests on `openWPM`

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
- [Chrome CLI flags](https://peter.sh/experiments/chromium-command-line-switches/)
- [BannerClick project](https://github.com/bannerclick/bannerclick?tab=readme-ov-file)
- [OpenWPM project](https://github.com/openwpm/OpenWPM)
- [Conda Installation](https://www.anaconda.com/docs/getting-started/miniconda/install#linux-2)

---

## Author

Francisco Bolzan - Research Assistant @ IMDEA Software
