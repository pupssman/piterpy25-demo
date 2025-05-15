# Docker management
DOCKER_IMAGE = esp-api-flasher
DOCKER_PORT = 8080

.PHONY: build run flash reboot flash_reboot

# Build Docker image
build:
	docker build -t $(DOCKER_IMAGE) .

# Run Docker container
run:
	docker run -p $(DOCKER_PORT):8080 $(DOCKER_IMAGE)

# ESP8266 management
SERIAL_PORT = /dev/ttyUSB0

# Flash the ESP8266
flash:
	ampy --port $(SERIAL_PORT) put main.py

# Reboot the ESP8266
reboot:
	ampy --port $(SERIAL_PORT) reset

# Combined flash and reboot
flash_reboot: flash reboot

# Show help
help:
	@echo "Available targets:"
	@echo "  build      - Build Docker image"
	@echo "  run        - Run Docker container"
	@echo "  flash      - Upload code to ESP8266"
	@echo "  reboot     - Reboot ESP8266"
	@echo "  flash_reboot - Upload code and reboot ESP8266"

.DEFAULT_GOAL := help
