<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DataAPIChinese'>direct link</a>).</font>

Google网上寻人应用可以存储和导出基于XML的 People Finder Interchange Format (PFIF)记录。
关于这种格式的文档在这里:

  * [PFIF 1.4 specification](http://zesty.ca/pfif/1.4)
  * [PFIF FAQ and implementation guidelines](http://zesty.ca/pfif/faq.html)

如果你希望自动检测到Google网上寻人的新数据库，请查看[RepositoryFeed](RepositoryFeed.md)。

<br>

<h3>为访问现有的网上寻人数据库申请API key</h3>

为了搜索，下载和上传数据到现有的Google网上寻人数据库，你需要一个API key。<br>
<font color='#a00'>提示：如果自己发布一个网上寻人应用，并不需要Google的API key。只有在访问放在 google.org/personfinder 上由Google管理的大规模灾害数据库时，才需要Google的API key。</font>

<ul><li><b>If you are developing an application, you can use our <a href='https://google.org/personfinder/test'>"test" repository</a> with an API key 43HxMWGBijFaYEr5</b> . When you upload data with the key, use a domain name testkey.personfinder.google.org as the prefix of record IDs.<br>
</li><li>要访问其他数据库，<a href='https://support.google.com/personfinder/contact/pf_api?rd=1'>在这里申请API key</a>. 可以申请三种访问类型：<br>
<ul><li>搜索：可以通过搜索查询取得数据<br>
</li><li>读取：可以读取数据库的所有记录<br>
</li><li>写入：可以发布记录到数据库</li></ul></li></ul>

当Google收到一个API key申请时，我们会考虑申请的原因以及使得网上寻人更有用、更多人使用的可能性。Google保留以任何原因授权或者拒绝API key申请的权力。任何申请API key的个体都必须同意<a href='http://code.google.com/p/googlepersonfinder/wiki/TermsOfService'>Person Finder API Terms of Service</a>.<br>
<br>
<br>

<h3>从网上寻人下载数据</h3>

PFIF 1.4 person 和 note 的源可以从这里访问：<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/person?key=</code><font color='#a00'><i>api_key</i></font><br>
<code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/note?key=</code><font color='#a00'><i>api_key</i></font><br></blockquote>

默认情况下，这些源以倒序返回最近添加的 person 和 note 记录。支持的查询参数包括：<br>
<br>
<ul><li><code>max_results</code>: 最多返回的结果数（最大值200）。<br>
</li><li><code>skip</code>: 返回 max_results 个结果之前，跳过的结果数。<br>
</li><li><code>min_entry_date</code>: 只返回 entry_date 等于或大于指定时间戳之后的结果。使用UTC，格式为<code>yyyy-mm-ddThh:mm:ssZ</code>。如果指定了这个参数，结果会以顺序返回。<br>
</li><li><code>person_record_id</code>: 只返回此 id 的 person 记录的 note 记录。此参数只对 note 的源有效。</li></ul>

可以使用 <code>person_record_id</code> 参数去订阅关于某个人的 notes 源。<br>
<br>
如果需要保持另一个数据库与Google网上寻人数据库同步的话，可以使用 <code>min_entry_date</code> 和 <code>skip</code> 参数来下载增量更新。使用你之前从Google网上寻人得到的最新的 <code>entry_date</code> 作为第一次请求的 <code>min_entry_date</code>。然后用得到的最新的 <code>entry_date</code>，作为下个请求的 <code>min_entry_date</code>。使用 <code>skip</code> 参数来跳过你已有的拥有相同 <code>entry_date</code> 的记录。此算法已在这里实现  <a href='http://code.google.com/p/googlepersonfinder/source/browse/tools/download_feed.py'>tools/download_feed.py</a>.<br>
<br>
如果知道某个人的 PFIF <code>person_record_id</code>，就可以取得他的一个带有 notes 的 PFIF person 记录，URL如下：<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/read?key=</code><font color='#a00'><i>api_key</i></font><code>&amp;id=</code><font color='#a00'><i>person_record_id</i></font></blockquote>

当向用户显示任何通过API取得的内容时，必须显示链接到原来的信息源，以指引任何对某记录的询问回到信息源。并且不可把通过API取得的内容和其他内容以任何形式混杂，以使得其来源不清楚。<br>
<br>
<br>

<h3>使用网上寻人搜索API</h3>

可以如此访问搜索API：<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/search?key=</code><font color='#a00'><i>api_key</i></font><code>&amp;q=</code><font color='#a00'><i>your query </i></font><br></blockquote>

它将返回一个含有对应结果的 PFIF 格式的XML文件。默认返回最多100个记录。可以使用 max_results=N 参数来限制结果数目。<br>
<br>
当向用户显示任何通过API取得的内容时，必须显示链接到原来的信息源，以指引任何对某记录的询问回到信息源。并且不可把通过API取得的内容和其他内容以任何形式混杂，以使得其来源不清楚。<br>
<br>
<br>

<h3>上传数据到网上寻人</h3>

通过 POST 一个XML文件，可以发布一个或多个 PFIF 记录到网上寻人，URL如下：<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/write?key=</code><font color='#a00'><i>api_key</i></font></blockquote>

我们接受 PFIF 1.1, 1.2, 1.3 和 1.4 格式。请注意这里需要一个API key（参考以上说明来取得key）。<br>
<br>
一旦准备好一个XML文件后，可以通过一下命令来上传：<br>
<br>
<blockquote><code>curl -X POST -H 'Content-type: application/xml' --data-binary @</code><font color='#a00'><i>your_file</i></font><code>.xml \</code>
<code>    https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/write?key=</code><font color='#a00'><i>auth_token</i></font></blockquote>

XML文档可以包含内嵌 <code>&lt;pfif:note&gt;</code> 元素的 <code>&lt;pfif:person&gt;</code> 元素。请参考 PFIF 示例文档来理解正确的XML格式。<br>
我们推荐你先上传单个或者少量记录作为测试，再通过单人 person 记录API (/api/read) 取回它，和在网站上浏览确认它们是所期望的结果。请特别小心注意处理重音字母、note的文本、来源URLs和照片URLs（如果你有的话）。<br>
<br>
因为POST请求有大小限制，你必须把文件分割成一个个含有100个 <code>&lt;pfif:person&gt;</code> 元素的文件。如果你遇到错误，或者需要修正上一次上传数据的问题，是可以把同样的记录集再上传一次的。新上传的记录会把既存的带有相同 <code>person_record_id</code> 或 <code>note_record_id</code> 的记录给替换。<br>
<br>
返回的XML文档应答如下：<br>
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

每个 <code>&lt;status:write&gt;</code> 元素描述一次的数据写入。<code>&lt;status:record_type&gt;</code> 表示此次写入的类型，<code>&lt;status:parsed&gt;</code> 表示被成功解释的XML记录数目，<code>&lt;status:written&gt;</code> 表示写到数据库的记录数目。在以上的例子中，1个 person 和1个 note 被成功写入了。当有问题时应答如下：<br>
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

每个 <code>&lt;status:skipped&gt;</code> 元素描述此记录被跳过的原因，并给出此记录ID（如果有提供的话）。<br>
<br>
当你上传 person 或 note 记录时，它会替换既存的带有相同ID的记录。所以可以不断尝试上传同一个数据集来修正格式问题。<br>
<br>
Google会根据 PFIF 数据过期机制来处理所有通过API上传的 PFIF 数据记录。