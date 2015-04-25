| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/HowToDevelop'>direct link</a>).</font>


We use Mercurial (hg) for revision control.  If you're new to Mercurial, try the tutorial at http://hginit.com/.  Mercurial is a distributed RCS, which means that your local machine gets a complete copy of the repository with all its history, and you can commit changes locally before pushing them to the main repository.

<br>

<b>Note:</b> If you are working from a specific release branch (instead of the default branch), <font color='#0a0'>follow the instructions in green and replace "releasebranch" with the release branch name</font>.<br>
<br>
<br>

<h3>Making local changes</h3>

Before you start making a new set of changes:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='350'><tt>hg pull -u</tt> <font color='#999'>or</font> <tt><font color='#0a0'>hg pull; hg update releasename</font></tt></td>
<td><font color='#999'># Brings your local repository up to date</font></td>
</tr>
<tr>
<td width='30'></td>
<td><tt>hg branch <font color='#c00' face='arial' size='2'><i>username</i></font>-<font color='#c00' face='arial' size='2'><i>feature</i></font></tt></td>
<td><font color='#999'># Makes a new branch for your changes</font></td>
</tr>
</table>

Your branch name should consist of your username, a hyphen, and a short identifier that describes your change.<br>
<br>
Now you can write code, edit, test, etc.  If you are adding or removing files, use <code>hg add</code> or <code>hg rm</code>.  If you are moving content from one file to another, use <code>hg cp</code> or <code>hg mv</code>.  The <code>hg status</code> command will show which files you have modified.<br>
<br>
<br>
<h3>Testing your changes</h3>

There are two kinds of tests.  When you make a significant change, please add tests for it (see <a href='HowToTest.md'>HowToTest</a> for details).<br>
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
<br>
<h3>Merging in changes from others to prepare for code review</h3>

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

Other changes can continue to happen on the default branch while you are working.  So, you'll need to merge in these changes before you do the final round of testing.  To merge in these changes:<br>
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
<td><tt>hg merge default</tt> <font color='#999'>or</font> <font color='#0a0'><tt>hg merge releasename</tt></font></td>
<td><font color='#999'># Merges changes from the default (or release) branch into your branch </font></td>
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
If you have changed or added messages in the UI, <code>hg merge</code> may ask you to resolve conflicts between all the 90+ message files.  To solve this problem:<br>
<br>
<ul><li>First back out your incomplete merge with <tt>hg update -C <font color='#c00' face='arial' size='2'><i>username</i></font>-<font color='#c00' face='arial' size='2'><i>feature</i></font></tt>, and remove any stray files from the incomplete merge<br>
</li><li><code>for i in app/locale/*/*/django*; do hg cat -r releasename $i &gt; $i; done</code> <font color='#999'># Copy all the message files from release-branch into your branch</font>
</li><li>If you added translations in other languages, <code>hg revert</code> those .po files with your new translations.<br>
</li><li><code>hg commit -m "Merge with messages from releasename"</code>
</li><li><code>hg merge releasename</code></li></ul>

After merging, rerun your tests to make sure merge was fine.<br>
<br>
<br>



<h3>Requesting a code review</h3>

When you have code that is tested and works, request a code review by running the <code>rietveld</code> script like this:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td><tt>tools/rietveld <font color='#c00' face='arial' size='2'><i>reviewer_list</i></font> <font color='#c00' face='arial' size='2'><i>optional_cc_list</i></font></tt></td>
</tr>
<tr>
<td width='30'></td>
<td><tt><font color='#0a0'>tools/rietveld-releasename <font color='#c00' face='arial' size='2'><i>reviewer_list</i></font> <font color='#c00' face='arial' size='2'><i>optional_cc_list</i></font></font></tt></td>
</tr>
</table>

(<font color='#c00' face='arial' size='2'><i>reviewer_list</i></font> and <font color='#c00' face='arial' size='2'><i>optional_cc_list</i></font> are lists of e-mail addresses separated by commas.)<br>
<br>
At some point, it will ask for a user and password, just leave them both empty and it will go through.<br>
<br>
<b>Note:</b> If you are asked to enter "Password for --send_mail", make sure there is a .email file in your home directory with the account you used to sign into code.google.com.<br>
<br>
This will produce a diff from the default branch to your branch and upload it to <a href='http://codereview.appspot.com'>Rietveld</a>, an open-source review tool.  The reviewer or reviewers will receive e-mail from you directing them to a page where they can browse your changes and make comments, and everyone can send comments back and forth.<br>
<br>
If your reviewer asks you to make some changes, you can do those changes locally, run the tests again, and then run <code>rietveld</code> again.  This will update the existing code review with a new patch.<br>
<br>
You can have multiple branches in progress in your local repository, if you need to, and switch among them with <code>hg update</code>.  Each time you run <code>rietveld</code>, it will detect the branch you are working in, and will either create a new code review or update the existing code review.<br>
<br>
<br>

<h3>Code has been reviewed and is ready to be added to default branch</h3>

When your reviewer approves the changes, then you need to send your change to the reviewer which will incorporate it in the default branch.<br>
<br>
<b>If you do NOT have developer permission for this project</b>, create a <code>bundle</code> of your changes like this:<br>

<table border='0'>
<tr>
<td width='30'></td>
<td width='480'><tt>hg outgoing</tt></td>
<td><font color='#999'># shows changeset which are not in default branch </font></td>
</tr>
<tr>
<td width='30'></td>
<td width='580'><tt>hg bundle -r your_branch_name --base default your_filename.hg</tt></td>
<td><font color='#999'># creates a compressed changegroup file with these changesets</font></td>
</tr>
<tr>
<td width='30'></td>
<td width='580'><font color='#0a0'><tt>hg bundle -r your_branch_name --base releasename your_filename.hg</tt></font> </td>
<td><font color='#999'># creates a compressed changegroup file with these changesets</font></td>
</tr>
</table>

Then e-mail <code>your_filename.hg</code> to your code reviewer, who will incorporate your changes into the <code>default</code> branch.<br>
<br>
Then you can update and return to the default/release branch like this:<br>
<br>
<table border='0'>
<tr>
<td width='30'></td>
<td width='350'><tt>hg update default</tt> <font color='#999'>or</font> <tt><font color='#0a0'>hg update releasename</font></tt></td>
<td><font color='#999'># Switches back to the default/release branch</font></td>
</tr>
<tr>
<td width='30'></td>
<td width='250'><tt>hg pull -u</tt></td>
<td><font color='#999'># Pulls down updates from the main repository</font></td>
</tr>
</table>

<b>If you do have developer permission for this project</b>, use <code>hg push -f</code> to push your branch into the main repository.  Your reviewer will then merge the change into the default branch.<br>
<br>
<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>