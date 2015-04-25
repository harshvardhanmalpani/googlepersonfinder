<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DeveloperGuideGHC11'>direct link</a>).</font>




# Getting Started #

You can develop on Linux, or Mac OS, or Windows-with-Cygwin.

## Step 1. Get tools ##

You will probably be happiest if you do these steps in order.

**Python 2.5.x or 2.6.x** (your system may already have this; try running "python" or "python2.5" to check)
  * All platforms: [Download here](http://www.python.org/download/releases/2.5.6) and install
  * Mac OS X: the pre-installed Python binaries are at /System/Library/Frameworks/Python.framework/Versions/2.x/bin/python2.x and are symlinked from /usr/bin/python2.x.  If you downloaded and installed a new version, it will be in /Library/Frameworks rather than /System/Library/Frameworks, and you'll need to `ln -s /Library/Frameworks/Python.framework/Versions/2.5/bin/python /usr/bin/python2.5`

**Setuptools 0.6c11 and EasyInstall** (your system may already have this; try running "easy\_install" or "easy\_install-2.5" to check)
  * All platforms:  [Download](http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e), then `tar xvfz` and `sudo python2.5 setup.py install`.

<font color='#777'>
<b>PIL 1.1.7</b> — optional, only needed if you want to test photo uploading locally<br>
<ul><li>All platforms: <a href='http://effbot.org/downloads/Imaging-1.1.7.tar.gz'>Download</a> then <code>tar xvfz</code> and <code>sudo python2.5 setup.py install</code>.<br>
</li><li>If you have trouble installing PIL 1.1.7 with Python 2.5.2, try switching to Python 2.5.4.<br>
</font></li></ul>

**App Engine SDK 1.5.2 or higher  (but not 1.6) for Python**
  * All platforms:  Download the **Linux** zip file (regardless of your platform) from  [google\_appengine\_1.5.4.zip](http://googleappengine.googlecode.com/files/google_appengine_1.5.4.zip)  and unzip in your home directory.

**Nose** — for running unit tests
  * All platforms: `sudo easy_install-2.5 nose`

**Mercurial 1.6.4** — for revision control
  * Linux: [Download](http://mercurial.selenic.com/release/mercurial-1.6.4.tar.gz), then `tar xvfz` and `sudo make install`.
  * Mac OS 10.5: [Download](http://mercurial.berkwood.com/binaries/Mercurial-1.6.4-py2.5-macosx10.5.zip), double-click, and install.
  * Mac OS 10.6: [Download](http://mercurial.berkwood.com/binaries/Mercurial-1.6.4-py2.6-macosx10.6.zip), double-click, and install.

**Gettext** — for internationalization
  * Linux: `sudo apt-get install gettext`
  * Mac OS 10.5: [Download](http://www.ellert.se/PKGS/gettext-0.17-u/10.5/gettext.pkg.tar.gz), double-click, and install.
  * Mac OS 10.6: [Download](http://www.ellert.se/PKGS/gettext-0.17-u/10.6/gettext.pkg.tar.gz), double-click, and install.
  * Mac OS 10.7: [Download](http://www.ellert.se/PKGS/gettext-0.18.1.1/10.7/gettext.pkg.tar.gz), double-click, and install.

## Step 2. Get the code ##

  * Make a local clone of the code repository with this command. First create a separate local directory to hold code, for example, a directory called "pf" (henceforth referred to as the "application directory"):
> > `mkdir pf` <br>
<blockquote><code>hg clone https://googlepersonfinder.googlecode.com/hg pf</code></blockquote></li></ul>

<ul><li>Create a .hgrc file in your HOME directory (or on a Windows system in %USERPROFILE%\Mercurial.ini)  containing the following 2 lines:<br>
<blockquote><code>[ui]</code> <br>
<code>username = Yourfirstname Yourlastname &lt;youremailaddress&gt;</code></blockquote></li></ul>

Questions about Mercurial?  Check out the [quickstart guide](http://mercurial.selenic.com/wiki/QuickStart).

## Step 3. Initialize the data in the app ##

All the following commands should be done from the application directory (the `pf` directory we created in the previous step).


> `cd pf`

In one terminal, start a local server with this command:

> `tools/gae run app` <font color='#ccc'># Brings up a local dev_appserver, serving on localhost:8000 by default</font>

With the app server running, open a separate terminal and connect to the app's datastore with the command:

> `tools/console` <font color='#ccc'># Connects to localhost port 8000 by default</font>

At the Python prompt that appears, enter this command to set up the datastore:

> `>>> setup_datastore()`

## Step 4. Try the app! ##

Now you should be able to use the app by going to http://localhost:8000/ in a browser.

You can also run tests like this:
> ` tools/all_tests `

You may see some warning about the version of Python but it is okay to ignore it now.

If you would like to contribute code, please see [GHC11 How To Develop](DeveloperGuideGHC11#How_To_Develop.md).

## Step 5. (optional) Configure your instance ##

The Person Finder application can run several instances.  There is usually one instance per current crisis. Each instance can be customized with a list of interface languages, announcements, and so on.

**How to create a new instance**

When running on localhost, you can create a new instance by  adding a subdomain to the  python configuration file: `tools/setup.py`

If your application is deployed on appengine, you can access to an admin UI at `http://yourapplication.appspot.com/admin`

| [Top](DeveloperGuideGHC11.md) |
|:------------------------------|

# How To Develop #

We use Mercurial (hg) for revision control.  If you're new to Mercurial, try the tutorial at http://hginit.com/.  Mercurial is a distributed RCS, which means that your local machine gets a complete copy of the repository with all its history, and you can commit changes locally before pushing them to the main repository.

## Making local changes ##

Before you start making a new set of changes:

<table border='0'>
<tr>
<td width='30'></td>
<td width='350'><tt>hg pull; hg update ghc-dev</tt></td>
<td><font color='#999'># Brings your local repository up to date to the ghc-dev release branch</font></td>
</tr>
<tr>
<td width='30'></td>
<td><tt>hg branch <font color='#c00' face='arial' size='2'><i>username</i></font>-<font color='#c00' face='arial' size='2'><i>feature</i></font></tt></td>
<td><font color='#999'># Makes a new branch for your changes</font></td>
</tr>
</table>
Your branch name should consist of your username, a hyphen, and a short identifier that describes your change.

Now you can write code, edit, test, etc.  If you are adding or removing files, use `hg add` or `hg rm`.  If you are moving content from one file to another, use `hg cp` or `hg mv`. <br>
You can see the files your modified through <code>hg status</code>.<br>
<br>
<h2>Testing your changes</h2>

There are two kinds of tests.  When you make a significant change, please add tests for it (see <a href='HowToWriteTests.md'>HowToWriteTests</a> for details).<br>
<br>
Run the unit tests with this command:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='250'><tt>tools/unit_tests</tt></td>
<td><font color='#999'># Takes about 3 seconds </font></td>
</tr>
</table>

Run the system tests with this command:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='250'><tt>tools/server_tests</tt></td>
<td><font color='#999'># Starts the app server on port 8081 and makes requests to it</font></td>
</tr>
<tr>
<td></td><td><font color='#999'># Takes about 3 minutes</font></td>
</tr>
</table>

You can also run all the tests with <code>tools/all_tests</code>.<br>
<br>
<h2>Merging in changes from others to prepare for code review</h2>

You can first look at your changes:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='250'><tt>hg status</tt></td>
<td><font color='#999'># Lists all files modified, created, removed.</font></td>
</tr>
<tr>
<td><tt>hg diff</tt></td>
<td><font color='#999'># Display diffs on all modified files.</font></td>
</tr>
</table>

Other changes can continue to happen on the ghc-dev branch while you are working.  So, you'll need to merge in these changes before you do the final round of testing.  To merge in these changes:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='350'><tt>hg commit</tt></td>
<td><font color='#999'># Commits your pending changes locally.</font></td>
</tr>
<tr>
<td><tt>hg pull</tt></td>
<td><font color='#999'># Pulls down any new changes from the main repository to your local repository</font></td>
</tr>
<tr>
<td><tt>hg merge ghc-dev</tt></td>
<td><font color='#999'># Merges changes from the ghc-dev branch into your branch </font></td>
</tr>
<tr>
<td><tt>hg commit</tt></td>
<td><font color='#999'># Commits the merge locally on your branch </font></td>
</tr>
</table>

<code>hg commit</code> will bring up an editor for you to enter a commit message.  If you don't enter a commit message, the commit will be cancelled.<br>
<br>
The <code>merge</code> command operates on two committed changesets (which is why you have to commit your local changes first) and produces a new changeset (which you then have the opportunity to inspect before committing).<br>
<br>
After merging, rerun your tests to make sure merge was fine.<br>
<br>
<h2>Requesting a code review</h2>

When you have code that is tested and works, request a code review by running the <code>rietveld</code> script like this:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td><tt>tools/rietveld-ghc <font color='#c00' face='arial' size='2'><i>reviewer</i></font></tt></td>
</tr>
</table>


(<font color='#c00' face='arial' size='2'><i>reviewer</i></font> should be the Google contact listed on the bug/issue you are working on. You may specify more than one reviewer by separating email addresses with commas.)<br>
<br>
At some point, it will ask for a user and password, just leave them both empty and it will go through.<br>
<br>
<b>Note:</b> If you are asked to enter "Password for --send_mail", make sure there is a .email file in your home directory with the account you used to sign into code.google.com.<br>
<br>
This will produce a diff from the ghc-dev branch to your branch and upload it to <a href='http://codereview.appspot.com'>Rietveld</a>, an open-source review tool.  The reviewer or reviewers will receive e-mail from you directing them to a page where they can browse your changes and make comments, and everyone can send comments back and forth.<br>
<br>
If your reviewer asks you to make some changes, you can do those changes locally, run the tests again, and then run <code>rietveld</code> again.  This will update the existing code review with a new patch.<br>
<br>
You can have multiple branches in progress in your local repository, if you need to, and switch among them with <code>hg update</code>.  Each time you run <code>rietveld</code>, it will detect the branch you are working in, and will either create a new code review or update the existing code review.<br>
<br>
<h2>Code has been reviewed and is ready to be added to ghc-dev branch</h2>

When your reviewer approves the changes, Then you need to send your patch to the reviewer which will incorporate it in the ghc-dev branch. For this, you need to create a <code>bundle</code> of your code using <br>

<table border='0'>
<tr>
<td width='10'></td>
<td width='480'><tt>hg outgoing</tt></td>
<td><font color='#999'># shows changeset which are not in ghc-dev branch </font></td>
</tr>
<tr>
<td width='10'></td>
<td width='580'><tt>hg bundle -r your_branch_name --base ghc-dev your_filename.hg</tt></td>
<td><font color='#999'># creates a compressed changegroup file with these changesets</font></td>
</tr>
</table>

Send <code>your_filename.hg</code> by email to the Google contact on the issue (i.e., your code reviewer) which will incorporate them into the ghc-dev branch.<br>
<br>
Then you can update and return to the ghc-dev branch like this:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='350'><tt>hg update ghc-dev</tt></td>
<td><font color='#999'># Switches back to the ghc-dev branch</font></td>
</tr>
<tr>
<td width='30'></td>
<td width='250'><tt>hg pull -u</tt></td>
<td><font color='#999'># Pulls down updates from the main repository</font></td>
</tr>
</table>

<h1>Useful Links</h1>

<a href='DeveloperGuideGHC11#Getting_Started.md'>Up to Getting Started</a>

<a href='DeveloperGuideGHC11#How_To_Develop.md'>Up to Developer Guide</a>

<a href='http://goo.gl/uvCXK'>Person Finder Codeathon Overview</a>

<a href='https://docs.google.com/spreadsheet/ccc?key=0AjdS3uyq0XmUdC1kMUlIRHZNdTVETnBaUGQyQ25FWVE#gid=0'>Bug Spreadsheet</a>

<a href='http://ghc-dev.appspot.com'>Development Instance</a>

<a href='http://zesty.ca/pfif/1.3'>PFIF 1.3</a>