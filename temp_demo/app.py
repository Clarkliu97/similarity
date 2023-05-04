from flask import Flask, render_template, request, jsonify
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
