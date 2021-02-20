## Operating System

This code has only been run in Ubuntu 20.04.


## Set work environment

1. Run `make set-py-venv-with-deps`.
2. Run `source .env/bin/activate`.
3. To deactivate the environment run `deactivate`.

## Check style

```
make check-style
```

## Reformat code style

```
make style
```

## Run tests

```
make test
```

## Activate virtual environment

```
source .env/bin/activate
```

## Deactivate virtual environment

```
deactivate
```

## Run code

If venv is active:

```
python src
```

otherwise

```
make run
```
