include	.server

DEPLOY_DIR=.deployment

.PHONY: all build verify upload

all: build verify upload

build: $(DEPLOY_DIR)/custom.remote.python.tcp_socket.zip

verify:
	plugin_sdk verify_plugin

upload:
	plugin_sdk upload_plugin --server $(SERVER) --token_file .api_token --plugin_zip $(DEPLOY_DIR)/custom.remote.python.tcp_socket.zip

$(DEPLOY_DIR)/custom.remote.python.tcp_socket.zip: tcp_socket.py plugin.json
	plugin_sdk build_plugin --no_upload --deployment_dir $(DEPLOY_DIR)

# vim: noexpandtab
