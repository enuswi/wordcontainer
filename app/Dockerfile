# ベースイメージ
FROM python:3.6

RUN mkdir /var/www
# workdirの指定
WORKDIR /var/www

# 依存Pythonライブラリ一覧コピー
COPY requirements.txt ./

# 依存Pythonライブラリインストール
RUN pip install --no-cache-dir -r requirements.txt

# 依存パッケージのインストール
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update && apt-get install -y \
    nodejs

# LESS
RUN npm install -g less

WORKDIR /var/www/src

CMD ["uwsgi","--ini","/var/www/uwsgi.ini"]
