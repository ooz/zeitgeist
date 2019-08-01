all: track index

track:
	pipenv run python3 tracker.py

index:
	pipenv run python3 indexer.py

install_pipenv:
	pip3 install pipenv

init:
	pipenv --python 3
	pipenv install

publish: all
	git add index.html investments.csv
	git commit -m "Update by CircleCI `date` [skip ci]" || true
	git push

# Cleanup
clean_vscode:
	rm -rf .vscode

clean: clean_vscode

.PHONY: track index \
install_pipenv init \
clean_vscode
