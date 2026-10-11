.PHONY: setup install dev test lint check

setup:
	conda env create -f environment.yml || pip install -r requirements.txt

install:
	pip install -r requirements.txt
	cd frontend && npm install

dev:
	powershell -ExecutionPolicy Bypass -File scripts/run_dev.ps1

test:
	pytest backend/tests/ -v

check:
	python scripts/check_dependencies.py
