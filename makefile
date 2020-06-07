b build: clean
	python3 snake.py dist

i install:
	pip3 install .

u uninstall:
	pip3 uninstall .

d develop: build
	pip3 install -e .

p publish: build
	python3 -m twine upload dist/*


clean:
	python3 snake.py clean --all
	rm -fr dist
