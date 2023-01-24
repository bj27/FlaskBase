from flask import jsonify
from Adrielly import *
class ResponseController():

    def formatDocument(self, content = [], format = "JSON", error = ""):
        tmp = {}
        tmp["message"] = "NOT CONTENT"
        tmp["error"] = ""
        tmp["content"] = []
        tmp["len"] = 0
        if format == "JSON":
            tmp["error"] = error
            tmp["message"] = "HAS CONTENT" if len(content) else tmp.get("message")
            tmp["content"] = content
            tmp["len"] = len(content)
        tmp["today"] = today()
        tmp["time"] = now()
        content = jsonify(tmp)
        return content