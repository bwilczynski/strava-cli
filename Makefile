.PHONY: install clean

setupbuild:
	python setup.py build

setupinstall:
	python setup.py install

install: setupbuild setupinstall

clean:
	python setup.py clean --all
