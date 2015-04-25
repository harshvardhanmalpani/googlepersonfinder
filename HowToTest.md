| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/HowToTest'>direct link</a>).</font>


Every piece of new code, or significant change to existing code, should be accompanied by a corresponding new test or change in a test.  We have two kinds of tests: **unit tests**, which quickly exercise the code that has minimal dependencies, and **system tests**, which attempt to exercise every user-facing page and feature.

Our tests are run with [pytest](http://pytest.org).  We generally prefer to use plain `assert` because it's much easier to read.  For example, please write `assert x == 3` instead of `self.assertEquals(x, 3)`.  If the assertion fails, pytest will produce a nice report explaining what the value of `x` was.

`tools/all_tests` will run both the unit and server tests.

<br>
<h3>Unit tests</h3>

Each Python module in the <code>app/</code> directory should have a corresponding test module in the <code>tests/</code> directory, with a filename starting with <code>test_</code>.  For example, <code>app/indexing.py</code> contains the indexing and ranking functions, and there are unit tests for those functions in <code>tests/test_indexing.py</code>.<br>
<br>
You can run the unit tests with the script <code>tools/unit_tests</code>.  If you want to run the tests in just one module, specify the module name, e.g. <code>tools/unit_tests test_indexing</code>.<br>
<br>
<br>
<h3>System tests</h3>

The system tests bring up a running application server with a file-based stub for the datastore, put test data in the datastore, and issue HTTP requests to the server to simulate a user actually loading pages and clicking on buttons.<br>
<br>
All of the system tests currently reside in one file, <code>tests/server_test_cases.py</code>.  For efficiency, the tests are grouped into classes based on what data they modify.  Your tests can create and modify data by manipulating datastore entities just like regular application code.  For example, you can create a Person entity by instantiating the <code>Person</code> class and calling <code>put()</code> on it.<br>
<br>
You can run all the server tests with the script <code>tools/server_tests</code>.  If you want to run the tests in just one class or method, specify the <code>-k</code> option with any substring of the class or method name, e.g. <code>tools/server_tests -k test_subscribe</code>.<br>
<br>
To simulate the actions of a real user, your tests can use the <code>scrape</code> module to make HTTP requests, parse HTML, find links and buttons on the page, and submit forms.  See <a href='http://zesty.ca/scrape'>http://zesty.ca/scrape</a> for details on how to use the <code>scrape</code> tool.<br>
<br>
<br>

<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>