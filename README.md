
Repo to illustrate TDD topics for planned talks/blogs

o) gathering coverage stats from the target server's container
   when tests are being run from a different container.

o) using tests functions of the form
       def test_696fa773():
           """
           Given alpha, When beta, Then gamma
           """
   rather than of the form
       def test_given_alpha_when_beta_then_gamma():
           ...
