BUILDDIR='~build'


.mkbuilddir:
	mkdir -p ${BUILDDIR}


#test:
#	py.test -v --create-db

lint:
	pre-commit run --all-files

test:
	coverage run --rcfile=tests/.coveragerc --source drf_api_checker -m pytest tests
	coverage report --rcfile=tests/.coveragerc
	coverage html --rcfile=tests/.coveragerc

clean:
	rm -fr ${BUILDDIR} dist src/*.egg-info .coverage coverage.xml .eggs *.sqlite
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf

fullclean:
	rm -fr .tox .cache .pytest_cache
	$(MAKE) clean


docs: .mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/ ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
