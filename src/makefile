# Paths
PORT = 1234
ADDRESS = 127.0.0.1
TMP_FLDR = /tmp/profiles/
OUTPUT_FLDR = ./output/
TEMPLATE = ./template/
NSSDB_FLDR = $(TMP_FLDR)$(PORT)/.pki/nssdb
MITM_CERT = /usr/local/share/ca-certificates/mitmproxy.crt

clean:
	rm -rf $(TMP_FLDR)*
	rm -rf $(OUTPUT_FLDR)*

launch:
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/

	google-chrome --user-data-dir=$(TMP_FLDR)$(PORT) --no-first-run \
	--remote-debugging-port=$(PORT) --remote-debugging-address=$(ADDRESS) \
	--remote-allow-origins=* --proxy-server="$(ADDRESS):$(PORT)" \
	--disable-background-networking > /dev/null 2>&1 &

cdp:
	python3 record_cookies_CDP.py

proxy:
	mitmproxy --listen-host $(ADDRESS) -p $(PORT)
# 	 -s cookies_mitm.py

.PHONY: clean launch cdp proxy