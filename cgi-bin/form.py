#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import steganography
import sys

form = cgi.FieldStorage()
image_path = form['photo'].filename
text_path = form['text'].filename
secret_word = form.getfirst("password", "default123")
image_decode_path = form['photo1'].filename
secret_word_decode = form.getfirst("password1", "default123")

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>txt to png</title>
        </head>
        <body>""")

if image_path != '' and text_path != '':
    result = steganography.txt_to_png(image_path, text_path, secret_word, 'new_' + image_path)
    if result == u'Успешно':
        data_uri = open(image_path, 'rb').read().encode('base64').replace('\n', '')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        print('без информации:')
        print(img_tag)
        data_uri = open('new_' + image_path, 'rb').read().encode('base64').replace('\n', '')
        data_uri = open(image_path, 'rb').read().encode('base64').replace('\n', '')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        print('с информацией:')
        print(img_tag)
    else:
        print result

if image_decode_path != '':
    result = steganography.txt_from_png(image_decode_path,secret_word_decode)
    result = result.split('\n')
    print """<p>Текст:</p>"""
    for row in result:
        print "<br>"
        print row
print """
<form method=post action="/cgi-bin/form.py" enctype="multipart/form-data">
    <h1>Текст в изображение:</h1>
    <p>Загрузите фотографию:</p>
    <p><input type="file" name="photo" multiple accept="image/*,image/png">
    <p>Загрузите текстовый файл:</p>
    <p><input type="file" name="text" multiple accept="text/*">
    <p><strong>Пароль:</strong>
    <input type="password" maxlength="25" size="40" name="password"></p>
    <input type="submit" value="Отправить"></p>
    <h1>Текст из изображения:</h1>
    <p>Загрузите фотографию:</p>
    <p><input type="file" name="photo1" multiple accept="image/*,image/png">
    <p><strong>Пароль:</strong>
    <input type="password" maxlength="25" size="40" name="password1"></p>
    <input type="submit" value="Отправить"></p>
</form>"""

print """</body>
        </html>"""
