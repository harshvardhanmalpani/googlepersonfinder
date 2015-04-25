<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/RepositoryFeed'>direct link</a>).</font>




The Person Finder application publishes a list of its available repositories in an Atom feed.  You can use this feed to automatically detect when a repository is launched or shut down.

<br>

<h3>Feed URL</h3>

The global repository feed is available at:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/global/feeds/repo</code></blockquote>

There are also individual feeds for each repository, available at:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/repo</code></blockquote>

All these feeds are in Atom format.  The global feed has one Atom entry for each active repository; the feed for a specific repository has just the one entry for that repository.<br>
<br>
The Atom entries contain custom elements, described below, that use the XML namespace URI <code>http://schemas.google.com/personfinder/2012</code> (referenced using the short prefix <code>gpf</code>).<br>
<br>
When a new repository is launched, a new entry appears in this feed.  When a repository is shut down, its entry disappears from this feed.<br>
<br>
<br>

<h3>Entry details</h3>

Each Atom entry contains the following standard Atom elements:<br>
<br>
<ul><li>The <code>&lt;id&gt;</code> element contains the URL to the repository's starting page, which is usable as a unique identifier for the repository.<br>
</li><li>The <code>&lt;title&gt;</code> element contains the displayed title of the repository in its default language.  The element also has an <code>xml:lang</code> attribute identifying the repository's default language.<br>
</li><li>The <code>&lt;published&gt;</code> element contains the date and time that the repository was first publicly listed as an active repository.<br>
</li><li>The <code>&lt;updated&gt;</code> element contains the date and time that the repository's activation state or test mode state last changed. It is initially the same as <code>&lt;published&gt;</code>, but, for example, if a repository first started in test mode, then switched to real mode, this element would contain the date and time of the switch.</li></ul>

The <code>&lt;content&gt;</code> of the Atom entry contains a single <code>&lt;gpf:repo&gt;</code> element with the following child elements:<br>
<br>
<ul><li>There are one or more <code>&lt;gpf:title&gt;</code> elements containing the displayed title of the repository in each available language.  Each <code>&lt;gpf:title&gt;</code> element has an <code>xml:lang</code> attribute identifying the language.<br>
</li><li>The <code>&lt;gpf:read_auth_key_required&gt;</code> element contains the string <code>true</code> if an API key is required to read records through the API.<br>
</li><li>The <code>&lt;gpf:search_auth_key_required&gt;</code> element contains the string <code>true</code> if an API key is required to make search queries through the API.<br>
</li><li>The <code>&lt;gpf:location&gt;</code> element contains a GeoRSS point specifying the approximate location of the incident.  (A GeoRSS point is a <code>&lt;georss:point&gt;</code> containing the latitude, then a space, then the longitude.)<br>
</li><li>The <code>&lt;gpf:test_mode&gt;</code> element contains the string <code>true</code> if the repository is in test mode.  In test mode, records that are more than 6 hours old are automatically deleted.