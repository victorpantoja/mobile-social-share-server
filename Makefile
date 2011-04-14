help:
	@echo 'USAGE: make <target>'
	@echo '-----------------'
	@echo 'Available targets'
	@echo '-----------------'
	@echo '    all............................cleans up and runs tests'
	@echo '    test...........................runs all tests'
	@echo '    clean..........................removes all .pyc files and all reports'
	@echo '    functional.....................runs all mss functional tests'
	

all: clean test

test: functional

clean:
	@echo "Cleaning up build, *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build

functional: clean
	@echo "Running mss functional tests..."
	@nosetests -s --verbose --with-coverage --cover-package=handlers tests/functional/*