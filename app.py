from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/')
def hello_world():
    return "Hello World"
@app.route('/hithere')
def second():
    retjson={
        'field1':'value1',
        'field2':'value2'
    }
    return jsonify(retjson)


@app.route('/add_num', methods=["POST"])
def add_num():
    dataDict = request.get_json()
    return jsonify(dataDict)



if __name__=="__main__":
    app.run(debug=True,host="127.0.0.1", port=80)




    
    