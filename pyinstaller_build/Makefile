MAIN = smcsc

all:
	pyinstaller --additional-hooks-dir ./hooks ../$(MAIN).py

clean:
	rm -r build dist

distclean: clean
	rm $(MAIN).spec

.PHONY: all clean
