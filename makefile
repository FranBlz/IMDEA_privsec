# Macros
PORT = 1234
DEV_PORT = 1235
ADDRESS = 127.0.0.1
TMP_FLDR = /tmp/profiles/
OUTPUT_FLDR = ./src/output/
TEMPLATE = ./src/template_3/
SITES_FILE = ./src/sites.txt

# To be used manually
clean:
	rm -rf $(TMP_FLDR)*
	rm -rf $(OUTPUT_FLDR)*

# To be used manually
browser:
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/

	google-chrome --user-data-dir=$(TMP_FLDR)$(PORT) --no-first-run \
	--remote-debugging-port=$(DEV_PORT) --remote-debugging-address=$(ADDRESS) \
	--remote-allow-origins=* --proxy-server="$(ADDRESS):$(PORT)" > /dev/null 2>&1 &

# To be used manually
logger:
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/
	
	python3 ./src/cookie_logger.py "./src/cookies_mitm.py" $(ADDRESS) $(PORT) $(DEV_PORT) $(SITES_FILE) $(OUTPUT_FLDR)

# To be used manually
proxy:
	mitmproxy --listen-host $(ADDRESS) -p $(PORT) -s cookies_mitm.py

# To be used manually
view:
	sqlite3 $(TMP_FLDR)$(PORT)/Default/Cookies "SELECT host_key, name, expires_utc FROM cookies;"

# To be used pipelined
fresh:
	rm -rf $(TMP_FLDR)*
	mkdir -p $(TMP_FLDR)$(PORT)
	cp -r $(TEMPLATE)* $(TMP_FLDR)$(PORT)/

.PHONY: clean browser logger proxy view fresh