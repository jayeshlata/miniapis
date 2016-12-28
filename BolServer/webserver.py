import logging
import traceback
import urlparse as urlparse
import SimpleHTTPServer
import SocketServer
import botController

PORT = 8035


class ReqHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def checkRequestValidity(self, paramDict):
        print paramDict
        return True;

    def do_GET(self):
        try:
            print "gets"
            ps = urlparse.urlparse(self.path)
            paramDict = urlparse.parse_qs(ps.query)
            self.handleRequest(paramDict=paramDict, ps=ps)
        except Exception as e:
            logging.error(traceback.print_exc())
            self.wfile.write(traceback.format_exc())

    def do_POST(self):
        try:
            print "posts"
            length = int(self.headers['Content-Length'])
            paramsDictObj = self.rfile.read(length).decode('utf-8')

            # gives a stringified version of the req data
            paramsDict = urlparse.parse_qs(paramsDictObj)

            ps = urlparse.urlparse(self.path)
            self.handleRequest(paramDict=paramsDict, ps=ps)
        except Exception as e:
            logging.error(traceback.print_exc())
            self.wfile.write(traceback.format_exc())

    def handleRequest(self, paramDict, ps):
        pathArr = ps.path.split("/")
        pathArr = filter((lambda x: x != ""), pathArr)
        currPathSelect, remainingPathList = ReqHandler.getCurrentSelectedPath(pathArr)
        retObj = None
        if not self.checkRequestValidity(paramDict):
            self.send_response(405, 'Bad Request: not allowed')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        if currPathSelect == "bot":
            retObj = botController.processAndRespond(remainingPathList, paramDict)

        if retObj != None:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Expose-Headers: Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept", "*")
            self.end_headers()
            self.wfile.write(retObj)
        else:
            self.send_response(400, 'Bad Request: record does not exist')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

    @staticmethod
    def getCurrentSelectedPath(pathArr):
        currPathSelect = pathArr[0] if len(pathArr) > 0 else ""
        remainingPathList = pathArr[1:] if len(pathArr) > 1 else []
        return currPathSelect, remainingPathList


if __name__ == '__main__':
    Handler = ReqHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()
