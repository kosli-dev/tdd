
[![Github Action (main)](https://github.com/kosli-dev/tdd-talk/actions/workflows/main.yml/badge.svg)](https://github.com/kosli-dev/tdd-talk/actions)

The following blog posts link to this repo:
- [Get Python system-test coverage faster by restarting your server](https://www.kosli.com/blog/getting-python-integration-test-coverage-without-killing-your-gunicorn-server/)
- [How to strangle old code using Python decorators](https://www.kosli.com/blog/how-to-strangle-old-code-using-python-decorators/)  
- ...
- ...

A public demo repo of
- [gunicorn](https://gunicorn.org/) running with multiple workers
- each worker running a simple [Flask](https://flask.palletsprojects.com/en/2.2.x/) web server (with an API)
- the web server scores the [XY Business Game](https://leanpub.com/experientiallearning4sampleexercises) by [Jerry Weinberg](http://jonjagger.blogspot.com/p/jerry-weinberg.html)  
- the web server runs inside a read-only Docker container
- system tests with full branch coverage
- unit tests with full branch coverage

```
$ source scripts/shortcuts.sh

$ rst          # Run all System Tests in new server ~10s
$ est          # Exec all System Tests in restarted server ~4s
$ rst 04692400 # Run only System Test 04692400 in new server
$ est 04692400 # Exec only System Test 04692400 in restarted server

$ rut          # Run all Unit Tests in new server ~10s
$ eut          # Exec all Unit Tests in existing server ~1s
$ rut a2189600 # Run only Unit Test a2189600 in new server
$ eut a2189600 # Exec only Unit Test a2189600 in existing server

$ demo         # run a demo server on localhost:80
$ hup          # restart the demo server
$ tid          # generate a test id
```
