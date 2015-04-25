| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/UserInterface'>direct link</a>).</font>

### Design ###

This app has a simple purpose: to **provide a coordination point** for each missing person, where all the people who have or seek information about that person can communicate.

The main UI flow goes like this:

> ![https://sites.google.com/site/zestyping/dropbox/person-finder-ui-flow.png](https://sites.google.com/site/zestyping/dropbox/person-finder-ui-flow.png)

From the very beginning of the Person Finder project, we decided on a few notable design points:

  * **Users make a clear choice between seeking or providing information** before doing anything else.  The prominence of this decision was motivated by past experience with missing person databases for September 11 and Hurricane Katrina.  We learned that it was common for users to be confused about whether they were registering a person they sought, or registering a person they had found.  Sometimes this would cause serious problems: a user would enter a record for a person they were looking for, then search and find the record they had just entered, leading them to incorrectly believe the person was found safe.  We wanted to avoid this.

  * **A search always takes place before data entry**, regardless of whether the user is seeking or providing information.  During past incidents, duplicate records were common.  We wanted to maximize the chance that people looking for the same person, or having information about the same person, would all converge on the same record and get in touch with each other.  So we require the user to look at potential duplicates before creating a new record.

  * **Information is divided into identifying information and status information** by the two-column layout of the pages for viewing and entering information.  The two kinds correspond to Person records and Note records in PFIF.  This division reflects the differing nature and use of the information:
    * Identifying information is fixed, likely to be known by those seeking, useful **for converging** on the correct record (e.g. hometown)
    * Status information is changing, not likely to be known by those seeking, useful **after having converged** on the correct record (e.g. current location)

<br>
<h3>Rendering</h3>

All pages are subclassed from <code>utils.Handler</code>, which contains some convenience methods and an <code>initialize</code> method that runs on every request.  The <code>initialize</code> method sets up <code>self.env</code>, a dictionary containing global configuration variables, and <code>self.params</code>, a dictionary containing parsed query parameters from the URL.  Some of the variables in <code>env</code> are specific to the subdomain, and others are application-wide.  The parsing of the query parameters is controlled by the <code>auto_params</code> dictionary.<br>
<br>
The pages are all rendered from Django HTML templates in the <code>app/templates</code> directory, and should be rendered by a call to <code>utils.Handler.render</code>, which passes in the <code>env</code> and <code>params</code> parameters.<br>
<br>
Note that all substituted strings in Django templates have to be manually escaped.  (We're using Django 0.96, so we don't get the autoescaping features of newer Django versions.)  This means inserting <code>|escape</code> after every template parameter, like this: <code>{{first_name|escape}}</code>.  Use <code>|escape</code> liberally; always add <code>|escape</code> unless you know you have a specific need to do otherwise.  To facilitate security reviews, please keep to the following convention for template variables:<br>
<ul><li>Variable names should end in <code>_html</code> if they are known to contain safe HTML.<br>
</li><li>Variable names should end in <code>_js</code> if they are known to contain safe JavaScript.<br>
</li><li>Date variables should be formatted with <code>|date</code>.<br>
</li><li>Boolean variables should be formatted with <code>|yesno</code>.<br>
</li><li>All other variables should be escaped with <code>|escape</code> regardless of whether you think they are safe or not.</li></ul>

Specifying the <code>small=yes</code> query parameter produces a miniature version of the UI intended for embedding (with <code>&lt;iframe&gt;</code>) on other sites.<br>
<br>
All of the stylesheets are in static files in the <code>app/static</code> directory.<br>
<br>
<br>
<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>