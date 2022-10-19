
Repo to illustrate TDD topics for future talks/blogs

o) gathering coverage stats from the target server's container
   when tests are being run from a different container.

o) using tests named with a GUID

```
$ source ./shortcuts.sh

$ rut          # run all unit tests in new server
$ rut a2189600 # run only unit test_a2189600 in new server

$ eut          # exec all unit tests in existing server
$ eut a2189600 # exec only unit test a2189600 in existing server

$ rst          # run all system tests
$ rst 04692400 # run only system test_04692400

$ est          # exec all system tests in existing server
$ est 04692400 # exec only system test 04692400 in existing server
```