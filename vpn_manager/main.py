import os
import subprocess
from flask import Flask, Response

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return "Manager is running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
