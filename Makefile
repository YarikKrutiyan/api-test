CURRENT_DIR = $(PWD)

SELENIUM_ENV_DIR = $(CURRENT_DIR)/venv
LOG_DIR = $(CURRENT_DIR)/log


setup:
	# Get last code from project repository
#	git checkout api
#	git pull origin api


	# Install project requirements
	$(PIP_ENV) install -r requirements.txt
