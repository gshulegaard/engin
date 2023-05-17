# engin
engin (Easy-NGINX) is an NGINX sidecar utility that provides an API and tries to
simplify server administration.

## Development

``` bash
$ make venv          # rm and create venv (~/venv/engin)
$ make docker-build  # rm and create local docker container(s)
$ make docker        # start and assume shell inside local container
```

From inside the local container you can do things like run the local server and
run tests.  Testing can be done outside the container using `venv` as well, the
container is provided for reproducibility/convenience.

You can run the server using `sanic` in the container or using the venv:

``` bash
python3 -m sanic engin.server.app:app --dev -v
```

### Testing

``` bash
(container) $ make test  # run tests using tox

# OR

(container) $ pytest tests/  # run specific tests using pytest
```


