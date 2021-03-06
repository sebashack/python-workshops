VENV_DIR:=${CURDIR}/.env
PY_BIN:=${CURDIR}/.env/bin/python

.PHONY: set-py-venv
set-py-venv:
	rm -rf ${VENV_DIR}
	python3.8 -m venv ${VENV_DIR}
	${PY_BIN} -m pip install -U pip wheel setuptools

.PHONY: set-py-venv-with-deps
set-py-venv-with-deps: set-py-venv
	${VENV_DIR}/bin/pip install -r requirements.txt

.PHONY: run
run:
	${VENV_DIR}/bin/python src

.PHONY: test
test:
	${VENV_DIR}/bin/python -m unittest discover

.PHONY: check-style
check-style:
	python3 -m black --check ${CURDIR}/src

.PHONY: style
style:
	python3 -m black ${CURDIR}/src

.PHONY: clean
clean:
	rm -rf ${VENV_DIR}
	rm -rf ${CURDIR}/src/__pycache__
