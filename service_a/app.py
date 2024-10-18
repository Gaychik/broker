from flask import Flask,request,jsonify
from dotenv import load_dotenv
import os
import requests
load_dotenv()

#

app=Flask(__name__)

@app.route("/send_cmd",methods=["POST"])
def send():
    data = request.get_json()
    print(data)
    url=os.getenv('BROKER_URL')+'/send'
    response = requests.post(url=url, 
                  json={ 
                      "command":data['cmd'],
                      "device_id":data['device_id'],
                      'status': "в обработке",
                      'target_host' : data['target_host'],
                      'target_port': data['target_port']
    })
    if response.status_code==200:
        return response.json()
    
    
@app.route("/subscribe",methods=["GET"])
def subscribe():
     url=os.getenv('BROKER_URL')+'subscribe'
     response = requests.get(url,headers={"X-Source-Port": "5003"})
     response.encoding='utf-8'
     if response.status_code==200:
         return response.json()
     return jsonify({"status_code": 500,"info": "Error"})
     
if __name__=="__main__":
    app.run(port=5003,debug=True)