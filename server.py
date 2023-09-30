from flask import Flask, jsonify, request

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
    url = f'https://{domain}'
    
    session = requests.Session()
    
    
    #time.sleep((20-5)*np.random.random()+5)
    session.headers  = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #'accept-encoding': 'gzip, deflate, br', # удалите эту строку
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; BNTV600 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36'}

    #response = requests.get(url, verify=False)
    response = session.get(url, verify=False,  proxies={"http": "http://111.233.225.166:1234"})
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
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)


