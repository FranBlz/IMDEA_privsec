# IMDEA_privsec

Personal repository dedicated to my internship at IMDEA Software

---

## To-Do list

1. Develop a `mitmproxy` extension to record every cookie set by HTTP.
2. Make `cookies_CDP.py` asynchronous.
3. Remove hard-coded address and port from framework and enable some sort of automatic selection.
4. Complete the pipeline so it has simple input for navigation and extension and outputs basic results for each component and its comparison.
5. Re-read SoK paper and inspect sources to add references and extend last paragraphs of thesis proposal.
6. Achieve fresh replicability and instrumentation on a browser session.
7. Check cookie location and readability on Chrome and Firefox.
8. Read about partitioning cookies.
9. Read about session cookies and develop a framework to inspect how prevalent they are.
10. Develop framework to compare HTTP and total cookies set.
11. Read more about firefox CLI arguments and its devtools protocol.

---

## Issues & Notes

### Makefile

1. Created a browser template at `/tmp/template` that has secure DNS disabled and mitmproxy's ca-certificate manually imported to "Custom certificates" (otherwise Chrome fails to pickup OS-wide certificates, tested against curl and Firefox).

### cookies_mitm.py

1. How to add python script (page navigation and CDP usage) on the same `mitmproxy` addon?
2. > warn: [11:58:25.667] [127.0.0.1:33410] Client TLS handshake failed. The client does
not trust the proxy's certificate for clientservices.googleapis.com (OpenSSL Error([('SSL routines', '', 'ssl/tls alert certificate unknown')]))
3. > error: [11:58:25.768] Addon error: [Errno 21] Is a directory:
'./output/elpais.com/'
Traceback (most recent call last): \
File "cookies_mitm.py", line 16, in response \
with open(full_path, 'w') as output: \
IsADirectoryError: [Errno 21] Is a directory: './output/elpais.com/'
4. > error: [11:58:26.897] Addon error: [Errno 36] File name too long: \
'./output/dpm.demdex.net/id?d_visid_ver=5.5.0&d_fieldgroup=AAM&d_rtbd=json&d_ver=2&d_orgid=2387401053DB208C0A490D4C%40AdobeOrg&d_nsid=0&d_mid=19197974952010786700499441737247788783&d_blob=RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y&d_cid_ic=user_id%01not-set%011&d_cid_ic=AdobeCampaignID%01not-set%011&ts=1761821906827' \
Traceback (most recent call last): \
  File "cookies_mitm.py", line 16, in response \
    with open(full_path, 'w') as output: \
OSError: [Errno 36] File name too long: \
'./output/dpm.demdex.net/id?d_visid_ver=5.5.0&d_fieldgroup=AAM&d_rtbd=json&d_ver=2&d_orgid=2387401053DB208C0A490D4C%40AdobeOrg&d_nsid=0&d_mid=19197974952010786700499441737247788783&d_blob=RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y&d_cid_ic=user_id%01not-set%011&d_cid_ic=AdobeCampaignID%01not-set%011&ts=1761821906827'
5. > [127.0.0.1:1234]/home/francisco_bolzan/.venvs/imdea/lib/python3.13/site-packages/OpenSSL/crypto.py:1231: CryptographyDeprecationWarning: Parsed a serial number which wasn't positive (i.e., it was negative or zero), which is disallowed by RFC 5280.

### cookies_CDP.py

1. Opted for `pychrome` library since it offers the `call_method` function which seems to work ok and follows CDP method names in its parameters.
2. Initially discarded copying the Cookie DB since it's encrypted, for now focusing only on CDP `getCookies`method as a full cookie jar.
3. Implemented a `wait_for_port` method to enable both `cookies_CDP` and `mitmproxy` before booting up the browser instance and simulating browsing.
4. Python venv aliased to "activate".
5. Changed CDP and `mitmproxy` ports to avoid collisions.
6. Parsed cookie dictionary, better parsing might be considerable.

### Template

1. Created a clean browser template with manually imported mitmproxy ca-certificate and secure DNS disabled (because of weird behaviours between Chrome and Debian OS certificates).
2. Created `template_2` to add extension "I still don't care about cookies" extension to browser template to bypass the consent requests on each site.

### General

1. Google detected unusual requests from network while using mitmproxy but not intercepting anything?
2. Some TLS handshake error messages still appear.
3. What's the initial traffic shown by mitmproxy?
4. How to isolate traffic to only the desired webpage.
5. How to automate the "Accept all cookies option for all webpages".
6. How to automate setup (make commands) and navigation (python script)?
7. How to properly choose ports?
8. Secuential runs of the tool seem to stop working for some reason.

---

## Relevant resources

- [Official mitmproxy http doc](https://docs.mitmproxy.org/stable/api/mitmproxy/http.html)
- [Pychrome library page](https://pypi.org/project/pychrome/)
- [I still don't care about cookies extension](https://chromewebstore.google.com/detail/i-still-dont-care-about-c/edibdbjcniadpccecjdfdjjppcpchdlm)

---

## Author

Francisco Bolzan - Research Assistant @ IMDEA Software
