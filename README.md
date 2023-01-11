
[![Github Action (main)](https://github.com/kosli-dev/tdd-talk/actions/workflows/main.yml/badge.svg)](https://github.com/kosli-dev/tdd-talk/actions)

A public demo repo of
- [gunicorn](https://gunicorn.org/) running with multiple workers
- each worker running a simple [Flask](https://flask.palletsprojects.com/en/2.2.x/) web server (with an API)
- system tests with full branch coverage
- unit tests with full branch coverage

The following blog posts link to this repo:
- Getting Python test coverage by restarting your gunicorn server (rather than killing it)
```
$ source scripts/shortcuts.sh

$ rst          # Run all System Tests in new xy server ~10s
$ est          # Exec all System Tests in restarted xy server ~4s
$ rst 04692400 # Run only System Test_04692400 in new xy server
$ est 04692400 # Exec only System Test 04692400 in restarted xy server

$ rut          # Run all Unit Tests in new xy server ~10s
$ eut          # Exec all Unit Tests in existing xy server ~1s
$ rut a2189600 # Run only Unit Test_a2189600 in new xy server
$ eut a2189600 # Exec only Unit Test a2189600 in existing xy server

$ tid          # generate a test id

$ demo         # run a demo server on localhost:80
$ hup          # restart the demo server
```
