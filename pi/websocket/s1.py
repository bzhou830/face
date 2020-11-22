from flask import Flask,render_template,request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer
import json

app=Flask(__name__)

user_socket_list = []

user_socket_dict = {

}

@app.route("/ws/<username>")
def ws(username):
    user_socket = request.environ.get("wsgi.websocket") #type:WebSocket
    if user_socket:
        user_socket_dict[username] = user_socket
    print(len(user_socket_dict),user_socket_dict)
    while 1:
        msg = user_socket.receive() # 收件人 消息 发件人
        msg_dict = json.loads(msg)
        msg_dict["from_user"] = username
        to_user = msg_dict.get("to_user")
        # chat = msg_dict.get("msg")
        u_socket = user_socket_dict.get(to_user) # type:WebSocket
        u_socket.send(json.dumps(msg_dict))

        # for u_socket in user_socket_list:
        #     if u_socket == user_socket:
        #         continue
        #     try:
        #         u_socket.send(msg)
        #     except:
        #         continue

@app.route("/")
def index():
    return render_template("ws.html")

if __name__ == '__main__':
    # app.run("0.0.0.0",9527,debug=True)
    http_serv = WSGIServer(("0.0.0.0",9527),app,handler_class=WebSocketHandler)
    http_serv.serve_forever()


