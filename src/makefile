# Paths
PORT = 1234
ADDRESS = 127.0.0.1
TMP_FLDR = /tmp/profiles/
TEMPLATE = /tmp/template
NSSDB_FLDR = $(TMP_FLDR)$(PORT)/.pki/nssdb
MITM_CERT = /usr/local/share/ca-certificates/mitmproxy.crt

clean:
	rm -rf $(TMP_FLDR)*

launch:
	cp -r $(TEMPLATE) $(TMP_FLDR)$(PORT)

	google-chrome --user-data-dir=$(TMP_FLDR)$(PORT) --no-first-run \
	--remote-debugging-port=$(PORT) --remote-debugging-address=$(ADDRESS) \
	--remote-allow-origins=* --proxy-server="$(ADDRESS):$(PORT)" > /dev/null 2>&1 &

cdp:
	python3 record_cookies_CDP.py

proxy:
	mitmproxy --listen-host $(ADDRESS) -p $(PORT)

.PHONY: clean launch cdp proxy