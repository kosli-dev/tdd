
Repo to illustrate TDD topics for future talks/blogs

o) gathering coverage stats from the target server's container
   when tests are being run from a different container.

o) using tests named with a GUID

```
$ source ./scripts/test_aliases.sh

$ rut          # run all unit tests
$ rut a2189600 # run only unit test_a2189600

$ rst          # run all system tests
$ rst 04692400 # run only system test_04692400
```