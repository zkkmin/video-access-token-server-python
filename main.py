import os
import time

from flask import Flask, jsonify, request, render_template
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
load_dotenv(find_dotenv())

def get_token(identity, room):
    # Get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    api_key = os.environ['TWILIO_API_KEY']
    api_secret = os.environ['TWILIO_API_SECRET']

    # Create an Access Token
    token = AccessToken(account_sid, api_key, api_secret)

    # Set the Identity of this token

    time_stamp = time.time()
    token.identity = identity + str(time_stamp)
    
    # Grant access to Video
    grant = VideoGrant()
    grant.room = room
    token.add_grant(grant)

    # Return token
    return token.to_jwt().decode('utf-8')


@app.route('/')
def index():
    user = {'user_name': 'Visitor'}
    return render_template('index.html', title='Home', user=user)

@app.route('/make_call')
def make_call():
    identity = request.values.get('identity') or 'identity'
    room = request.values.get('room')
    token_value = get_token(identity, room)
    print (token_value)
    token = {'token': token_value}
    return render_template('make_call.html', token=token)

@app.route('/accept_call')
def accept_call():
    return render_template('accept_call.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

