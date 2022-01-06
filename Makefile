PYTHON = python3

.DEFAULT_GOAL = help

help:
	@echo "To install run: make install"
	@echo "To uninstall run: make uninstall"
	@echo "To run run: make run"
    
install:
	pip3 install .
    
uninstall:
	pip3 uninstall great_countdown
    
run:
	python3 src/great_countdown/main.py
