all: index

track_investments:
	pipenv run python3 investment_tracker.py

track_news:
	pipenv run python3 news_tracker.py

index: track_investments track_news
	pipenv run python3 indexer.py

publish: pull all
	git add .
	git commit -m "Update by CircleCI `date` [skip ci]" || true
	git push

# Setup
install_pipenv:
	pip3 install pipenv

init:
	pipenv --python 3
	pipenv install

pull:
	git pull origin master

# Cleanup
clean_vscode:
	rm -rf .vscode

clean_artifacts:
	rm -rf index.html investments.csv

clean: clean_artifacts clean_vscode

.PHONY: track_investments \
track_news \
install_pipenv init \
clean_vscode clean_artifacts
