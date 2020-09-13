all: pull track_language track_investments build

often: pull track_language commit push

rarely: pull track_investments commit push

publish: pull build commit push

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

commit:
	git add .
	git commit -m "Update by CircleCI `date` [skip ci]" || true

push:
	git push

# Cleanup
clean_vscode:
	rm -rf .vscode

clean_artifacts:
	rm -rf index.html investments.csv

clean: clean_artifacts clean_vscode

.PHONY: track_investments track_language build \
install_pipenv init pull commit push \
clean_vscode clean_artifacts
