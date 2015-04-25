| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DeveloperFaq'>direct link</a>).</font>


### How do I safely delete Person entities? ###

Because Person entities can have associated Note and Photo entities, it's not safe to just call Person.delete() in the console.  Instead, go to the `/admin` page of the app and use the deletion form there.

### The app says "There was an error processing your request".  What do I do? ###

If you're running a local development appserver, check the console for error messages.  If you're running on appspot.com, go to your application dashboard at http://appspot.com/ and check the "Logs" page for error messages.

### The app crashed with NeedIndexError.  What do I do? ###

This means that either an index definition is missing from app/index.yaml, or the index is defined but isn't built yet.  Go to your application dashboard at http://appspot.com/ and check the "Datastore Indexes" page.  All the indexes should be "Serving"; if they are still "Building" then you just have to wait.  Unfortunately this can take a long time (hours in some cases).

### tools/gae run app returns "Could not find google\_appengine directory.  Please set APPENGINE\_DIR." ###

This means that it can not find where you installed appengine.
[common.sh](http://code.google.com/p/googlepersonfinder/source/browse/tools/common.sh) is looking into you HOME directory or in a env variable $APPENGINE\_DIR to find google\_appengine but could not find it.
When installing appengine, make sure to unzip it into your home directory.


### hg commit says "No username found" ###
You need to create a .hgrc file. See the Mercurial [quickstart guide](http://mercurial.selenic.com/wiki/QuickStart).

### hg commit says "transaction abort!" ###
This means the commit did not go through. When you commit, Mercurial brings up an editor for you to enter a commit message. This message is required. Beware that Mercurial ignores the lines beginning with `HG:` when looking for your message, so do not type `HG:` in front of your message.

### hg produces errors about hgext.hbisect and hgext.imerge ###
If you get the following errors:
> `failed to import extension hgext.hbisect: No module named hbisect`<br>
<blockquote><code>failed to import extension hgext.imerge: No module named imerge</code></blockquote>

These used to be extensions, but are now built-in commands.  Check these files:<br>
<blockquote><code>~/.hgrc</code><br>
<code>/etc/mercurial/hgrc</code><br>
<code>/etc/mercurial/hgrc.d/hgext.rc</code></blockquote>

and remove any lines that try to load the <code>hbisect</code> and <code>imerge</code> extensions.  Still not working?  Check the<br>
<a href='http://mercurial.808500.n3.nabble.com/failed-to-import-error-warning-td799350.html'>Mercurial forum</a>.<br>
<br>
<h3>tools/rietveld produces error messages</h3>
The <code>rietveld</code> script can fail for following reasons:<br>
<ul><li>the EDITOR env variable is not set<br>
</li><li>Description longer than 100 characters<br>
</li><li>Description contains a <code>"</code> character</li></ul>

Make sure your EDITOR env variable is set (echo $EDITOR). If not set it through export EDITOR=emacs.<br>
It will allow you to edit your description when running rietveld if the description was longer than 100 characters or if it contained a bad character.<br>
<br>
After a failure related to long description or bad character, subsequent runs of <code>rietveld</code> will fail with errors such as:<br>
<blockquote><code>Usage: -c [options] [-- diff_options]</code><br>
<code>-c: error: option -i: invalid integer value: 'aliceb-translation'</code></blockquote>

To go back to a clean state, you have to remove the broken line from the file <code>.codereview_issues</code> in your home directory.<br>
<br>
<h3>Unittests failed to launch</h3>
If Error is '<code>tools/unit_tests: line 7: nosetests: command not found</code>. It means you did not install <b>Nose</b> for running unittests. Install it using  <code>sudo easy_install nose</code>.<br>
<br>
<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>