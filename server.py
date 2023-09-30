from flask import Flask, jsonify, request
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import numpy as np
app = Flask(__name__)
# http://127.0.0.1:5000/check_domain?domain=vk.com/fix_price
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
os.environ['CURL_CA_BUNDLE'] = ''


def parser(domain):
    url = f'http://{domain}'
    
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}

    #response = requests.get(url, verify=False)
    response = session.get(url, verify=False,  headers=header, timeout=30)
    if response.status_code == 200:

        response.encoding = 'utf-8'
        soup = BeautifulSoup((response.text), 'html.parser')
        text = soup.get_text()
        return text
    else:
        url = f'https://{domain}'
        response = session.get(url, verify=False,  headers=header)
        if response.status_code == 200:
          
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            return text
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
        return jsonify({'error': 'Параметр domain отсутствует в запросе'})

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)


