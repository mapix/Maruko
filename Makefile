shell:
	python shell.py

clean_pyc:
	@find `pwd` \( -name '*.pyc' -o -name '*.ptlc' \) -type f -delete

serve:
	python manager.py serve

prepare_models:
	python manager.py prepare_models

recreate_store:
	python manager.py recreate_store
