import json
import os
from flask import Flask, render_template, request, make_response, send_from_directory
import requests

app = Flask(__name__)
LDAP_URL = os.environ['LDAP_URL']

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('/templates', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def hello():
    name = "move"
    return render_template('hello.html', title='flask test', name=name) 


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ""
    if request.method == 'POST':
        headers = {"content-type": "application/json"}
        payload = {'userid': request.form['username'], 'passwd': request.form['password']}
        r = requests.post(LDAP_URL, headers=headers, data=json.dumps(payload))
        print(r.text)
        print(r.status_code)
        response = None
        if r.status_code == 200:
            response = make_response(
                render_template('login_result.html',
                                login_status="成功",
                                transfer_url="https://ca.labo.local/"
                                )
            )
            response.set_cookie('Authorization',
                                value=r.headers['Authorization'],
                                max_age=3600,
                                secure=True,
                                samesite=None,
                                domain="labo.local",
                                path="/"
                                )
        else:
            response = make_response(render_template('login.html', error="ログイン失敗"))
        return response 
        
    # Login form を表示
    return render_template('login.html', error=error)


## メイン
if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0')
  

