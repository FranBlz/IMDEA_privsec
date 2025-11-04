# Paths
PORT = 1234
DEV_PORT = 1235
ADDRESS = 127.0.0.1
OUTPUT_FLDR = ./src/output/
TEMPLATE = ./src/template_2/
TMP_FLDR = /tmp/profiles/

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
	
	python3 ./src/cookie_logger.py "./src/cookies_mitm.py" $(ADDRESS) $(PORT) $(DEV_PORT) "https://elpais.com" "https://instagram.com" "https://lanacion.com"

proxy:
	mitmproxy --listen-host $(ADDRESS) -p $(PORT) -s cookies_mitm.py

.PHONY: clean browser logger proxy