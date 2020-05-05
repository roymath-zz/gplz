run:
	PYTHONPATH=$(PWD)/src python src/gplz/demo/my_flask.py

test:
	curl -d '{"url": "https://google.com?q=flowers"}' -H "Content-Type: application/json" -Lv localhost:5000/ops/shorten


