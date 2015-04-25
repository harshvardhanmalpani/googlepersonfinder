| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/Internationalization'>direct link</a>).</font>


### Language codes and locale codes ###

Person Finder follows the Django convention for "language code" versus "locale code".  A **language code** is a lowercase ISO 639-1 language code, optionally followed by a _hyphen_ and an uppercase ISO 3166-1 two-letter country code.  A **locale code** is like a language code except that it uses an _underscore_ instead of a hyphen.  The use of `locale` and `lang` for variable and function names in Person Finder should follow this convention.

<br>
<h3>Selecting the display language</h3>

Setting the <code>lang</code> query parameter to a <i>language code</i> sets the display language (on any page).  The language code is also saved in a browser cookie, which determines the language when there is no <code>lang</code> parameter.<br>
<br>
<br>
<h3>Translated messages</h3>

Localized messages are stored in <code>app/locale</code> in a directory named after the <i>locale code</i>, in <code>.po</code> format.  For example, French messages are in <code>app/locale/fr/LC_MESSAGES/django.po</code>.  These <code>.po</code> files are compiled into <code>.mo</code> files, which are used at runtime.<br>
<br>
Whenever you change strings in the code, you should run <code>tools/update_messages</code>, which will scan the Python code and all the Django templates for strings, update the <code>.po</code> files with new strings, compile them into the appropriate <code>.mo</code> files, and then print a report listing the messages that have missing translations in each language.  In general, you will rarely need to run <code>tools/update_messages</code> directly, because running the tests with <code>tools/server_tests</code> automatically runs <code>tools/update_messages</code>.<br>
<br>
<br>
<h3>Adding a new language</h3>

Take the following steps to add a new language:<br>
<ul><li>Important: stop any local running appservers<br>
</li><li>Run <code>tools/update_messages</code>
</li><li>Create a new directory for the language at <code>app/locale/</code><font color='#a00'><i>locale_code</i></font><code>/LC_MESSAGES</code>
</li><li>Copy <code>app/locale/en/LC_MESSAGES/django.po</code> into your new directory<br>
</li><li>Edit this new <code>django.po</code> file to add the translated messages for the new language<br>
</li><li>Run <code>tools/update_messages</code> again to compile and convert the new translated messages<br>
</li><li>Add the new language to <code>LANGUAGE_ENDONYMS</code> and <code>LANGUAGE_EXONYMS</code> in <code>app/utils.py</code>
</li><li>Add the new language to the <code>lang-test</code> subdomain in <code>tools/setup.py</code>
</li><li>Run the tests as explained in <a href='HowToDevelop.md'>HowToDevelop</a>
</li><li>Run <code>tools/gae run app</code> and then go to <code>http://localhost:8080/?subdomain=lang-test</code> to try out the new language<br>
</li><li>If everything looks good, run <code>hg add</code> to add your new message files, commit, and request a code review</li></ul>

<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>