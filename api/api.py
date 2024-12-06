from flask import Flask
from flask import request,Response

app = Flask(__name__)

@app.get('/')
def method():
    return {"message":"Hi there"}

@app.post('/feed')
def method(username,category_id,mood):
    pass


if __name__=='__main__':
    app.run(host='localhost',debug=True,port=8080)