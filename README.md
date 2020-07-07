# FLASKR

Flask based blog app based on the Flask tutorials.
https://flask.palletsprojects.com/en/1.1.x/tutorial/

Project to learn how to develop and distribute a python based web app.

---

## Python Development

### Dependency Management:
https://modelpredict.com/python-dependency-management-tools#all-solutions-compared

- poetry - https://python-poetry.org/docs/

- pyenv - https://github.com/pyenv/pyenv
        - https://python-poetry.org/docs/managing-environments/

### Web Framework
- flask - https://flask.palletsprojects.com/en/1.1.x/

### Linting and Formatting
- flake8 - https://pypi.org/project/flake8/
- pydocstyle - https://pypi.org/project/pydocstyle/
- black - https://pypi.org/project/black/

### Testing
- pytest - https://docs.pytest.org/en/stable/
- mock - https://pypi.org/project/mock/
- coverage - https://pypi.org/project/coverage/

### Documentation
- Sphinx - https://www.sphinx-doc.org/en/1.6/index.html

### Automation
- Makefile - https://www.gnu.org/software/make/manual/make.html

---

# Development

Developing in [VSCode](https://code.visualstudio.com/) is highly encouraged due
to how configurable it is and the great number of integrations with common
toolsets. Of course there is no requirement to use vscode, however a `.vscode`
settings file is provided to aid getting started with Flaskr development.

## Getting started

Requirements:
  - [Poetry](https://python-poetry.org/)

Once poetry is installed you can begin developing in the project.

## Makefile

Most of the common development tasks are configured in a Makefile to speed up
development processes.

To get started, `make install` will install the package and dependencies into
a local .venv directory.

You can then run the tests using `make test` to run all the tests, or specify
`make integration` or `make unit` in order to run those tests seperately.
A coverage report can be generated using `make cov`.

To generate documentation, `make docs` will create a `doc/sphinx/build` directory
where you can find an `index.html` which will take you to the documentation homepage
when opened in any modern web browser.
