| [« back to DeveloperGuide](DeveloperGuide.md) |
|:-----------------------------------------------|

<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DataModel'>direct link</a>).</font>



### PFIF entities (person and note) ###

The data model is defined in `app/model.py`.

The schema for storing information about missing people closely follows the [PFIF 1.2](http://zesty.ca/pfif) model.

Each person corresponds to a `Person` entity (which has a set of fields defined in PFIF 1.2).  Associated with each `Person` entity, there can be any number of `Note` entities (whose fields are also defined in PFIF 1.2).

The database is partitioned according to **repository**.  For example, `person-finder.appspot.com/foo` and `person-finder.appspot.com/bar` will look and behave like two separate instances of Person Finder, each with their own separate database.  But, it is really just a single application, where all the `Person` and `Note` entities have a `repo` field and all queries filter on the repository.

Both `Person` and `Note` entities have unique record IDs, as described in PFIF.  The repository name and the record IDs are used together to form the key names of the App Engine entities.  The common logic concerned with record IDs and repositories is implemented in the `Base` class, from which both `Person` and `Note` are derived.

<br>
<h3>Other entities</h3>

We also keep a few other kinds of entities in the datastore.<br>
<br>
<b><code>Repo</code></b> entities don't contain anything.  There's one for each repository, and it exists to make the repositories appear in administrative menus.<br>
<br>
<b><code>UniqueId</code></b> entities also don't contain anything.  We create one (and use its numeric ID) whenever we want to generate a unique identifier.<br>
<br>
<b><code>Photo</code></b> entities store the binary image data of uploaded photos.  Like <code>Person</code> and <code>Note</code> entities, Photo entities are also partitioned by repository.  They're referenced in the <code>photo</code> properties of <code>Person</code> entities.<br>
<br>
<b><code>Authorization</code></b> entities control access to the data through the feeds and the read/write API.  Clients of the API have to specify an authorization token.  Each <code>Authorization</code> entity specifies what powers are associated with a given authorization token.<br>
<br>
<b><code>Secret</code></b> entities are for cryptographic keys.  Right now there is just one signing key used to create tokens for viewing contact information or letting users delete records that they posted.<br>
<br>
<b><code>Counter</code></b> entities are used to store counts of how many records are in the database, for reporting and charting.<br>
<br>
<b><code>StaticSiteMapInfo</code></b> and <b><code>SiteMapPingStatus</code></b> are used to store information for site maps (for indexing by search engines).  This feature is not used much and will probably be removed.<br>
<br>
<b><code>ConfigEntry</code></b> entities store configuration settings for each repository.  For example, different repositories can have different languages available in the language menu; there are also various other locality-related options.<br>
<br>
<br>
<h3>Indexing and ranking</h3>

In <code>indexing.py</code>, Person records are indexed by putting all possible prefixes of <code>first_name</code> and <code>last_name</code> into a StringListProperty called <code>names_prefixes</code>.  The names are normalized (by removing accents and converting to uppercase) before forming these prefixes.  See <code>text_query.py</code> for the normalization function.<br>
<br>
In the <code>CmpResults.rank()</code> method, matches are ranked by a score based on how much of the name is matched and whether the first and last name are matched in the right order.  The ordering preference is different for Chinese, Japanese, and Korean names.<br>
<br>
#. Remove all accents from letters (e.g. replace å with a).<br>
#. Convert all letters to uppercase.<br>
#. Store three extra attributes on the Person entity:<br>
<br>
<br>
<br>
<table><thead><th> <a href='DeveloperGuide.md'>« back to DeveloperGuide</a> </th></thead><tbody>