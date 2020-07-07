.PHONY: install init dev run lint format unit integration test cov docs clean

PACKAGE_NAME:=flaskr
PACKAGE_DIR:=./${PACKAGE_NAME}
TEST_DIR:=./tests
DOC_DIR:=./doc/sphinx
DOC_SRC:=${DOC_DIR}/source
DOC_BUILD:=${DOC_DIR}/build

CMD:=poetry run

install:
	poetry install

# initialise the database
init: export FLASK_APP=${PACKAGE_NAME}
init:
	$(CMD) flask init-db

# set the env for the flask app
dev: export FLASK_APP=${PACKAGE_NAME}
dev: export FLASK_ENV=development
dev: # run the flask server in devmode
	$(CMD) flask run

# set the env for the flask app
run: export FLASK_APP=${PACKAGE_NAME}
run:  # run the flask server
	$(CMD) flask run

lint:
	$(CMD) flake8 --filename "${PACKAGE_DIR}/*.py, ${TEST_DIR}/*.py" --max-line-length 88

format:
	$(CMD) black ${PACKAGE_DIR}/* ${TEST_DIR}/*

unit:
	$(CMD) coverage run -m pytest ${TEST_DIR}/unit

integration:
	$(CMD) coverage run -m pytest ${TEST_DIR}/integration

test:
	$(CMD) coverage run -m pytest ${TEST_DIR}

cov:
	$(CMD) coverage html

docs:
	$(CMD) sphinx-build -b html ${DOC_SRC} ${DOC_BUILD}

clean:
	# Delete all files in .gitignore
	git clean -Xdf
