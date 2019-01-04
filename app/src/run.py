#!/usr/bin/python
# -*- coding: utf-8 -*-

# [Import start]
#from server import app
import os
from flask import Flask, render_template, send_from_directory

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
# [Import end]

# favicon設定
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# staticルート設定
@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), path)
"""
render_templateへの引数
1. テンプレートファイル
2. ページタイトル
3. ユーザー名
4. コンテンツタイトル
"""
# 404ページ
@app.errorhandler(404)
def error_handler(error):
    """
    abort(404)時にレスポンスをレンダリングするハンドラ
    :param error:
    :return:
    """
    msg = 'Error: {code}\n'.format(code=error.code)
    return render_template(
        'noroute.html',
        title = msg,
        headingContent = msg,
        code = error.code
    )
    return msg, error.code

# 正常ページのルーティング
@app.route('/')
def main():
    title = "Word Container"
    return render_template(
        'main.html',
        title = title,
        headingContent = title,
        action = 'add'
    )

if __name__ == '__main__':
    app.run(debug=True)
