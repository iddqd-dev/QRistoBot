import hashlib
import hmac
import os
from flask import Flask, render_template, session, request, redirect, send_from_directory
from core.config import TOKEN

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['TELEGRAM_BOT_TOKEN'] = TOKEN


@app.route('/')
def index():
    return '''
    <style>
    div {
    position: fixed;
    top: 50%;
    left: 50%;
    margin-top: -100px;
    margin-left: -100px;
    }
    </style>
    <body>
        <div>
            <script async 
                src="https://telegram.org/js/telegram-widget.js?16" 
                data-telegram-login="QRisto_Bot" 
                data-size="large" 
                data-auth-url="http://qristo.zerity.site/login/telegram" 
                data-request-access="write">
            </script>
        </div>
    </body>
    '''


def check_response(data):
    d = data.copy()
    del d['hash']
    d_list = []
    for key in sorted(d.keys()):
        if d[key] is not None:
            d_list.append(key + '=' + d[key])
    data_string = bytes('\n'.join(d_list), 'utf-8')

    secret_key = hashlib.sha256(app.config['TELEGRAM_BOT_TOKEN'].encode('utf-8')).digest()
    hmac_string = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
    if hmac_string == data['hash']:
        return True
    return False


@app.route('/login/telegram')
def login_telegram():
    data = {
        'id': request.args.get('id', None),
        'first_name': request.args.get('first_name', None),
        'last_name': request.args.get('last_name', None),
        'username': request.args.get('username', None),
        'photo_url': request.args.get('photo_url', None),
        'auth_date': request.args.get('auth_date', None),
        'hash': request.args.get('hash', None)
    }
    if check_response(data):
        session['user_id'] = request.args.get('id', None)
        return redirect('/gallery')
    else:
        return 'Authorization failed'


@app.route('/gallery')
def gallery():
    if 'user_id' in session:
        images = os.listdir('web/static/images/' + session['user_id'])
        return render_template('index.html', images=images, user_id=session['user_id'])
    else:
        return redirect('/')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'images/favicon.ico', mimetype='image/vnd.microsoft.icon')