update-packages:
	@ echo 'update requests'
	@ pip install --upgrade requests
	
	@ echo 'update lxml'
	@ pip install --upgrade lxml

update-dev-packages:
	@ echo 'update nose'
	@ pip install --upgrade nose

	@ echo 'update coverage'
	@ pip install --upgrade coverage

	@ echo 'update bottle'
	@ pip install --upgrade bottle	

test-all:
	@ rm -f -R tests/results/*
	@ nosetests --cover-package=webpage --verbosity=1

test-all-with-coverage:
	@ rm -f -R tests/results/*
	@ nosetests --cover-package=webpage --verbosity=1 --cover-erase --with-coverage

