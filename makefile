# Paths
PORT = 1234
DEV_PORT = 1235
ADDRESS = 127.0.0.1
TMP_FLDR = /tmp/profiles/
OUTPUT_FLDR = ./src/output/
TEMPLATE = ./src/template_2/
SITES_FILE = ./src/sites.txt

clean:
	rm -rf $(TMP_FLDR)*
	rm -rf $(OUTPUT_FLDR)*

browser:
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/

	google-chrome --user-data-dir=$(TMP_FLDR)$(PORT) --no-first-run \
	--remote-debugging-port=$(DEV_PORT) --remote-debugging-address=$(ADDRESS) \
	--remote-allow-origins=* --proxy-server="$(ADDRESS):$(PORT)" > /dev/null 2>&1 &

logger:
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/
	
	python3 ./src/cookie_logger.py "./src/cookies_mitm.py" $(ADDRESS) $(PORT) $(DEV_PORT) $(SITES_FILE) $(OUTPUT_FLDR)

proxy:
	mitmproxy --listen-host $(ADDRESS) -p $(PORT) -s cookies_mitm.py

.PHONY: clean browser logger proxy