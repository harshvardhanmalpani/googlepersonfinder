<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DataAPIJapanese'>direct link</a>).</font>

以下は [Person Finder DataAPI](http://code.google.com/p/googlepersonfinder/wiki/DataAPI) の日本語訳です。

パーソンファインダーはXMLに基づいた People Finder Interchange Format (PFIF)を用いてレコードの保存および書き出しを行うアプリケーションです。

  * [PFIF 1.4 仕様](PFIF1_4_Japanese.md)
  * [PFIF FAQと導入ガイドライン (英語)](http://zesty.ca/pfif/faq.html)

<br>

<h3>既存のパーソンファインダー・リポジトリにアクセスするには</h3>

既存のGoogleパーソンファインダーのリポジトリ内を検索、またデータのダウンロードやアップロードを行うにはAPIキーが必要です。<font color='#a00'>注:これは自分で作製したインスタンスには必要ありません。大規模な災害に備え、Googleが管理・提供しているリポジトリにのみ必要となります。</font>

<ul><li><b>アプリケーションを開発している方は、<a href='https://google.org/personfinder/test'>"test"リポジトリ</a>にAPIキー 43HxMWGBijFaYEr5 でアクセスできます。</b> このキーで書き込みを行う場合は、レコードIDのプレフィックスとしてドメイン名 testkey.personfinder.google.org を使用してください。</li></ul>

<ul><li>他のリポジトリにアクセスするには、<a href='https://support.google.com/personfinder/contact/pf_api'>こちら</a>からAPIキーを申請してください。アクセスタイプには３つの種類があります。<br>
<ul><li>検索：検索クエリに基づいたデータの取得が可能になります<br>
</li><li>読み取り：データベース上のすべてのレコードを取得できます<br>
</li><li>書き込み：データベース上にレコードを追加できます</li></ul></li></ul>

トークンの申請を受けると、Googleは申請理由や、申請された利用方法によりユーザーにとってのパーソンファインダーの使いやすさや利便性を十分に拡張するものか、などを審査します。Googleはいかなる理由であれトークンの申請の許可および拒否を独自に決定する権利を有します。トークンを申請される方は <a href='http://code.google.com/p/googlepersonfinder/wiki/TermsOfService'>パーソンファインダーAPI使用規約（英語）</a> に合意しなければなりません。<br>
<br>
<br>

<h3>パーソンファインダーからデータをダウンロードするには</h3>

PFIF1.4 person と note のフィードは以下URLからご覧になれます<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/person?key=</code><font color='#a00'><i>api_key</i></font><br>
<code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/note?key=</code><font color='#a00'><i>api_key</i></font><br></blockquote>

初期設定では、これらの登録されたpersonおよびnoteのフィードは新しいものから古いものに逆日付順に表示します。以下のクエリパラメータに対応しています。<br>
<br>
<ul><li><code>max_results</code>: 最大200までの特定数のレコードを表示します。<br>
</li><li><code>skip</code>: max_resultsの結果を表示する前に指定した数のレコードをスキップします。<br>
</li><li><code>min_entry_date</code>: <code>yyyy-mm-ddThh:mm:ssZ</code> の形式で指定された協定世界時(UTC)におけるタイムスタンプよりも新しいあるいは同時刻の結果のみを表示します。このパラメータが指定された場合は表示順は日付順となります。<br>
</li><li><code>person_record_id</code>: 指定された個人へのnoteだけを表示する。このパラメータはnoteフィードでのみ有効です。</li></ul>

<code>person_record_id</code> パラメータを用いて特定個人のnoteフィードを購読することが出来ます。<br>
<br>
Googleパーソンファインダー・データベースと同期したデータベースが必要な場合は、<code>min_entry_date</code>と<code>skip</code>パラメータを用いて差分のアップデートをダウンロードすることが出来ます。その際、前回Googleパーソンファインダーから取得した中で最も新しい<code>entry_date</code>を、最初のリクエストの<code>min_entry_date</code>として使ってください。次に、受け取った<code>batch</code>の中で最も新しい<code>entry_date</code>を、次のリクエスト時に<code>min_entry_date</code>として使ってください。同じ<code>entry_date</code>を持つ、すでに受け取ったレコードをスキップするためにもし<code>skip</code>パラメータを使ってください。このアルゴリズムは<a href='http://code.google.com/p/googlepersonfinder/source/browse/tools/download_feed.py'>tools/download_feed.py</a>に実装されています。<br>
<br>
特定個人のPFIF <code>person_record_id</code> がわかっている場合は、その個人レコードおよびnoteを以下のURLから取得できます。<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/read?key=</code><font color='#a00'><i>api_key</i></font><code>&amp;id=</code><font color='#a00'><i>person_record_id</i></font></blockquote>

APIを通してアクセスされたコンテンツをユーザーに表示する場合、その特定のレコードに関する調査の際に、オリジナルのソースを参照できるようにするために、必ずオリジナルのソースへのリンクを含めてください。また、APIを通してアクセスされたコンテンツと他のコンテンツを混ぜ、どのコンテンツがどのソースから来たのかを不明確にすることは避けてください。<br>
<br>
<br>

<h3>パーソンファインダー検索APIを使うには</h3>

検索APIへは以下からアクセスできます:<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/search?key=</code><font color='#a00'><i>api_key</i></font><code>&amp;q=</code><font color='#a00'><i>your query </i></font><br></blockquote>


合致結果はPFIFフォーマットのXMLファイルとして表示されます。初期設定では最大１００件のレコードを取得できます。<code>max_results</code> パラメータを用いることで表示数を制限することが出来ます。<br>
<br>
APIを通して取得したコンテンツをユーザーに表示する場合は、必ずオリジナルレコードへのリンクを含めてください。これはユーザがそのレコードに関してさらに調べる際に、オリジナルの記録を参照できるようにするためです。また、APIを通して取得したコンテンツと他のコンテンツをソースが不明確になるような形で混ぜて表示することは許可されません。<br>
<br>
<br>

<h3>パーソンファインダーにデータをアップロードするには</h3>

XMLファイルを以下のURLにPOSTすることでパーソンファインダーに複数のPFIFレコードを追加することが出来ます。<br>
<br>
<br>
<blockquote><code>https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/write?key=</code><font color='#a00'><i>api_key</i></font></blockquote>

PFIF1.1, 1.2, 1.3, <a href='http://zesty.ca/pfif/1.4'>1.4</a> (<a href='http://zesty.ca/pfif/1.4/examples.html'>例</a>)が使用可能です。注:<br>
<ul><li>APIキーが必要です(キーを取得する方法については、上の節を参照してください)。<br>
</li><li>person_record_id と note_record_id は <font color='#a00'><i>domain_name</i></font>/<font color='#a00'><i>unique_string</i></font> の形式である必要があります(例: example.com/113 )。<font color='#a00'><i>domain_name</i></font> は<a href='https://support.google.com/personfinder/contact/pf_api?rd=1'>APIキー申請フォーム</a>で"Domain Name"の欄に書いたものと同一である必要があります。"test"リポジトリを使う場合は testkey.personfinder.google.org を使用してください。</li></ul>

XMLファイルの準備が整ったら、以下のコマンドでアップロードしてください。<br>
<br>
<blockquote><code>curl -X POST -H 'Content-type: application/xml' --data-binary @</code><font color='#a00'><i>your_file</i></font><code>.xml \</code>
<code>    https://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/api/write?key=</code><font color='#a00'><i>auth_token</i></font></blockquote>

XMLドキュメントは<code>&lt;pfif:person&gt;</code>エレメントを複数含むことができ、個々の<code>&lt;pfif:person&gt;</code>エレメントは<code>&lt;pfif:note&gt;</code>エレメントを複数含むことができます。このXMLフォーマットの詳細については、PFIF参考ドキュメントを参照して下さい。我々が推奨する方法は、まず一つ、もしくは少数のレコードをテストとしてアップロードし、Individual Person  Record API (/api/read)を使ってそのデータを取得します。そしてサイトのレコードと自分の予測した結果が同じかどうかを確かめてみてください。アクセント記号付き文字、noteのテキスト、ソースURL、写真URLを含んでいる場合は特に注意してください。<br>
<br>
POSTリクエストのサイズ制限によって、ファイルを100個の<code>&lt;pfif:person&gt;</code>エレメントごとに分割しなくてはならない場合があります。エラーの場合、もしくは前回のアップロードで修正すべきことがある場合は、同じレコードをもう一度アップロードするのがよいでしょう。そのレコードは同一の<code>person_record_id</code>や<code>note_record_id</code>を持った既存のレコードを置き換えます。<br>
<br>
レスポンスは以下のようなXMLドキュメントになるはずです：<br>
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

1つの <code>&lt;status:write&gt;</code>エレメントが１回の書き込みに対応します。<code>&lt;status:record_type&gt;</code>は書き込みのタイプ、<code>&lt;status:parsed&gt;</code>はパースに成功したレコード数、そして<code>&lt;status:written&gt;</code>は datastore に書き込まれた数を表しています。上の例からは1人のpersonと1つのnoteの書き込みに成功したことが分かります。問題があった場合は以下のように表示されます：<br>
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

<code>&lt;status:skipped&gt;</code>の各項は、なぜそのレコードがスキップされたのか、もしレコードIDがある場合はそれも含まれます。<br>
<br>
personやnoteをアップロードする場合、同一レコードIDのレコードが既に存在すれば、新しいもので置き換えられます。ですから、フォーマットのエラーを修正するために複数回同じデータをアップロードしても問題ありません。<br>
<br>
GoogleはGoogleパーソンファインダーおよびそのAPIを通して提出されたPFIFレコードをPFIF Data Expiry Mechanism に準拠して扱います。