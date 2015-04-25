<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/RepositoryFeedJapanese'>direct link</a>).</font>


以下は [Person Finder Repository Feed](http://code.google.com/p/googlepersonfinder/wiki/RepositoryFeed) の日本語訳です。

アクティブなレポジトリーのリストを Atom フィード経由で取得することができます。このフィードを使うことで、新しいレポジトリーが追加されたことや、既存のレポジトリーが閉じられたことを自動的に知ることができます。
<br>

<h3>フィード URL</h3>

すべてのアクティブなレポジトリーのリストを含むグローバルフィードは以下から取得できます。<br>
<br>
<blockquote><code>http://www.google.org/personfinder/global/feeds/repo</code></blockquote>

また個別のレポジトリーのみについて知りたい場合は、以下の単一レポジトリーフィードを利用してください。<br>
<br>
<blockquote><code>http://www.google.org/personfinder/</code><font color='#a00'><i>repository</i></font><code>/feeds/repo</code></blockquote>

これらのフィードはすべて Atom 形式です。グローバルフィードはアクティブなレポジトリー当たり 1 つのエントリーを持っています。単一レポジトリーフィードは指定されたレポジトリーに対応するエントリーを 1 つだけ持ちます。<br>
<br>
Atom フィードのエントリーは以下に列挙されているカスタム要素によって構成されています。カスタム要素の XML 名前空間は以下の通りです。<br>
<br>
<code>http://schemas.google.com/personfinder/2012</code> (名前空間接頭辞には <code>gpf</code> を用います).<br>
<br>
新しいレポジトリーが追加された際には、新しいエントリーがフィードにも追加されます。既存のレポジトリーが閉じられた際には、対応するエントリーがフィードから削除されます。<br>
<br>

<h3>エントリーの詳細</h3>

Atom エントリーはそれぞれ以下の標準要素を含みます。<br>
<br>
<ul><li><code>&lt;id&gt;</code> 要素はレポジトリーのスタートページの URL を表します。これは該当するレポジトリーの固有識別子として使うことができます。<br>
</li><li><code>&lt;title&gt;</code> 要素は既定の言語におけるレポジトリーのタイトルを表します。この要素は <code>xml:lang</code> 属性を持ち、既定言語が何であるかを表します。<br>
</li><li><code>&lt;published&gt;</code> 要素はレポジトリーが最初にアクティブになった日時を表します。<br>
</li><li><code>&lt;updated&gt;</code> 要素はレポジトリーの有効・無効、またはテストモード・リアルモードが最後に切り替わった日時を表します。これは基本的には <code>&lt;published&gt;</code> と同じ値ですが、レポジトリーがテストモードで立ち上げられ、その後リアルモードに切り替えられた場合、切り替えの日時を表します。</li></ul>

Atom エントリーの <code>&lt;content&gt;</code> 要素は唯一の要素である <code>&lt;gpf:repo&gt;</code> で構成されます。<code>&lt;gpf:repo&gt;</code> 要素は以下のカスタム要素で構成されます。<br>
<br>
<ul><li><code>&lt;gpf:title&gt;</code>: レポジトリーのタイトルを表します。レポジトリーが対応している言語ごとに、1 つの <code>&lt;gpf:title&gt;</code> があり、<code>xml:lang</code> 属性がその言語を表します。そのため、複数の言語に対応している場合は複数の <code>&lt;gpf:title&gt;</code> が存在します。<br>
</li><li><code>&lt;gpf:read_auth_key_required&gt;</code>: API 経由でレコードを読み込む際に API キーが必要な場合、文字列の <code>true</code> を含みます。<br>
</li><li><code>&lt;gpf:search_auth_key_required&gt;</code>: API 経由でレコードを検索する際に API キーが必要な場合、文字列の <code>true</code> を含みます。<br>
</li><li><code>&lt;gpf:location&gt;</code>: レポジトリーに関連した災害・事故のおおよその位置を GeoRSS point 形式で表します。GeoRSS point は <code>&lt;georss:point&gt;</code> 要素で表され、緯度経度を半角スペースで区切ったフォーマットとなります。<br>
</li><li><code>&lt;gpf:test_mode&gt;</code>: レポジトリーがテストモードに設定されている場合は、文字列の <code>true</code> を含みます。テストモードでは、レコードは 6 時間を経過すると自動的に削除されます。