var express = require('express');
var router = express.Router();

//DB 연결
var mongoDB=require("mongodb").MongoClient;
var url="mongodb://127.0.0.1:27017/";
var dbObj=null;
mongoDB.connect(url, function(err, DB){
	
	console.log("DB Connect.......");
	dbObj=DB.db('iot');
});

//MQTT 서버 연결 IP주소 내 IP로 변경
var mqtt=require("mqtt"); 
var client=mqtt.connect("mqtt://192.168.0.11");

/* GET home page. */

//LED 제어 post 방식
router.post('/led/:flag', function(req, res, next) {
   res.set('Content-Type', 'text/json');	
   if(req.params.flag=="on"){
	   // MQTT->led : 1
	   client.publish("led", '1');
	   res.send(JSON.stringify({led:'on'}));
   }else{
	   client.publish("led", '2');
	   res.send(JSON.stringify({led:'off'}));
   }
});

// Android APP에서 추가된 부분
// 안드로이드 앱에서 요청을 받아서 DB에서 데이터를 가져와서 전송
router.get('/:device/:sensor', function(req, res, next){	
	var sensorLogs=null;
	if(req.params.sensor=="dht11"){
		sensorLogs=dbObj.collection('dht11');
	}else{
		//sensorLogs=dbObj.collection('mq2');
	}
    sensorLogs.find({}).limit(10).sort({created_at:-1}).toArray(function(err, results){
        if(err) res.send(JSON.stringify(err));		            	 
        else res.send(JSON.stringify(results));
   });		
});
module.exports = router;