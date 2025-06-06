from flask import Flask,jsonify
import os
app = Flask(__name__)

@app.route('/',methods=["GET"])
def index():
    return "Hello World"
@app.route('/health',methods=["GET"])
def helth():
    return jsonify(status='up'),200
if __name__== "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)