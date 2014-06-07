update-packages:
	@ echo 'update requests'
	@ pip install --upgrade requests
	
	@ echo 'update lxml'
	@ pip install --upgrade lxml

update-dev-packages:
	@ echo 'update pylint'
	@ pip install --upgrade pylint

	@ echo 'update nose'
	@ pip install --upgrade nose

	@ echo 'update coverage'
	@ pip install --upgrade coverage

	@ echo 'update bottle'
	@ pip install --upgrade bottle	

	@ echo 'update pydoc2md'
	@ rm -f ../bin/pydoc2md.py
	@ curl https://raw.githubusercontent.com/ownport/pydoc2md/master/pydoc2md.py \
			-o ../bin/pydoc2md.py
	@ chmod +x ../bin/pydoc2md.py

test-all:
	@ rm -f -R tests/results/*
	@ nosetests --cover-package=webpage --verbosity=1

test-all-with-coverage:
	@ rm -f -R tests/results/*
	@ nosetests --cover-package=webpage --verbosity=1 --cover-erase --with-coverage

update-docs-api:
	@ echo 'Updating Webpage API docs ... '
	@ echo '- webpage'
	@ pydoc2md.py webpage > docs/api/index.md
	@ echo '- webpage.cleaner'
	@ pydoc2md.py webpage.cleaner > docs/api/cleaner.md
	@ echo '- webpage.content'
	@ pydoc2md.py webpage.content > docs/api/content.md
	@ echo '- webpage.fetcher'
	@ pydoc2md.py webpage.fetcher > docs/api/fetcher.md
	@ echo '- webpage.page'
	@ pydoc2md.py webpage.page > docs/api/page.md
	@ echo '- webpage.template'
	@ pydoc2md.py webpage.template > docs/api/template.md
	@ echo '- webpage.utils'
	@ pydoc2md.py webpage.utils > docs/api/utils.md
	@ echo 'Done'

