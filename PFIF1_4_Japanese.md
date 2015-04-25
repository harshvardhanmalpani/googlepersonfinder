<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/PFIF1_4_Japanese'>direct link</a>).</font>

この仕様の原文のURL（英語）:  http://zesty.ca/pfif/1.4

PFIF 1.4 の例: http://zesty.ca/pfif/1.4/examples.html

FAQ、参考例、その他のPFIFに関する情報（英語）: http://zesty.ca/pfif

このドキュメントは [GNU Free Documentation License 1.2](http://www.gnu.org/copyleft/fdl.html)のもとにライセンスされています。




---


# 概要 #
このドキュメントは、天災および人災時の行方不明者や遭難者の情報を共有するためのデータモデルとXMLベースの交換フォーマット「Person Finder Interchange Format」の定義します。はじめに、データモデルを実装スタイル（オブジェクト指向、リレーショナル、もしくはXML）に因らない形で解説します。次にPFIF XMLフォーマットを RELAX NG スキーマで定義します。また、PFIFデータを表現するためのリレーショナルデータベースのスキーマ例も提示します。

# デザイン方針 #
  1. PFIFの目的は人とデータを引き合わせることにあります。このデザインは集約の効率化を目指しています。同じ人物を捜している人たちの情報、複数の情報源から得られた個人についての情報、重複する情報、そして何より愛する人々と離ればなれになってしまった人々が集まる場です。
  1. データは追跡可能でなければなりません。情報は確実性や責任が明らかでない情報源から提供されます。ユーザーがその信憑性を確認するために情報源に関するデータも管理されます。
  1. それぞれのレコードはある _**オリジナルレポジトリ**_ に帰属します。オリジナルレポジトリは PFIF にもとづくものでも、そうでないものでも構いません。レコードは他の場所へコピーされることもありますが、オリジナルレポジトリはそのレコードにたいして唯一の情報源であり続けます。レコードの内容を変更できるのはオリジナルレポジトリだけとなります。
  1. 各データアグリゲーターは独自の判断基準に基づき、どの情報源を信頼するかは各アグリゲーターが責任を負います。ある特定の権威がすべてのデータについての「真実」を規定することは不可能です。
  1. 複数のレコードが同一人物を指している場合があります。PFIFはそのようなレコードを結びつけることができます。しかし、前項にある通り、どのレコードを結びつけるかは各アグリゲーターが決定します。結びつけ方を決定する特定の権威は存在しません。
  1. 異なる経路でインポートされた同一のレコードを処理できる必要があります。
  1. データレコードは世界中で送信/共有されるため、日時はローカルタイムではなくUTCで指定されなければなりません。日時のフォーマットは[RFC3339](http://www.ietf.org/rfc/rfc3339.txt)に準拠します。フロントエンドが日時をローカルタイムに変換して表示することは許されます。

# データのライフサイクル #

PFIFレポジトリはオリジナルレコードとクローンレコードを持つことができます。オリジナルレコードとはオリジナルレポジトリの中に存在するもののことです。一方、クローンレコードとは他のレポジトリからコピーされたレコードのことです。PFIFレコードがどのように作り出され、他のレポジトリにたどり着くのかを示したダイアグラムが下記です。

<pre>
.----------------------.<br>
| 1. 実世界の事実        |<br>
'----------------------'<br>
|             |<br>
人間による PFIF  |             | 人間によるPFIF以外の<br>
レポジトリへの登録 |             | レポジトリへの登録<br>
|             |<br>
レポジトリが      |             |<br>
entry_date, source_date,|             |<br>
source_name, source_url |             |<br>
を設定 |             |<br>
v             v<br>
.------------------------------.   .---------------------------------.<br>
| 2a. オリジナルレポジトリ中の     |   | 2b. オリジナルレポジトリ中の       |<br>
|       PFIFレコード            |   |       非PFIFレコード              |<br>
'------------------------------'   '---------------------------------'<br>
|             |<br>
PFIF文書もしくはフィード |             | 自動あるいは手動によるPFIF<br>
としてエクスポート |             | データモデルへの変換<br>
|             |<br>
|             | 自動あるいは手動による<br>
|             | source_date, source_name, source_urlの付与<br>
v             v<br>
.-----------------.<br>
.--------------> | 3. PFIF レコード  |<br>
|                '-----------------'<br>
|                        |<br>
|                        | PFIFレポジトリへの読み込み<br>
|                        |<br>
|                        | 読み込み時点の日時を entry_date に設定<br>
|                        v<br>
|     .--------------------------------------.<br>
|     | 4. PFIFレポジトリ内のクローンレコード |<br>
|     '--------------------------------------'<br>
|                        |<br>
|                        | PFIF文書あるいはフィードとしてエクスポート<br>
|                        |<br>
'------------------------'<br>
</pre>


## Incremental export mechanism ##

PFIFレポジトリがオリジナルレコードやクローンレコードを追加する際は `entry_date` フィールドを現在時刻に設定しなければなりません。
`entry_date` はレコードを追加したときに減少してはいけません。
クライアントが別のレポジトリからコピーしたレコードをアップデートするには、最後に取得したレコードの `entry_date` より大きいあるいは同じ値の `entry_date` を持ったレコードを、そのレポジトリに問い合わせます。

## Data update mechanism ##

オリジナルレポジトリ（ダイアグラム上の2aもしくは2bにあたる）は以前に作成したレコードのフィールドのうち、`person_record_id` を除く、すべてのフィールドを変更することができます。PFIFレポジトリがオリジナルレコードを作成もしくは変更する場合は必ず `source_date` と `entry_date` フィールドを現在の時刻に設定必要があります。レポジトリがインポートした PFIF レコードが既存のレコードと同じ identifier をもつ場合、最も新しい`source_date` のものを保存します。

## Data expiry mechanism ##

`expiry_field` は（存在する場合）個人的な情報を保護するためにそのレコードをいつ消去するかを示します。本仕様に実装を適合させるためには、以下の条件を満たさねばなりません

  * `expiry_date` から1日以内に、PFIFレポジトリはユーザ及びAPIクライアントに対して、PERSONレコード及びそれに関連づけられているNOTEレコードをアクセス不可にしなくてはなりません。

  * その後レポジトリがAPIを通してデータをエクスポートする場合には、期限切れを示す PERSON レコードとして、次のプレースホルダーをエクスポートしなければなりません。プレースホルダーは期限が切れた PERSON レコードと同一の `person_record_id` と`expiry_date` を持ち、プレースホルダーが作成された日時を示す `source_date` と `entry_date` を持ちます。その他のフィールドは空欄にするかあるいは省略されなければいけません。

  * `expiry_date` から60日以内にPFIFレポジトリおよびそのバックアップの中に存在するPERSONレコードおよび関連づけられたNOTEレコードは、永久かつ復旧不可能な方法ですべて削除されなければなりません。ただし、前項で説明したプレースホルダーを作成するのに必要な `person_record_id`、`source_date`、`entry_date`、そして`expiry_date` は除きます。

ユーザーからのオリジナルレコードの削除要請があった場合、PFIFレポジトリは `expiry_date` を現在時刻に設定します。（ [前述](#Data_update_mechanism.md)した通り、レポジトリは同時に `source_date` と`entry_date` も現在時刻に設定します。）上記の expiry mechanism により、オリジナルオリジナルレポジトリで削除されたレコードは、他の連動したPFIFレポジトリにおいても順次削除されます。

# データモデル #
レコードには二つの種類があります。PERSONレコードは人物を特定するための情報です。NOTEレコードは人物の現在の状況です。それぞれのNOTEレコードは特定のPERSONレコードに属しますが、PERSONレコードは複数のNOTEレコードを持つことができます。

PERSONレコードはある人物を捜している人、ある人物に関する情報を持っている人の両方が作成できます。PERSONレコードとはその人物の関係者全員が集まる場であり、NOTEレコードはその人に関する共有すべき情報を保存するための場所です。

PERSONレコードは内容に間違いがあった場合のみアップデートされるべきです。特定の人物の状況や居場所が変わった場合には、そのPERSONレコードに関連づけた新たなNOTEレコードを追加します。

## PERSONレコード ##

PERSONレコードにはフィールドが25項目あります。同じ人物への複数のレコードが存在する場合もあります。実際、複数のソースからデータをインポートするアプリケーションは同一人物のPERSONレコードを複数取得することがあります。そういったレコードを関連づけるかはアプリケーション次第です。（下記「リレーショナルデータベーススキーマの例」を参照）。アプリケーションは、すべてのレコードのコピーを保持したうえで、それとは別にどのレコードが同一人物に対応するか記録することが推奨されます。

_レコード自体に関するメタデータ（9項目）_


このメタデータはユーザーがデータを追跡し、信頼性を確認するために必要とされます。

  * `person_record_id` (ASCII文字列、必須）
    * レコードを一意に指定する識別子であり、小文字のASCIIドメインネーム、それに続くスラッシュ(/)、そしてローカル識別子、から成ります。ドメインネームはこのレコードに対して権限をもつオリジナルレポジトリを指定します。ローカル識別子のフォーマットはオリジナルレポジトリが決めます。person\_record\_id がアプリケーションのドメイン以外で始まる場合は、そのレコードがクローンレコードであることを意味します。

  * `entry_date` (“yyyy-mm-ddThh:mm:ssZ” 形式のASCII文字列 、任意）
    * UTCにおけるレコードの保存日時（上記、[Incremental export mechanism](#Incremental_export_mechanism.md) を参照）

  * `expiry_date` (“yyyy-mm-ddThh:mm:ssZ”形式のASCII文字列、任意）
    * UTCにおけるレコードの削除日時（上記、[Data expiry mechanism](#Data_expiry_mechanism.md) を参照）

  * `author_name` (Unicode文字列、任意）
    * レコードを入力した人のフルネーム

  * `author_email` (Eメールアドレスを表す文字列、任意）
    * レコードを入力した人への連絡用電子メールアドレス

  * `author_phone` (ASCII文字列、任意）
    * レコードを入力した人の電話番号

  * `source_name` (ASCII文字列、必須)
    * レコードのオリジナルレポジトリの名前。人間が読んで理解できるもの。

  * `source_date` (“yyyy-mm-ddThh:mm:ssZ”形式のASCII文字列、必須）
    * レコードのオリジナルコピーがオリジナルレポジトリに作製された日付（UTC）

  * `source_url` (URL文字列、任意）
    * オリジナルレポジトリ中のオリジナルレコードのURL (できるかぎり個別のレコードを指定するURLであることが望ましい）


_行方不明者を特定する情報（16項目）_


これらのフィールドは人物を特定するのに用いられる情報を含みます。間違いがあった場合を除き、変更される必要のない情報です。PERSONレコードの検索はこれらのフィールドの検索を行います。

  * `full_name` (Unicode文字列、必須）
    * 行方を探している人・行方が見つかった人の氏名。フォーマットは人物、言語、文化などに依存します。例えば、英名の場合はファーストネーム（名）、ミドルネーム、ラストネーム（姓）の順に間にスペースを入れて入力されます。一方、一般的な中国名は姓が最初で姓名の間にスペースはありません）。もしその人物が複数のフルネームを持つ場合（例えば、英名と中国名の両方）、改行文字（Unicode U+000A) で区切って、もっとも一般的に使われている名前を最初に、その他の名前を次に入力して下さい。

  * `given_name` （Unicode文字列、任意）
    * 行方を探している人・行方が見つかった人の名。ミドルネームもしくはミドルイニシャルがある場合はスペースを一つ空けて入力してください。

  * `family_name`（Unicode文字列、任意）
    * 行方を探している人・行方が見つかった人の姓。

  * `alternate_names` (Unicode文字列、任意）
    * ニックネームや別の綴り方など、人物が通常使う氏名表記ではないものの、その人と関連づけてよく使われる名前。例えば漢字のかな読みはここに入力してください。複数の名前を入力する場合は、改行文字（Unicode U+000A) で区切って下さい。

  * `description` (Unicode文字列、任意）
    * その人物に関する自由記述の説明文です。入力フォームとしてはマルチラインテキストボックスが適切です。

  * `sex` (ASCII文字列、任意）
    * 人物の（生物学的）性別を female,、male もしくは other から選んで入力します。性別が不明な場合は、このフィールドは含まないでください。

  * `date_of_birth` (“yyyy”、"yyyy-mm”, ”yyyy-mm-dd”形式のASCII文字列、任意）
    * 人物の生年月日。だいたいのものでも構いません。

  * `age` (整数、あるいは ”min-max”形式のASCII文字列、任意）
    * `source_date` の時点における、生年月日から数えた人物の（だいたいの）年齢。値は単なる整数値か、ハイフンでつないだ２つの整数値で表された範囲（両端の値を含む）です。`source_date` が欠如している場合、このフィールドの意味は未定義です。

  * `home_street` （Unicode文字列、任意）
    * 人物の住所の通り名。個人的な情報を保護するため、アプリケーション一般的には通りの番号を含めるべきではありません。

  * `home_neighborhood` （Unicode文字列、任意）
    * 人物の住所の町名。他のアドレスフィールドに入力されていない公式または非公式な地理情報を入力してください。

  * `home_city` （Unicode文字列、任意）
    * 人物の住所の市町村

  * `home_state`（Unicode文字列、任意）
    * 人物の住所の都道府県または州名。大文字のISO 3166-2コード（推奨）もしくは、一般的に使われる名称。

  * `home_postal_code` (ASCII文字列、任意）
    * 人物の郵便番号。その国で使われる一般的なフォーマットで入力します。

  * `home_country` (ASCII ISO-3166-1 カントリーコード、任意）
    * 人物の出身国です。大文字二文字のISO-3166-1カントリーコードを用います。

  * `photo_url` (URL文字列、任意）
    * 人物を特定するイメージのURLです。

  * profile\_urls (URL文字列、任意）
    * 他のウェブサイト上の人物のプロフィールへのURLです。複数のURLがある場合は改行文字 (Unicode U+000A)でURLを区切ります。


## NOTEレコード ##

それぞれのNOTEはたったひとつのPERSONレコードに対応します。１つのPERSONレコードに対し、複数の関連するNOTEレコードがある場合もあります。(詳しくは下記の実装上の注意を参照してください。データベースを使う場合は、person\_record\_idを外部キーとし、ノートレコードとパーソンレコードを関連付けるかもしれませんし、オブジェクト型で表現する場合は、パーソンレコードが複数のノートレコードを保持するという形で実装するかもしれません。

NOTEレコードは行方不明者の現在情報を提供するのに用いられます。どのNOTEもタイムスタンプと投稿者の情報を持っています。アプリケーションはこのタイムスタンプを用いて、特定フィールドの最新の値を知ることができます。ユーザーは投稿者情報を知ることでその信憑性を確認出来ます。

_レコードに関するメタデータ（8項目）_

  * `note_record_id` (ASCII文字列。必須）
    * このレコードのユニーク識別子です。ドメイン名に続くスラッシュとローカル識別子で成り立ちます。ドメインネームはこのレコードへの権限を持つホームレポジトリを識別します。ローカル識別子のフォーマットはホームレポジトリによって違います。`note_record_id`がアプリケーション自体のドメインとは違うもので始まる場合、そのレコードは別ソースからのクローンであることを意味します。

  * `person_record_id` (ASCII文字列。必須）
    * このNOTEが属するPERSONレコードの `person_record_id`。

  * `linked_person_record_id` (ASCII文字列、任意）
    * このNOTEの属するPERSONレコードに関連づける別のPERSONレコードの `person_record_id`。NOTEの `author` が `person_record_id` と `linked_person_record_id` で識別される二つのレコードが同一人物を指している、と考える場合にこのフィールドが作製されます。どのような経緯でこれらのレコードが同一人物を言及するものであると考えられるかが `text` フィールドに書かれます。

  * `entry_date` (ASCII文字列”yyyy-mm-ddThh:mm:ssZ”形式、任意）
    * このデータのコピーが保存された日時（UTC）。クライアントが最後に受信したレコードの `entry_date` より大きいか同じ値の `entry_date` をもつすべてのレコードをクエリすることで、クライアント側のコピーをアップデートできるようにするため、PFIFレポジトリはレコードが加えられるにつれ、この値が単調に増加することを保証しなくてはなりません。

  * `author_name` (Unicode文字列。必須）
    * このNOTEを入力した人のフルネーム。

  * `author_email` (Eメールアドレス文字列、任意）
    * このNOTEを入力した人のEメールアドレス。

  * `author_phone` (ASCII文字列、任意）
    * このNOTEを入力した人の電話番号。

  * `source_date` (ASCII文字列”yyyy-mm-ddThh-mm-ssZ”。必須）
    * このNOTEのオリジナルコピーがホームレポジトリに作製された日時（UTC）。通常NOTEはこのフィールドをもとに並び替えられ表示される。

_行方不明者の現在の状況　(6項目)_

`author_made_contact`、 `status`、 `email_of_found_person`、`phone_of_found_person` そして `last_known_location` は変化し得る情報を保管します。これらのフィールドがNOTEレコードに存在する場合、そのレコードはこれらフィールドに対し新しい値を指定しており、`source_date` がそれらの新しい値が有効になった日時を示します。例えば、最新の所在地を表示したいアプリケーションは `last_known_location` が空欄ではない最新の `source_date` を持ったNOTEを探せば良いのです。

  * `author_made_contact` (ASCII文字列、任意）
    * もし投稿者が行方不明者にコンタクトをとった場合、この文字列の値はtrueに、それ以外の場合はfalseとなります。もしこのフィールドがtrueの場合、NOTEは人物がいつどこで目撃または接触されたかを記述します。

  * `status` (ASCII文字列、任意）
    * 目撃または発見された人物のステータスは次の５つの文字列によって特定されます。
      * `information_sought`
        * 投稿者はその人物に関する情報を探している
      * `is_note_author`
        * 投稿者自身がその人物である。
      * `believed_alive`
        * 投稿者はその人物は生きているという情報を入手した
      * `believed_missing`
        * 投稿者はその人物が依然として行方不明であると判断する理由がある。
      * `believed_dead`
        * 投稿者はその人物が死亡したという情報を入手した

  * `email_of_found_person` (Eメールアドレス文字列、任意）
    * 発見された人物のEメールアドレス。その人物が発見された場合にのみ、このフィールドを入力してください。もしこのフィールドが入力されている場合、どのようにこの人物に連絡をとれば良いかが `text` フィールドに書いてあるはずです。

  * phone\_of\_found\_person (ASCII文字列、任意）
    * 発見された人物の電話番号。その人物が発見された場合にのみ、このフィールドを入力してください。もしこのフィールドが入力されている場合、どのようにこの人物に連絡をとれば良いかがtextフィールドに書いてあるはずです。

  * `last_known_location` (Unicode文字列、任意）
    * その人物が最後にいた場所、状況を自由形式で記述。このフィールドの地理座標を指定する場合、まず緯度を十進法で表し(北が正）、コンマ、そして経度を同じく十進法で入力してください（東が正）。

  * `text` (Unicode文字列。必須）
    * 人物の現在の健康状態、環境、最後に目撃された場所の詳細、情報変更などの自由形式の記述です。入力フォームにはマルチラインテキストボックスがこのフィールドには適当です。

  * `photo_url` (URL文字列、任意）
    * このNOTEに含まれる画像へのURL


# XMLフォーマット仕様 #

PFIFのXML名前空間:
  * http://zesty.ca/pfif/1.4

PFIFドキュメントのMIMEタイプ:
  * `application/pfif+xml`

有効なPFIF XMLドキュメントは１つ以上のPERSONかNOTEの要素を含んだ単独のPFIFエレメントから成っています。さらに、その要素のそれぞれが上記のフィールドの子要素を含みます。例えば、PERSONエレメントでは`person_record_id`、`source_date` そして `full_name` のフィールドは必須です。NOTEエレメントでは、`note_record_id`、`author_name` そして `source_date` のフィールドが必須です。他のすべてのフィールドは任意です。PERSONやNOTEエレメントの内部にある子要素の順番は自由です。

NOTEエレメントはPERSONエレメントの内側か外側に存在することが出来ます。NOTEエレメントが外側の場合、それは `person_record_id` を含んでいなくてはなりません。そうでない場合、`person_record_id` は任意で、もし存在する場合は入力された人物の `person_record_id` と一致していなくてはなりません。

[RELAX NG コンパクトシンタックス](http://relaxng.org/compact-20021121.html) で書かれた PFIF の [RELAX NG](http://relaxng.org/) スキーマは以下の通りです

```
namespace pfif = "http://zesty.ca/pfif/1.4"

start = element pfif:pfif { person* & note* }

person = element pfif:person {
    *element pfif:person_record_id { record_id }* &
    element pfif:entry_date { time } ? &
    element pfif:expiry_date { time } ? &
    element pfif:author_name { text } ? &
    element pfif:author_email { email } ? &
    element pfif:author_phone { phone } ? &
    element pfif:source_name { text } ? &
    element pfif:source_date { time } &
    element pfif:source_url { url } ? &
    element pfif:full_name { text } &
    element pfif:given_name { text } ? &
    element pfif:family_name { text } ? &
    element pfif:alternate_names { text } ? &
    element pfif:description { text } ? &
    element pfif:sex { sex } ? &
    element pfif:date_of_birth { approx_date } ? &
    element pfif:age { approx_age } ? &
    element pfif:home_street { text } ? &
    element pfif:home_neighborhood { text } ? &amp;
    element pfif:home_city { text } ? &
    element pfif:home_state { text } ? &
    element pfif:home_postal_code { text } ? &
    element pfif:home_country { country_code } ? &
    element pfif:photo_url { url } ? &
    element pfif:profile_urls { text } ? &
    note*
}

note = element pfif:note {
    element pfif:note_record_id { record_id } &
    element pfif:person_record_id { record_id } ? &
    element pfif:linked_person_record_id { record_id } ? &
    element pfif:entry_date { time } ? &
    element pfif:author_name { text } &
    element pfif:author_email { email } ? &
    element pfif:author_phone { phone } ? &
    element pfif:source_date { time } &
    element pfif:author_made_contact { boolean } ? &
    element pfif:status { status } ? &
    element pfif:email_of_found_person { email } ? &
    element pfif:phone_of_found_person { phone } ? &
    element pfif:last_known_location { text } ? &
    element pfif:text { text } &
    element pfif:photo_url { url } ?
}

record_id = xsd:string { pattern = ".+/.+" }
time = xsd:dateTime { pattern = "\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z" }
email = xsd:string { pattern = ".+@.+" }
phone = xsd:string { pattern = "[\-+()\d ]+" }
url = text
sex = "female" | "male" | "other"
approx_date = xsd:string { pattern = "\d\d\d\d(-\d\d(-\d\d)?)?" }
approx_age = xsd:string { pattern = "\d+(-\d+)?" }
country_code = xsd:string { pattern = "[A-Z][A-Z]" }
boolean = "true" | "false"
status = "information_sought" | "is_note_author" |
    "believed_alive" | "believed_missing" | "believed_dead"
```


# Atomフィード仕様 #
PFIF XMLドキュメントは [Atom 1.0](http://www.atomenabled.org/developers/syndication/atom-format-spec.php) フィードに埋め込みが可能です。XML名前空間を用いてPFIFドキュメントを埋め込み、entryエレメントの直接の子要素として挿入してください。

Atom 1.0は複数の entry エレメントを含む、トップレベルのフィードエレメントを定義します。トップレベルエレメントはPFIF名前空間を指定しなくてはなりません。推奨されるプリフィックスは `pfif` で、トップレベルエレメントはこのようになるでしょう

```xml

<feed xmlns="http://www.w3.org/2005/Atom"
xmlns:pfif="http://zesty.ca/pfif/1.4">
...


Unknown end tag for &lt;/feed&gt;


```


本セクションでは、既存のフィードリーダーで読み込めるように、アプリケーションがどのように標準Atomエレメントを埋めるべきかについて説明します。それでもなお、埋め込まれたPFIFドキュメントはAtomエレメントに現れる重複した情報より優先されます。

ここでは２種類のPFIF Atomフィードを定義します。それぞれのエントリーが人物を含むものはPERSONフィード、NOTEを含むものはNOTEフィード呼ばれます。PERSONフィードはブログエントリーを含んだブログフィードに例えられ、NOTEフィードはある１つのブログエントリーのコメントフィードに例えられるでしょう。例えば、他のデータベースから行方不明者記録を集めるためにアプリケーションがPERSONフィードを購読することもあれば、別のアプリケーションは特定人物に関する一連のアップデートNOTEを表示するためにNOTEフィードを購読する、ということもあるのです。

## Atom PERSONフィード ##
Atom PERSONフィード内の feed エレメントでは、最低でも以下のエレメントが提供する必要があります。

  * `id`
    * このエレメントはフィードと関連するユニークなURIを表します。これはフィードを提供するデータベースのウェブサイトやサービスへのURLである場合もあります。

  * `title`
    * このエレメントはフィードの名前を表します。このフィードを提供するデータベースやサービスのタイトルを含んでいるでしょう。

  * `subtitle`
    * このエレメントはフレーズやフィードを説明する文などを表します。このフィードがなぜ作製されたかを説明する場所でもあります。例としては `“Scraped daily by FooMatic 2.3 from http://example.org/”` のような文字列です。

  * `updated`
    * このエレメントはフィードが最後にアップデートされた日付をUTCフォーマット”yyyy-mm-ddThh:mm:ssZ”で表します。

  * `link`
    * このエレメントはフィードの取得されたURLを表します。これはrel属性の値selfを持ちます。

Atom PERSONフィードはそれぞれのentryエレメントに最低でも以下の要素を含みます

  * `pfif:person`
    * このエレメントは `person_record` の子要素および０個以上の `pfif:note` エレメントを含みます。完全なエクスポートを提供するサービスはここに人物に関連したすべてのNOTEレコードも含むでしょう。

  * `id`
    * このエレメントはスキーム名”pfif:” と後に続く `person_record_id` の値で構成されるURI文字列を持ちます。

  * `title`
    * このエレメントは `full_name` フィールドの値を持ちます。

  * `author`
    * このエレメントは `author_name` フィールドの値を持った `name` エレメントと `person_record` の `author_emai` lフィールドの値を持った `email` エレメントを含みます。

  * `updated`
    * このエレメントは `person` レコードの `source_date` の値を持ちます。

  * `content`
    * このエレメントは `person` レコードを可読形式の `html` でフォーマットしたものを含みます。内容をどうフォーマットするかはアプリケーション次第です。

  * `source`
    * このエレメントはフィードの `title` エレメントのコピーです。

## Atom NOTEフィード ##

Atom NOTE フィード内の feed エレメントでは、最低でも以下のエレメントが提供されます。

  * `id`
    * このエレメントはフィードに一意に関連づけられたURIを含みます。このフィードを提供しているデータベースやウェブサイトへのURLである場合もあります。

  * `title`
    * この要素はフィードの名前を含みます。データベースの名前やこのフィードを提供しているサービスの名前に続いて、どのようにNOTEがデータベースやサービスから抽出されたかを述べる詳しいタイトルも含みます。例えば、ある特定の人物へのNOTEフィードの場合、タイトルは、サービスの名前と人物の姓名から構成することができます。

  * `subtitle`
    * このエレメントはこのフィードに関する単語や文を含みます。このフィードがなぜ作製されたかをここで記述してください。例えば `“Exported by CiviCRM 1.1, http://www.example.org/”` などの文字列がそれに当たります。

  * `updated`
    * このエレメントは ”yyyy-mm-ddThh-mm-ssZ” フォーマットで、このフィードが最後にアップデートされた日付（UTC）を含みます。

  * `link`
    * このエレメントはフィードが取得されたURLを含みます。これは値がselfのrel属性を持ちます。

Atom NOTEフィード内のentryエレメントでは、最低でも以下のエレメントが提供されます。

  * `pfif:note`
    * この要素はNOTEレコードのフィールドに対応する子要素を含みます

  * `id`
    * この要素はスキーム名"pfif:"と `person_record_id` の値で構成されるURI文字列を含みます。この要素はpfifスキームで成り立つURI文字列とそれに続く `note_record_id` の値を含みます

  * `title`
    * この要素は `text` フィールドの抜粋を含みます。

  * `author`
    * この要素はNOTEレコード内の `author_name` の値を含む `name` 要素と `author_email` の値を含む `email` 要素を含みます。

  * `updated`
    * この要素はNOTEレコードの `source_date` フィールドの値を含みます。

  * `content`
    * この要素はNOTEレコードの html形式の `text` フィールドを含みます。内容のフォーマット方法はアプリケーションにより異なります。


# RSS フィード仕様 #
PFIF XMLドキュメントは [RSS 2.0](http://cyber.law.harvard.edu/rss/rss.html) フィードに埋め込み可能です。(RSS2.0の用語ではこのセクションはRSS 2.0モジュールと定義づけられます。）PFIFドキュメントはXML名前空間を用いて指定され、item要素の直接の子要素として埋め込まれます。

RSS 2.0 は二つのメイン要素をもち、トップレベルrss要素に内包されるchannel とitemを定義します。トップレベル要素はPFIF名前空間を宣言します。推奨されるプリフィックスは `pfif` で、トップレベル要素は以下のようになるでしょう

```xml

<rss version="2.0" xmlns:pfif="http://zesty.ca/pfif/1.4">
...


Unknown end tag for &lt;/rss&gt;


```

残りのセクションではアプリケーションがどうやって標準RSS要素を追加し、フィードを既存のフィードリーディングソフトウェアで機能させるかについて述べます。しかし、埋め込まれたPFIFドキュメントはRSS要素に現れるいかなる重複情報より優先されます。

最初にある通り、ここでは二つのPFIF RSSフィードが定義づけられています。人物を含むPERSONフィード、NOTEを含むNOTEフィードです。

## RSS PERSONフィード ##
RSS PERSONフィードは少なくとも以下の要素をchannel要素内で提供します。

  * `title`
    * この要素はフィード自体の名前と、フィードを提供しているデータベースやサービスの名前を含みます。

  * `description`
    * この要素はフィードを説明する言葉や文を含みます。ここでフィードが作製された理由を説明します。例えば  `“Scraped daily by FooMatic 2.3 from http://example.org/”` といった文字列がそれにあたります。

  * `lastBuildDate`
    * この要素は [RFC 822](http://www.ietf.org/rfc/rfc0822.txt) フォーマットで、最後にアップデートが行われたUTCでの日時を含みます。例えば “Sat, 07 Sep 2002 00:00:01 GMT”。

  * `link`
    * この要素はフィードを提供するデータベースやサービスへのURLを含みます。

RSS PERSONフィードは少なくとも以下の要素をitem要素の中で提供します。

  * `pfif:person`
    * この要素はPERSONレコードのフィールドの子要素および０以上の `pfif:note` 要素を含みます。サービスが完全なエクスポートをする場合、この人物に関連するすべてのNOTEレコードを含むでしょう。

  * `guid`
    * この要素は `person_record_id` フィールドの値を含むでしょう。

  * `title`
    * この要素は `full_name` フィールドの値を含むでしょう。

  * `author`
    * この要素は `author_email` フィールドの値、その後にスペース、そしてその後に `author_name` フィールドの値を丸括弧に入れたものを含みます。

  * `pubDate`
    * この要素はPERSONレコードの `source_date` フィールドの日付を[RFC 822](http://www.ietf.org/rfc/rfc0822.txt)フォーマット、例えば”Sat, 07 Sept 2002 00:00:01 GMT”、に変換したものを含みます。タイムゾーンはGMTで西暦は４桁でなければなりません。

  * `description`
    * この要素はPERSONレコードの情報を目視可能なHTMLフォーマットにしたものが含まれます。内容をどのようにフォーマットするかはアプリケーション次第です。

  * `source`
    * この要素は `source_name` フィールドの値を含みます。

  * `link`
    * この要素は `source_url` の値を含みます。

## RSS NOTEフィード ##

RSS NOTEは `channel` 要素内で以下の要素を提供します。

  * `title`
    * この要素はフィード名を含みます。データベースの名前やこのフィードを提供しているサービスの名前に続いて、どのようにNOTEがデータベースやサービスから抽出されたかを述べる詳しいタイトルも含みます。例えばある特定の人物へのNOTEフィードの場合、使用されるサービスの名前、それに続いて人物の姓名からタイトルは構成されます。

  * `description`
    * この要素はフィードを説明するフレーズや文を含みます。このフィードがなぜ作製されたかを説明する場所でもあります。たとえば `“Scraped daily by FooMatic 2.3 from http://example.org/”` といった文字列がその例です。

  * `lastBuildDate`
    * この要素は[RFC 822](http://www.ietf.org/rfc/rfc0822.txt)フォーマットで、フィードが最後にアップデートされたUTCでの日付と時間を含みます。例えば、”Sat, 07 Sep 2002 00:00:01 GMT”

  * `link`
    * この要素はフィードを提供するデータベースやサービスに対応するウェブサイトへのURLを含みます。特定人物に関するNOTEフィードの場合、このリンクはPERSONレコードのwebページを指定することも可能です。

RSS NOTEは `item` 要素内で以下の要素を提供します。

  * `pfif:note`
    * この要素はNOTEレコードのフィールドの子要素を含みます。

  * `guid`
    * この要素は `note_record_id` フィールドの値を含みます。

  * `author`
    * この要素は `author_email` フィールドの値、その後にスペース、その後に `author_name` フィールドの値を丸括弧に入れたものを含みます。

  * `pubDate`
    * この要素はNOTEレコードの `source_date` フィールドの日付が[RFC 822](http://www.ietf.org/rfc/rfc0822.txt)フォーマットに変換されたもの、例えば ”Sat, 07 Sep 2002 00:00:01 GMT” を含みます。タイムゾーンはGMTで西暦は４桁でなければなりません。

  * `description`
    * この要素はNOTEレコード内のtextフィールドのHTMLフォーマットを含みます。内容をどのようにフォーマットするかはアプリケーション次第です。


# リレーショナルデータベーススキーマの例 #
このセクションではPFIFデータを保存するために可能なリレーショナルデータベーススキーマを紹介します。データベースデザインの正確な詳細はそれぞれのアプリケーションによって異なりますから、これは最初の一歩に過ぎません。リレーショナルデータベースは二種類の `person と `note` をそれぞれ別のテーブルでPFIFレコードをストアできます。

```
PERSON table:
     string      person_record_id           primary key
     datetime    entry_date
     datetime    expiry_date
     string      author_name
     string      author_email
     string      author_phone
     string      source_name
     datetime    source_date
     string      source_url
     string      full_name
     string      given_name
     string      family_name
     string      alternate_names
     text        description
     string      sex
     string      date_of_birth
     string      age
     string      home_street
     string      home_neighborhood
     string      home_city
     string      home_state
     string      home_postal_code
     string      home_country
     string      photo_url
     string      profile_urls

NOTE table:
     string      note_record_id             primary key
     string      person_record_id           foreign key not null
     string      linked_person_record_id    foreign key or null
     datetime    entry_date
     string      author_name
     string      author_email
     string      author_phone
     datetime    source_date
     boolean     author_made_contact
     string      status
     string      email_of_found_person
     string      phone_of_found_person
     string      last_known_location
     text        text
     string      photo_url
```


外部の `person` レコードとローカルのレコードをリンクする場合、アプリケーションはローカル `person` レコードに関する `note` を、外部レコードの `person_record_id` を含む `linked_person_record_id` フィールドに加えます。NOTEの他のフィールドはマージの経緯を説明します。`source_date` はこれが決定された日付、`text` で決定理由、そして `author_name` は決定を下した人物、プログラム、その他のエンティティの名前を含みます。この仕様はアプリケーションがどのように二つのレコードをマージさせるかを指示するものではありません。マージは人間の操作主もしくは類似データを探し出すソフトウェアアルゴリズムによって引き起こされる場合があります。マージの決定を `note` レコードに記述しておくことは、誤ったマージのやり直しを可能にし、`author_name` フィールドに人名もしくはプログラム名を残しておくことで、不確かなマージの原因を突き止めることが出来ます。

`person` レコードを表示するとき、アプリケーションはその `person` レコードと関係するノートの中から、`linked_person_record_id` フィールドをすべて探し出し、すべてのリンクレコードやマージされたリンクレコードを表示することが出来ます。


# 以前のバージョンからの変更点 #

## PFIF 1.1からPFIF 1.2への変更点 ##
PERSONレコードには `sex`、`date_of_birth`、`age`、`home_country` と４つの新しいフィールドが加わりました。`home_zip`フィールドは `home_postal_code` と置き換えられました。PFIF1.1レポジトリからアップグレードするには、古い `home_zip` の値を `home_postal_code` フィーエルドにエクスポートし、レコードの`home_state` が
アメリカの州名もしくは `home_postal_code` フィールドが米国の郵便番号を含むものについては、`home_country` フィールドを US とセットしてください。

`note`レコードには`person_record_id`、`linked_person_record_id`、そして`status`の３つのフィールドが加わりました。

PFIF XMLフォーマットでは`note`要素が`person`要素の外で使えるようになりました。初めに現れなければならなかった`note_record_id`と`person_record_id`フィールドを除いて、残りの子要素は順番の制限がなくなりました。

Atom entryとRSS itemは独立した`pfif:person`と`pfif:note`要素を`pfif:pfif`要素の追加なしで含めるようになりました。

## PFIF1.2からPFIF1.3への変更点 ##
PERSONレコードの`source_date`フィールドが必須になりました。レコードはオリジナルレポジトリによってのにアップデートされ、レコードに変更がある場合は`source_date`も変更されなければなりません。

PERSONレコードに必須の `full_name` フィールドが加わりました。`first_name` と `last_name` は任意になりました。

PERSONレコードに `expiry_date` フィールド、データ削除および伝達の必要事項が加えられました。

PFIF XMLフォーマットでは、`person`と`note`要素のすべての子要素がどのような順序でも良くなりました。

## PFIF1.3からPFIF1.4への変更点 ##
PERSONレコードにオプションの `alternate_names` と `profile_urls`が加えられました。

PERSONレコードの `first_name` が `given_name` に、`last_name` が `family_name` に名称変更されました。

PERSONレコードの`other`フィールドが`description`フィールドに置き換えられました。

NOTEレコードに`photo_url`フィールドが加えられました。

NOTEレコードの`found`フィールドが`author_made_contact`に名称変更されました。

NOTEレコードの`last_known_location`フィールドの地理座標の特定に新たな約束事が加わりました。


---


# 謝辞 #
PFIFの元となるものの原型は以下の人々によって作られました。
The CiviCRM team, David Geilhufe, Kieran Lal, Luke Blanshard, Tony Chang, Josh Kleinpeter, Kieran Lal, Jonathan Plax, Gabe Wachob, Ka-Ping Yee, Steve Hakusa, Mark Prutsalis, Lee Schumacher, the Missing Persons Community of Interest　(tci\_missingpersons@googlegroups.com),  そして現在も活動するグループリストの他の参加者 (pfif@googlegroups.com) が今日のPFIFデザインに貢献してくれました。