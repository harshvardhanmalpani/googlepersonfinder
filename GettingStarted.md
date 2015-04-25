| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/GettingStarted'>direct link</a>).</font>

You can develop on Linux, or Mac OS, or Windows-with-Cygwin.

<br>
<h2>Step 1. Get tools</h2>

You will probably be happiest if you do these steps in order.<br>
<br>
<font color='#777'>
<b>Python 2.7.x</b> (you may already have this; try running "python" or "python2.7" to check)<br>
<ul><li>All platforms: <a href='https://www.python.org/download/releases/2.7.6'>Download here</a> and install<br>
</li><li>Mac OS X: the pre-installed Python binaries are at /System/Library/Frameworks/Python.framework/Versions/2.x/bin/python2.x and are symlinked from /usr/bin/python2.x.  If you downloaded and installed a new version, it will be in /Library/Frameworks rather than /System/Library/Frameworks, and you'll need to <code>ln -s /Library/Frameworks/Python.framework/Versions/2.7/bin/python /usr/bin/python2.7</code></li></ul>

<b>Setuptools 0.6c11 and EasyInstall</b> (you may already have this; try running "easy_install" or "easy_install-2.7" to check)<br>
<ul><li>All platforms:  <a href='http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e'>Download</a>, then <code>tar xvfz</code> and <code>sudo python2.7 setup.py install</code>.<br>
</li><li>Ubuntu: <code>sudo apt-get install python-setuptools</code></li></ul>

<b>Mercurial</b> — for revision control (you may already have this; try running "hg" to check)<br>
<ul><li>All platforms: Download from <a href='http://mercurial.selenic.com/'>http://mercurial.selenic.com/</a> and install.</li></ul>

<b>PIL 1.1.7</b> — optional, only needed if you want to test photo uploading locally<br>
<ul><li>All platforms: <a href='http://effbot.org/downloads/Imaging-1.1.7.tar.gz'>Download</a> then <code>tar xvfz</code> and <code>sudo python2.7 setup.py install</code>.<br>
</font></li></ul>

<b>Latest App Engine SDK for Python</b>
<ul><li>All platforms:  Download the <b>Linux</b> zip file (regardless of your platform) from  <a href='http://googleappengine.googlecode.com/files/google_appengine_1.8.8.zip'>google_appengine_1.8.8.zip</a>  and unzip in your home directory.</li></ul>

<b>py.test</b> — for running unit tests<br>
<ul><li>All platforms: <code>sudo easy_install-2.7 pytest</code></li></ul>

<b>Gettext</b> — for internationalization<br>
<ul><li>Linux: <code>sudo apt-get install gettext</code>
</li><li>Mac OS 10.7: <a href='http://www.ellert.se/PKGS/gettext-0.18.1.1/10.7/gettext.pkg.tar.gz'>Download</a>, double-click, and install.<br>
</li><li>Mac OS 10.8: <a href='http://www.ellert.se/PKGS/gettext-0.18.1.1-u/10.8/gettext.pkg.tar.gz'>Download</a>, double-click, and install.</li></ul>

<br>
<h2>Step 2. Get the code</h2>

<ul><li>Make a local clone of the code repository with this command.  (This assumes you want to put the code in a directory called <code>pf</code>:<br>
<blockquote><code>hg clone https://googlepersonfinder.googlecode.com/hg pf</code></blockquote></li></ul>

<ul><li>Create a .hgrc file in your HOME directory (or on a Windows system in %USERPROFILE%\Mercurial.ini)  containing the following 2 lines:<br>
<blockquote><code>[ui]</code> <br>
<code>username = John Doe &lt;john@example.com&gt;</code></blockquote></li></ul>

Questions about Mercurial?  Check out the <a href='http://mercurial.selenic.com/wiki/QuickStart'>quickstart guide</a>.<br>
<br>
<br>
<h2>Step 3. Initialize the data in the app</h2>

All the following commands should be done from the application directory (the <code>pf</code> directory we created in the previous step).<br>
<br>
<blockquote><code>cd pf</code></blockquote>

In one terminal, start a local server with this command:<br>
<br>
<blockquote><code>tools/gae run app</code> <font color='#ccc'># Brings up a local dev_appserver, serving on localhost:8000 by default</font></blockquote>

With the app server running, open a separate terminal and enter this command:<br>
<br>
<blockquote><code>tools/console :8000 -c 'setup_datastore()'</code> <font color='#ccc'># Connects to localhost:8000 and executes setup_datastore()</font></blockquote>

This will connect to your app and create a few example repositories such as "haiti" and "japan".<br>
<br>
<br>
<br>
<h2>Step 4. Try the app!</h2>

Now you should be able to use the app by going to <a href='http://localhost:8000/'>http://localhost:8000/</a> in a browser, where you'll see the repositories listed on the left.<br>
<br>
You can also run tests like this:<br>
<blockquote><code> tools/all_tests </code></blockquote>

You may see some warning about the version of Python but it is okay to ignore it now.<br>
<br>
If you would like to contribute code, please see <a href='HowToDevelop.md'>HowToDevelop</a>.<br>
<br>
<br>
<br>
<h2>Step 5. (optional) Set up additional repositories</h2>

Person Finder usually has one repository per crisis incident.  Each repository can be customized with a title, set of languages, announcements, and other settings.<br>
<br>
To create a new repository, go to the administration page at <code>http://localhost:8000/haiti/admin</code> and next to "Select a repository" choose "Create new...", then fill in the box with a new repository identifier and click Create.  You can then edit the settings page for your newly created repository and click "Save these settings" to save your edits.<br>
<br>
If you would like to be able to read and write data in your new repository through the Person Finder API, you will need to create an API key, which you can do at <code>http://localhost:8000/</code><font color='#800'><var>repo</var></font><code>/admin/api_keys</code> (replace <font color='#800'><var>repo</var></font> with your repository identifier).<br>
<br>
<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>