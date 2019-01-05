# flaskでwebサービスを作りたい！

## 準備
・Docker for macのインストール

※ Windowsに関しては未検証。

## 使いたい技術
* テンプレートには、jinja2を使用する
* スタイルシートは、LESSファイルを使用する
* knockout.jsを使用する
* mysqlを使用する(SQLAlchemy使いたい)

### テンプレートには、jinja2を使用する
requirements.txt
```
jinja2==2.10
```

app/run.py
```
# jinja2とvue.jsを併行して使用できるように、jinjaのテンプレート識別子を変更
# このプロジェクトでは、vue.jsではなくknockoutJsを使用するがめんどくさいので変更しない
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))

app = CustomFlask(__name__)
```

### スタイルシートは、LESSファイルを使用する
app/Dockerfile
```
Lessファイルをコンパイルする為にnodejsをインストール
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update && apt-get install -y \
    nodejs

コンパイルの為に、lessをインストール
RUN npm install -g less
```
#### コンパイル方法
```
# lessc static/less/layout.less static/css/layout.css

# .cloyster/less.sh ← 今はこれ
cloyster?そう、パルシェンのことさ！
```
#### TODO
* ファイル指定では無く、フォルダ指定(lessフォルダ以下の.lessファイルをコンパイルするように修正)

### knockout.jsを使用する
個人的な趣味で使います。
公式からminファイルをDLしてきて、static/js以下に配置

layout.html(テンプレートのベースとして用意)
```
    <head>
        <meta charset="UTF-8">
        (% block head %)
        <script src="/js/layout.js"></script>
        <script type="text/javascript" src="/js/knockout-min3.4.2.js"></script> ここでminファイルを読み込む
        (% block script %)(% endblock %)
```

#### TODO
minファイルの位置はここでいいのか？

### mysqlを使用する(SQLAlchemy使いたい)

全体の構成については、下記のエントリーを参考にさせていただいています。(ほぼほぼおんぶに抱っこ状態です。)
https://qiita.com/trrrrrys/items/a905f1382733dfb9c8c1

mysqlのコンテナについてはこちらの構成に追加する形で行なっています。

mysql/Dockerfile
```
FROM mysql:5.7
EXPOSE 3306

ADD ./my.cnf /etc/mysql/conf.d/my.cnf

CMD ["mysqld"]
```

mysql/my.cnf
```
[mysqld]
character-set-server=utf8

[mysql]
default-character-set=utf8

[client]
default-character-set=utf8
```

#### docker-compose.ymlの変更

```
version: "2"
services:
  # ここから
  mysql:
    build: ./mysql/
    volumes:
      - ./mysql/mysql_data:/var/lib/mysql
      - ./mysql/sqls:/docker-entrypoint-initdb.d
    environment:
      - MYSQL_ROOT_PASSWORD=hogehoge
  # ここまで

  uwsgi:
    build: ./app
    volumes:
      - ./app:/var/www/
    ports:
      - "3031:3031"
    environment:
      TZ: "Asia/Tokyo"
    links:
      - mysql　← 追加

  nginx:
    build: ./nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    links:
      - uwsgi
    ports:
      - "81:80"
    environment:
      TZ: "Asia/Tokyo"

```

#### Makefileの変更
```
NAME=wordcontainer

run:
	docker-compose build
	docker-compose up -d

stop:
	docker stop ${NAME}_uwsgi_1 ${NAME}_nginx_1 ${NAME}_mysql_1
	docker rm ${NAME}_uwsgi_1 ${NAME}_nginx_1 ${NAME}_mysql_1
```
* docker stop, docker rm にそれぞれ　${NAME}_mysql_1を追加
* NAMEをリポジトリの名前に修正

#### 起動
```
# make run
```
#### 停止
```
# make stop
```

#### TODO
restartが欲しい

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
├── mysql
│   ├── Dockerfile
│   ├── my.cnf
│   └── sqls
└── nginx
    ├── Dockerfile
    └── nginx.conf
```

## 参考
https://qiita.com/trrrrrys/items/a905f1382733dfb9c8c1
