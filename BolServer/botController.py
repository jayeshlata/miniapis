from webserver import ReqHandler
from pymongo import MongoClient
from bson import json_util

client = MongoClient()
db = client.local


def processAndRespond(pathList, paramDict):
    currPathSelect, remainingPathList = ReqHandler.getCurrentSelectedPath(pathList)
    responseMap = {}

    responseMap["success"] = False
    if currPathSelect == "getReply":
        if "userMessage" in paramDict:
            print "got a message from user"
            # TODO handle multiple messages and replies
            userMessage = paramDict["userMessage"][0]
            responseMap["reply"] = getMessageReply(userMessage)
            responseMap["success"] = True
        else:
            responseMap["error"] = "No userMessage"
    else:
        responseMap["error"] = "Invalid path"
    return json_util.dumps(responseMap)

def getMessageReply(message):
    return  "bhak from server: " + message