# 以下エントリーを参照させていただき作成
https://qiita.com/trrrrrys/items/a905f1382733dfb9c8c1

## 下ごしらえ
Docker for macのインストール

上記エントリー主の方が作成したgithubのURL。

こちらから、git clone

https://github.com/lboavde1121/flaskapp

※ Windowsに関しては未検証。

## カスタマイズ
* テンプレートには、jinja2を使用する
* スタイルシートは、LESSファイルを使用する
* knockout.jsを使用する
* mysqlを使用する

app/Dockerfile
```
Lessファイルをコンパイルする為にnodejsをインストール
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update && apt-get install -y \
    nodejs

コンパイルの為に、lessをインストール
RUN npm install -g less
```

#### LESSファイルコンパイル
```
# .cloyster/less.sh
パルシェンでの実行に変更
```

#### knockout.js
vue.jsとjinja2を併用する為にdelimiterをカスタマイズする必要がある。

※ 詳しくは、app/src/run.pyを参照

## docker-compose.ymlの変更
uwsgiのポート番号だけ変更した。(80は既に使ってたから)

## 起動
```
# make run
```
## 停止
```
# make stop
```

# 構成
```
.
├── Makefile
├── README.md
├── app
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   └── default.py
│   │   ├── run.py
│   │   ├── templates (追加要素)
│   │   │   └── layout.html  -> 基本のレイアウト
│   │   │   └── main.html    -> 基本のレイアウトを継承して、作成
│   │   │   └── noroute.html -> 404ページ用
│   │   ├── static (追加要素)
│   │   │   └── css
│   │   │       ├── layout.css
│   │   │   └── less
│   │   │       ├── layout.less
│   │   │   └── favicon.ico
│   │   ├── server
│   │   │   ├── __init__.py
│   │   │   └── hoge
│   │   │       ├── __init__.py
│   │   │       └── hoge_api.py
│   │   └── tests
│   │       ├── __init__.py
│   │       └── test_hoge.py
│   └── uwsgi.ini
├── docker-compose.yml
└── nginx
    ├── Dockerfile
    └── nginx.conf
```

# 今後の展望
1. LESSファイルのコンパイル自動化
2. 単体テスト実装
3. レスポンシブデザイン
4. ログイン