from home.api_v1 import api,login_required
from flask import jsonify, request,g
from home.api_v1 import userservice


@api.route("/user/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    (code, data) = userservice.login(username, password)
    return jsonify({"status": code, "data": data})


@api.route("/user/register", methods=["POST"])
@login_required('1')
def register():
    data = request.json
    username = data["username"]
    password = data['password']
    tip = data['tip']
    (code, data) = userservice.register(username, password, tip)
    return jsonify({'status': code, 'data': data})


@api.route("/user/users", methods=["POST"])
@login_required('1')
def users():
    data = request.json
    username = data['query']
    pagenum = data['pagenum']
    pagesize = data['pagesize']
    (code, data) = userservice.users(username, pagenum, pagesize)
    return jsonify({"status": code, "data": data})


@api.route("/user/status", methods=["POST"])
@login_required('1')
def setuserstatus():
    data = request.json
    username = data['username']
    status = data['status']
    (code, data) = userservice.setuserstatus(username, status)
    return jsonify({'status': code, 'data': data})


@api.route("/user/previlege", methods=["POST"])
@login_required('1')
def setprevilege():
    data = request.json
    username = data['username']
    rights = data['rights']
    (code, data) = userservice.setprevilege(username, rights)
    return jsonify({'status': code, 'data': data})


@api.route("/user/previlege", methods=["GET"])
@login_required()
def getmyprevilege():
    (code, data) = userservice.getprevilege(g.username)
    return jsonify({'status': code, 'data': data})

@api.route("/user/previlege/<username>", methods=["GET"])
@login_required("1")
def getprevilege(username):
    (code, data) = userservice.getprevilege(username)
    return jsonify({'status': code, 'data': data})


@api.route("/user/password", methods=["POST"])
@login_required('1')
def updatepassword():
    data = request.json
    username = data['username']
    newpass = data['newpass']
    (code, data) = userservice.updatepassword(username, newpass)
    return jsonify({'status': code, 'data': data})
