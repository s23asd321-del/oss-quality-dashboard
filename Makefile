.PHONY: install test run scan-good scan-risky docker-build

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

run:
	python -m oss_quality_dashboard.app --host 127.0.0.1 --port 8000

scan-good:
	python -m oss_quality_dashboard.cli scan examples/sample-good-repo --format markdown

scan-risky:
	python -m oss_quality_dashboard.cli scan examples/sample-risky-repo --format json

docker-build:
	docker build -t oss-quality-dashboard .

