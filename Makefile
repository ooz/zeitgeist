all: index

track_investments:
	pipenv run python3 tracker.py

track_weather:
	curl de.wttr.in/Leipzig?3mTFq > weather.txt 2> stderr.txt
	curl de.wttr.in/Hamburg?3mTFq >> weather.txt 2>> stderr.txt

index: track_investments track_weather
	pipenv run python3 indexer.py
	$(MAKE) clean_weather

publish: all
	git add index.html investments.csv
	git commit -m "Update by CircleCI `date` [skip ci]" || true
	git push

# Setup
install_pipenv:
	pip3 install pipenv

init:
	pipenv --python 3
	pipenv install

# Cleanup
clean_vscode:
	rm -rf .vscode

clean_artifacts:
	rm -rf index.html investments.csv

clean_weather:
	rm -rf weather.txt stderr.txt

clean: clean_artifacts clean_weather clean_vscode

.PHONY: track_investments \
install_pipenv init \
clean_vscode clean_artifacts clean_weather
