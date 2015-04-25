| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/Launching'>direct link</a>).</font>

Here's how to launch Person Finder on your own site.  (Google runs this code at http://google.org/personfinder but you can also run your own completely independent Person Finder site.)

<br>
<h2>Step 1. Get the code</h2>

Follow the steps at GettingStarted to get the code.<br>
<br>
<br>
<h2>Step 2. Create your application on App Engine</h2>

If you're not already signed up for App Engine, go to <a href='https://appengine.google.com/'>https://appengine.google.com/</a> and sign up, using a Google account.<br>
<br>
Then, at <a href='http://appengine.google.com/'>http://appengine.google.com/</a>, click the "Create Application" button, choose an identifier for your application, and follow the instructions.  In the rest of this page below, APPID represents the application identifier you chose.<br>
<br>
<br>
<h2>Step 3. Deploy your code</h2>

Run this command in your application directory:<br>
<br>
<blockquote><code>tools/gae update app -A APPID</code> <font color='#ccc'># Deploys your code to the application named APPID</font></blockquote>

You'll be asked for your Google username and password, and in a few minutes, the current version of the code on your computer will be installed and running on Google App Engine.<br>
<br>
<br>
<h2>Step 4. Create an instance</h2>

Run this command in your application directory:<br>
<br>
<blockquote><code>tools/console APPID.appspot.com</code> <font color='#ccc'># Connects to the application named APPID</font></blockquote>

Person Finder can run multiple repositories (for example, if there are multiple crises, a single website running Person Finder can contain a separate database for each crisis).  Choose a name for your new repostiory.  For example, if you choose "abc", then your site will be available at "APPID.appspot.com/abc".  At the Python prompt, type:<br>
<br>
<blockquote><code>&gt;&gt;&gt; Repo(key_name='REPO').put()</code> <font color='#ccc'># Create a repository named REPO</font></blockquote>

<br>
<h2>Step 5. Visit your new site</h2>

Visit <a href='http://APPID.appspot.com/REPO/'>http://APPID.appspot.com/REPO/</a> to see your new site in action!<br>
<br>
Visit <a href='http://APPID.appspot.com/REPO/admin'>http://APPID.appspot.com/REPO/admin</a> to adjust the settings for your repository.<br>
<br>
<br>
<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>