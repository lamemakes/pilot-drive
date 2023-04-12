# Command vars
RM := rm -fr
UI_DIR := ui
BACKEND_DIR := backend
YARN := yarn --cwd $(UI_DIR)
PYTHON := python3

# Display vars
COLOR_LIGHT_PURPLE := '\e[1;35m'
COLOR_NC := '\e[0m'
PRINT_START := $(COLOR_LIGHT_PURPLE)============[
PRINT_END :=  ]============$(COLOR_NC)

# Web vars/paths
YARN_LOCK := $(UI_DIR)/yarn.lock
NODE_MODULES := $(UI_DIR)/node_modules
WEB_OUTPUT_DIR := $(BACKEND_DIR)/pilot_drive/web/files

# Python package vars/paths
PACKAGE_DIR := dist
EGG_INFO := $(BACKEND_DIR)/pilot_drive.egg-info

# Makefile vars/paths (see https://stackoverflow.com/questions/44036997/how-to-prevent-yarn-install-from-running-twice-in-makefile)
MANIFEST_DIR := $(UI_DIR)/.manifest
LAST_MANIFEST := $(MANIFEST_DIR)/node_modules.last
NEW_MANIFEST := $(MANIFEST_DIR)/node_modules.peek
GEN_MANIFEST := find $(NODE_MODULES)/ -exec stat -c '%n %y' {} \;

# Makefile commands for file tracking (see above)
$(shell mkdir -p $(MANIFEST_DIR) $(NODE_MODULES))
$(if $(wildcard $(LAST_MANIFEST)),,$(shell touch $(LAST_MANIFEST)))
$(shell $(GEN_MANIFEST) > $(NEW_MANIFEST))
$(shell cmp -s $(LAST_MANIFEST) $(NEW_MANIFEST) || touch $(NODE_MODULES))

.PHONY: all package web install clean

all: web package

# Build the python package
package:
	@echo -e $(PRINT_START)Building PILOT Drive package$(PRINT_END)
	$(PYTHON) -m build $(BACKEND_DIR) -o $(PACKAGE_DIR)

# Build only the frontend. Yarn configuration will output it to backend/pilot_drive/web/files/
web: install
	@echo -e $(PRINT_START)Building PILOT Drive UI$(PRINT_END)
	$(YARN) build --emptyOutDir

# Do a yarn install
install: $(LAST_MANIFEST)

$(LAST_MANIFEST): $(YARN_LOCK)
	$(GEN_MANIFEST) > $@

$(YARN_LOCK): $(NODE_MODULES) $(UI_DIR)/package.json
	@echo -e $(PRINT_START)Executing Yarn install$(PRINT_END)
	$(RM) $(NODE_MODULES) $(NODE_MODULES)
	$(YARN) install

# Cleanup!
clean:
	$(RM) $(NODE_MODULES) $(MANIFEST_DIR) $(PACKAGE_DIR) $(EGG_INFO) $(WEB_OUTPUT_DIR)