
Repo to illustrate TDD topics for future talks/blogs

o) gathering coverage stats from the target server's container
   when tests are being run from a different container.

o) using tests named with a GUID

```
$ source ./scripts/makefile_shortcuts.sh

$ rut          # run all unit tests
$ rut a2189600 # run only unit test_a2189600

$ eut          # exec all unit tests in existing container
$ eut a2189600 # exec only unit test_a2189600 in existing container

$ rst          # run all system tests
$ rst 04692400 # run only system test_04692400
```