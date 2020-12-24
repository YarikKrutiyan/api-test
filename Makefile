CURRENT_DIR = $(PWD)

SELENIUM_ENV_DIR = $(CURRENT_DIR)/selenium_env
OPS_DIR = $(CURRENT_DIR)/ops
LOG_DIR = $(CURRENT_DIR)/log


PIP_ENV = $(SELENIUM_ENV_DIR)/bin/pip



CHROME_DRIVER_LAST_VERSION = `curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`


setup:
	# Get last code from project repository
#	git checkout api
#	git pull origin api

	# Setup virtual environment
	if [ ! -d $(SELENIUM_ENV_DIR) ] ; then\
		virtualenv --python=python3.8 $(SELENIUM_ENV_DIR) ;\
	fi

	# Install project requirements
	$(PIP_ENV) install -r requirements.txt

 	# Get last stable version of chromedirver
	wget -P $(OPS_DIR) https://chromedriver.storage.googleapis.com/$(CHROME_DRIVER_LAST_VERSION)/chromedriver_linux64.zip

	# Remove older chromedriver if it exists
	if [ -d $(OPS_DIR)/chromedriver ] ; then\
		rm $(OPS_DIR)/chromedriver ;\
	fi

	# Unzip chromedriver
	unzip -o $(OPS_DIR)/chromedriver_linux64.zip  -d $(OPS_DIR)
	# Remove downloaded zip
	rm $(OPS_DIR)/chromedriver_linux64.zip