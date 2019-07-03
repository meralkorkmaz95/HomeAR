# 
from bottle import *
from bottle import default_app, route, get, post, request, response
import sqlite3
import json
from json import dumps

DBPath = os.path.abspath(os.path.dirname(__file__)) + '/Database/HomeAR.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@route('/tempData')
def tempData():

    DBConn = sqlite3.connect(DBPath)
    DBConn.row_factory = dict_factory
    DBPtr = DBConn.cursor()

    SQL_Query = "SELECT * FROM Temperature ORDER BY ID DESC LIMIT 1"
    DBPtr.execute(SQL_Query)
    Temperature = DBPtr.fetchone()

    TempData = dict()
    TempData["ID"] = Temperature['ID']
    TempData["DateAndTime"] = Temperature["DateAndTime"]
    TempData["Temperature"] = Temperature["Temperature"]

    DBPtr.close()
    DBConn.close()
    return TempData


@post('/postTemp')
def postTemp():
    postData = request.body.read()
    postData = postData.decode('utf-8')
    postData = json_loads(postData)

    myStr = "[{avgTime:" + str(postData[0]['avgTime']) + ", avgTemp: " + str(postData[0]['avgTemp']) + "}," + "{avgTime:" + str(postData[1]['avgTime']) + ", avgTemp: " + str(postData[1]['avgTemp']) + "}," + "{avgTime:" + str(postData[2]['avgTime']) + ", avgTemp: " + str(postData[2]['avgTemp']) + "}," + "{avgTime:" + str(postData[3]['avgTime']) + ", avgTemp: " + str(postData[3]['avgTemp']) + "}," + "{avgTime:" + str(postData[4]['avgTime']) + ", avgTemp: " + str(postData[4]['avgTemp']) + "}]"
    print(myStr)

    DBConn = sqlite3.connect(DBPath)

    DBPtr = DBConn.cursor()

    SQL_Query = 'UPDATE avgTemp SET avgTempData="' + myStr + '" WHERE ID=1';
    DBPtr.execute(SQL_Query)

    DBPtr.close()
    DBConn.commit()
    DBConn.close()

    return 'OK'


@route('/postTemp', method='POST')
def postTemp():
    postData = request.body.read()
    postData = postData.decode('utf-8')
    postData = json.loads(postData)

    SQL_Query = "UPDATE Temperature SET Temperature="+postData["tempSensor"]+", DateAndTime="+postData["dateTime"]+" WHERE ID=1"

    DBConn = sqlite3.connect(DBPath)
    DBPtr = DBConn.cursor()
    DBPtr.execute(SQL_Query)
    DBPtr.close()
    DBConn.commit()
    DBConn.close()

    return "OK"


@get('/getAvgTemp')
def avgTemp():
    DBConn = sqlite3.connect(DBPath)
    DBConn.row_factory = dict_factory
    DBPtr = DBConn.cursor()

    SQL_Query = "SELECT avgTempData FROM avgTemp ORDER BY ID DESC LIMIT 1"
    DBPtr.execute(SQL_Query)
    avgTemp = DBPtr.fetchone()

    DBPtr.close()
    DBConn.close()

    avgTemp['avgTempData'] = avgTemp['avgTempData'].replace('avgTemp:', '"avgTemp":')
    avgTemp['avgTempData'] = avgTemp['avgTempData'].replace('avgTime:', '"avgTime":')

    send = json.dumps(avgTemp)
    send = send.replace('\\"', "\"")
    response.content_type = 'application/json'
    response.body = send
    return response


@post('/toggleLight')
def toggleLight():
    postData = request.body.read()
    postData = postData.decode('utf-8')
    postData = postData.replace('Status=', '')

    DBConn = sqlite3.connect(DBPath)
    DBConn.row_factory = dict_factory
    DBPtr = DBConn.cursor()
    
    SQL_Query = 'UPDATE Light SET Status="' + postData + '" WHERE ID=1';
    DBPtr.execute(SQL_Query)
    
    DBPtr.close()
    DBConn.commit()
    DBConn.close()

    return 1


@get('/getLightStatus')
def getLightStatus():
    DBConn = sqlite3.connect(DBPath)
    DBConn.row_factory = dict_factory
    DBPtr = DBConn.cursor()

    SQL_Query = "SELECT Status FROM Light ORDER BY ID DESC LIMIT 1"
    DBPtr.execute(SQL_Query)
    lightStatus = DBPtr.fetchone()
    DBPtr.close()
    DBConn.close()
    lightStatus = str(lightStatus)

    if lightStatus.find("OFF") >= 0:
        return '0'
    if lightStatus.find("ON") >= 0:
        return '1'