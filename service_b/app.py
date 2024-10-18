from flask import Flask,request,jsonify,Response
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app=Flask(__name__)
app.devices={}


@app.route("/",methods=["POST"])
def execute():
    data = request.get_json()
    print(data)
    response={ 
                     
                      "device_id":data['device_id'],
                      'status': "Выполнено",
                      'result': app.devices[data['device_id']]()
    }
    return Response(response,status=200,mimetype='application/json')

@app.route("/subscribe",methods=["GET"])
def subscribe():
     url=os.getenv('BROKER_URL')+'/subscribe'
     response = requests.get(url,headers={"X-Source-Port": "5002"})
     response.encoding='utf-8'
     if response.status_code==200:
         return response.json()
     return jsonify({"status_code": 500,"info": "Error"})

def turn_lamp():
    return "Лампочка зажглась!"


if __name__=="__main__":
    app.devices['1'] = turn_lamp
    app.run(port=5002,debug=True)

