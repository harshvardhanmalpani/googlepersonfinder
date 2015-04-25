<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DataAPI'>direct link</a>).</font>


The Person Finder application stores and exports records using the People Finder Interchange Format (PFIF), which is based on XML. Documentation on the format is available here:

  * [PFIF 1.4 specification](http://zesty.ca/pfif/1.4)
  * [PFIF FAQ and implementation guidelines](http://zesty.ca/pfif/faq.html)

If you'd like to automatically detect when Google Person Finder launches a new repository, see RepositoryFeed.

<br>

<h3>Requesting an API key for an existing Person Finder repository</h3>

To search, download data from, or upload data to an existing Google Person Finder repository, you need an API key.  <font color='#a00'>Note: You don't need an API key from Google for instances of the Person Finder application that you launch yourself.  API keys from Google are only required for access to repositories hosted at google.org/personfinder that Google manages for major disaster events.</font>

<ul><li><b>If you are developing an application, you can use our <a href='https://google.org/personfinder/test'>"test" repository</a> with an API key 43HxMWGBijFaYEr5</b> . When you upload data with the key, use a domain name testkey.personfinder.google.org as the prefix of record IDs.<br>
</li><li>For access to other repositories, <a href='https://support.google.com/personfinder/contact/pf_api?rd=1'>request an API key here</a>. The three types of access you can apply for are:<br>
<ul><li>Search: Allows you to retrieve data based on a search query.<br>
</li><li>Write: Allows you to publish records to the database.<br>
</li><li>Read: Allows you to retrieve all records in the database.</li></ul></li></ul>

When Google receives a request for an API key, we may evaluate the request based on factors including the motivation for the request and the likelihood that the request will meaningfully expand the usefulness of Person Finder and its accessibility to users. Google reserves the right to grant or deny a request for an API key for any reason, in its sole discretion. Any entity requesting an API key must agree to the <a href='http://code.google.com/p/googlepersonfinder/wiki/TermsOfService'>Person Finder API Terms of Service</a>.<br>
<br>
<br>

<h3>Using the Person Finder search API</h3>

You can access the search API here:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/search?key=</code><font color='#a00'><i>api_key</i></font><code>&amp;q=</code><font color='#a00'><i>your query </i></font><br></blockquote>

It will return the matching results as a XML file with PFIF format. By default it will return up to 100 records. You can use a max_results=N parameter to restrict the number of result records.<br>
<br>
If you know the PFIF <code>person_record_id</code> of a specific person, you can also fetch a single PFIF person record with notes at the following URL:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/search?key=</code><font color='#a00'><i>api_key</i></font><code>&amp;id=</code><font color='#a00'><i>person_record_id</i></font></blockquote>

When displaying any content accessed via the API to a user, you must display a link to the original source of information to refer any enquiries in connection with that specific record back to the original source, and may not intermix content accessed via the API with other content in any way that makes it unclear which content came from which source.<br>
<br>
<br>

<h3>Uploading data into Person Finder</h3>

You can also push one or more PFIF records to the Person Finder by posting an XML file to the following URL:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/write?key=</code><font color='#a00'><i>api_key</i></font></blockquote>

PFIF 1.1, 1.2, 1.3, and <a href='http://zesty.ca/pfif/1.4'>1.4</a> (<a href='http://zesty.ca/pfif/1.4/examples.html'>Example</a>) are accepted. Note that:<br>
<ul><li>You will need an API key (see the section above for instructions on obtaining a key).<br>
</li><li>person_record_id and note_record_id must be in the form of <font color='#a00'><i>domain_name</i></font>/<font color='#a00'><i>unique_string</i></font> e.g., example.com/113 . <font color='#a00'><i>domain_name</i></font> must be the one you specified in the "Domain Name" field of <a href='https://support.google.com/personfinder/contact/pf_api?rd=1'>the API key request form</a>. If you use the "test" repository, it must be testkey.personfinder.google.org .</li></ul>

Once you have prepared an XML file, you can use the following command to upload it:<br>
<br>
<blockquote><code>curl -X POST -H 'Content-type: application/xml' --data-binary @</code><font color='#a00'><i>your_file</i></font><code>.xml \</code>
<code>    https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/write?key=</code><font color='#a00'><i>auth_token</i></font></blockquote>

<b>NOTE:</b> Make sure not to drop "@" before the file name. Otherwise a string "your_file.xml" is sent as the POST body, instead of the content of the file.<br>
<br>
The XML document can contain <code>&lt;pfif:person&gt;</code> elements with nested <code>&lt;pfif:note&gt;</code> elements. To understand the proper XML format, see the PFIF example document. We recommend that you upload a single record or a small number of records as a test, retrieve the records using the Individual Person Record API (/api/read), and view the records on the site to verify that the results are what you expected. Pay careful attention to the handling of accented letters, note text, source URLs, and photo URLs (if you have them).<br>
<br>
Due to the size limitation on POST requests, you should split up files into batches of 100 <code>&lt;pfif:person&gt;</code> elements. If you encounter an error, or need to correct problems in a previous upload, it is safe to upload the same records again. Records will replace existing records with the same <code>person_record_id</code> or <code>note_record_id</code>.<br>
<br>
The response will be an XML document like this:<br>
<br>
<pre><code>&lt;?xml version="1.0"?&gt;<br>
&lt;status:status&gt;<br>
  &lt;status:write&gt;<br>
    &lt;status:record_type&gt;pfif:person&lt;/status:record_type&gt;<br>
    &lt;status:parsed&gt;1&lt;/status:parsed&gt;<br>
    &lt;status:written&gt;1&lt;/status:written&gt;<br>
    &lt;status:skipped&gt;<br>
    &lt;/status:skipped&gt;<br>
  &lt;/status:write&gt;<br>
<br>
  &lt;status:write&gt;<br>
    &lt;status:record_type&gt;pfif:note&lt;/status:record_type&gt;<br>
    &lt;status:parsed&gt;1&lt;/status:parsed&gt;<br>
    &lt;status:written&gt;1&lt;/status:written&gt;<br>
    &lt;status:skipped&gt;<br>
    &lt;/status:skipped&gt;<br>
  &lt;/status:write&gt;<br>
&lt;/status:status&gt;<br>
</code></pre>

Each <code>&lt;status:write&gt;</code> element describes one batch of writes. <code>&lt;status:record_type&gt;</code> indicates the type of the batch. <code>&lt;status:parsed&gt;</code> says how many XML records were successfully parsed. <code>&lt;status:written&gt;</code> says how many were written to the datastore. In the above example, 1 person and 1 note were successfully written.<br>
When there are problems it will look like this:<br>
<br>
<pre><code>&lt;?xml version="1.0"?&gt;<br>
&lt;status:status&gt;<br>
  &lt;status:write&gt;<br>
    &lt;status:record_type&gt;pfif:person&lt;/status:record_type&gt;<br>
    &lt;status:parsed&gt;1&lt;/status:parsed&gt;<br>
    &lt;status:written&gt;0&lt;/status:written&gt;<br>
    &lt;status:skipped&gt;<br>
      &lt;pfif:person_record_id&gt;google.com/person.4040&lt;/pfif:person_record_id&gt;<br>
      &lt;status:error&gt;not in authorized domain: u'google.com/person.4040'&lt;/status:error&gt;<br>
    &lt;/status:skipped&gt;<br>
  &lt;/status:write&gt;<br>
<br>
  &lt;status:write&gt;<br>
    &lt;status:record_type&gt;pfif:note&lt;/status:record_type&gt;<br>
    &lt;status:parsed&gt;1&lt;/status:parsed&gt;<br>
    &lt;status:written&gt;0&lt;/status:written&gt;<br>
    &lt;status:skipped&gt;<br>
      &lt;pfif:note_record_id&gt;zesty.ca/note.53&lt;/pfif:note_record_id&gt;<br>
      &lt;status:error&gt;ValueError: bad datetime: u'xyz'&lt;/status:error&gt;<br>
    &lt;/status:skipped&gt;<br>
  &lt;/status:write&gt;<br>
&lt;/status:status&gt;<br>
</code></pre>

Each <code>&lt;status:skipped&gt;</code> entry describes the reason why a particular record was skipped, and includes the record ID if one was given.<br>
<br>
When you upload person or note records, you will be replacing any existing records with the same record ID. It should be safe to upload the same data multiple times while you fix formatting problems.<br>
<br>
Google will treat all PFIF records submitted through Google Person Finder and through the API in conformance with the PFIF Data Expiry Mechanism (see <a href='http://zesty.ca/pfif/1.4'>http://zesty.ca/pfif/1.4</a>).<br>
<br>
<br>

<h3>Downloading data from Person Finder</h3>

PFIF 1.4 person and note feeds are available here:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/person?key=</code><font color='#a00'><i>api_key</i></font><br>
<code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/note?key=</code><font color='#a00'><i>api_key</i></font><br></blockquote>

By default, these feeds return the most recently added person records or note records in reverse chronological order. These query parameters are supported:<br>
<br>
<ul><li><code>max_results</code>: Return up to the specified number of results (maximum 200).<br>
</li><li><code>skip</code>: Skip the specified number of records before returning the next max_results results (maximum 800).<br>
</li><li><code>min_entry_date</code>: Return only results with an entry_date greater than or equal to the specified timestamp, which should be in UTC in <code>yyyy-mm-ddThh:mm:ssZ</code> format. If this parameter is specified, results will be returned in forward chronological order.<br>
</li><li><code>person_record_id</code>: Return only notes for this person record. This parameter is only valid for the note feed.</li></ul>

You can use the <code>person_record_id</code> parameter to subscribe to a feed of notes on a specific person.<br>
<br>
If you need to keep another database synchronized with the Google Person Finder database, use the <code>min_entry_date</code> and <code>skip</code> parameters to download incremental updates. Use the latest <code>entry_date</code> you have previously received from Google Person Finder as the <code>min_entry_date</code> for your first request. Then take the latest <code>entry_date</code> in the batch you receive, and use it as the <code>min_entry_date</code> for your next request. Use the <code>skip</code> parameter to skip the records you already received that have the same <code>entry_date</code>. This algorithm is implemented by <a href='http://code.google.com/p/googlepersonfinder/source/browse/tools/download_feed.py'>tools/download_feed.py</a>.<br>
<br>
We also recommend that you use the <code>min_entry_date</code> parameter in the above fashion whenever you need to scan a large number of records.  (The <code>skip</code> parameter is limited to a maximum value of 800 due to limitations in the App Engine datastore, so using <code>skip</code> alone will not let you scan all the records.)<br>
<br>
When displaying any content accessed via the API to a user, you must display a link to the original source of information to refer any enquiries in connection with that specific record back to the original source, and may not intermix content accessed via the API with other content in any way that makes it unclear which content came from which source.