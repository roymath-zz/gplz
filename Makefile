all: run

run:
	PYTHONPATH=$(PWD)/src python src/gplz/demo/my_flask.py

install:
	pip install -r requirements.txt

test:
	curl -d '{"url": "https://google.com?q=flowers"}' -H "Content-Type: application/json" -Lv localhost:5000/ops/shorten
	curl -d '{"url": "https://google.com?q=flowers", "shortcode": "custom1"}' -H "Content-Type: application/json" -Lv localhost:5000/ops/custom
	curl -d '{"url": "https://google.com?q=flowers", "shortcode": "custom2"}' -H "Content-Type: application/json" -Lv localhost:5000/ops/custom

