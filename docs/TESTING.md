# Authentication

* Login 
  * Username/password must be filled out
  * Username or email can work to login
  * username or email case insesitive, password case sensitive
* Register
  * All fields required
  * Email must be a coloradoe.edu email
  * Confirm password must be the same as password
  * Username must not already be in use.
  * Email must not already be in use.
* Confirm
  * Token must be valid and not expired.
  * User must be logged in.
* Logout
  * User must be logged in.

# Post

* Making a post
  * Must be logged in
  * All fields required
  * Title < 500 chars
  * Body < 50000 chars

# Comment

* Making a comment
  * Must be logged in
  * All fields required
  * Body < 5000 chars

# Running tests

    $ pipenv shell
    (venv) $ flask test
    test_home (test_auth_views.AuthViewTestCase) ... ok
    test_login_logout (test_auth_views.AuthViewTestCase) ... ok
    test_register_confirm (test_auth_views.AuthViewTestCase) ... ok
    test_no_password_getter (test_user_model.UserModelTestCase) ... ok
    test_password_salts_are_random (test_user_model.UserModelTestCase) ... ok
    test_password_setter (test_user_model.UserModelTestCase) ... ok
    test_password_verification (test_user_model.UserModelTestCase) ... ok

    ----------------------------------------------------------------------
    Ran 7 tests in 0.777s

    OK
    
