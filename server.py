﻿from flask import Flask, jsonify, request
app = Flask(__name__)
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
def parser(domain):
    url = f'https://{domain}'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return(text)
    else:
        return(f"Ошибка при запросе: {response.status_code}")
#www.gotennis.ru/
@app.route('/check_domain', methods=['GET'])
def check_domain():
    domain = request.args.get('domain')

    if domain:
        result = parser(domain)
        return jsonify(result)
    else:
        return jsonify({'error': 'Параметр domain отсутствует в запросе'}), 400

if __name__ == '__main__':
    app.run(debug=True)


