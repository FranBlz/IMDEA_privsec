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

## Notes

### Makefile

1. Created a browser template at `/tmp/template` that has secure DNS disabled and mitmproxy's ca-certificate manually imported to "Custom certificates" (otherwise Chrome fails to pickup OS-wide certificates, tested against curl and Firefox).

### cookies_CDP.py

1. Opted for `pychrome` library since it offers the `call_method` function which seems to work ok and follows CDP method names in its parameters.
2. Initially discarded copying the Cookie DB since it's encrypted, for now focusing only on CDP `getCookies`method as a full cookie jar.
3. Implemented a `wait_for_port` method to enable both `cookies_CDP` and `mitmproxy` before booting up the browser instance and simulating browsing.
4. Python venv aliased to "activate"

### Issues

1. Google detected unusual requests from network while using mitmproxy but not intercepting anything?
2. Some TLS handshake error messages still appear
3. What's the initial traffic shown by mitmproxy?
4. How to isolate traffic to only the desired webpage
5. How to automate the "Accept all cookies option for all webpages"

---

## Relevant resources

- [Official mitmproxy http doc](https://docs.mitmproxy.org/stable/api/mitmproxy/http.html)

---

## Author

Francisco Bolzan - Research Assistant @ IMDEA Software
