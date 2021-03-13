all: pull track_language track_investments build deploy

often: pull track_language build deploy

rarely: pull track_investments build deploy

# Track and building
track_investments:
	pipenv run python3 investment_tracker.py

track_language:
	pipenv run python3 news_tracker.py

build:
	pipenv run python3 indexer.py

# Setup
install_pipenv:
	pip3 install pipenv

init:
	pipenv --python 3
	pipenv install

pull:
	git pull origin master

deploy:
	git config user.email "ooz@users.noreply.github.com"
	git config user.name "ooz"
	git add .
	git commit -m "Update by CircleCI `date` [skip ci]" || true
	git push

test: clean_coverage
	pipenv install --dev
	pipenv run coverage run --source=. -m pytest -vv
	pipenv run coverage report --omit="test/*"

# Cleanup
clean_vscode:
	rm -rf .vscode

clean_coverage:
	rm -rf htmlcov/
	rm -f .coverage

clean_artifacts:
	rm -rf index.html investments.csv

clean: clean_artifacts clean_vscode

.PHONY: track_investments track_language build \
install_pipenv init pull commit push \
clean_vscode clean_coverage clean_artifacts
