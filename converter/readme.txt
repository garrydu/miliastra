
Genshin Impact UGC File Converter

  原神 (Genshin Impact) のUGC関連ファイルを .gil / .gia ⇔ .json 形式で相互変換するコンソールアプリです。


使い方

  UgcFileConverter.exe [オプション] 入力ファイル名

  オプション一覧
  -d デコードモード： .gil / .gia → .json に変換
  -e エンコードモード： .json → .gil / .gia に変換
  -o 出力ファイル名: 出力ファイル名を指定（デフォルト: output.json, output.gil, output.gia）
  -t dtypeファイル名: dtypeファイルを指定（デフォルト: dtype.json）

  デコードモードやエンコードモードが指定されてない場合は、入力ファイルの拡張子から自動で判別されます。


使用例

  デコード例
  UgcFileConverter.exe sample.gil
  → output.json が生成されます。

  エンコード例
  UgcFileConverter.exe -o mydata.gil data.json
  → mydata.gil が生成されます。


ライセンス
  本ソフトウェアは MITライセンス のもとで公開されています。
