# Paths
PORT = 1234
ADDRESS = 127.0.0.1
DEV_PORT = 1235
TMP_FLDR = /tmp/profiles/
OUTPUT_FLDR = ./output/
TEMPLATE = ./template_2/
NSSDB_FLDR = $(TMP_FLDR)$(PORT)/.pki/nssdb
MITM_CERT = /usr/local/share/ca-certificates/mitmproxy.crt

clean:
	rm -rf $(TMP_FLDR)*
	rm -rf $(OUTPUT_FLDR)*

launch:
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/

	google-chrome --user-data-dir=$(TMP_FLDR)$(PORT) --no-first-run \
	--remote-debugging-port=$(DEV_PORT) --remote-debugging-address=$(ADDRESS) \
	--remote-allow-origins=* --proxy-server="$(ADDRESS):$(PORT)" > /dev/null 2>&1 &

cdp:
	python3 cookies_CDP.py

proxy:
	mitmproxy --listen-host $(ADDRESS) -p $(PORT) -s cookies_mitm.py

.PHONY: clean launch cdp proxy