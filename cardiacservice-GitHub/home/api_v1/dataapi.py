from home.api_v1 import api,login_required
from flask import request,jsonify,send_from_directory,send_file,make_response,g
from flask import current_app as ca
import os,datetime,shutil,zipfile
from io import BytesIO
from home.models import Cardiacdata,db
from home.api_v1 import dataservice

@api.route("/data/uploaddicom",methods=["POST"])
@login_required('2')
def uploadDicomZip():
    file = request.files['zipfile']
    (code,data) = dataservice.uploadDicomZip(file,g.username)
    return jsonify({"status":code,"data":data})

@api.route("/data/publishlist",methods=["POST"])
@login_required('2')
def publishlist():
    data = request.json
    dataname = data['queryinfo']['query']
    pagenum = data['queryinfo']['pagenum']
    pagesize = data['queryinfo']['pagesize']
    (code,data) = dataservice.publishlist(dataname,pagenum,pagesize,g.username)
    return jsonify({'status':code,'data':data})

@api.route("/data/todolist",methods=["POST"])
@login_required('3')
def todolist():
    data = request.json
    dataname = data['query']
    pagenum = data['pagenum']
    pagesize = data['pagesize']
    (code,data) = dataservice.todolist(dataname,pagenum,pagesize)
    return jsonify({'status':code,'data':data})

@api.route("/data/gettask",methods=["POST"])
@login_required('3')
def gettask():
    data = request.json
    dataid = data['dataid']
    (code,data) = dataservice.gettask(g.username,dataid)
    return jsonify({"status":code,"data":data})

@api.route("/data/mytodolist",methods=["POST"])
@login_required('3')
def mytodolist():
    data = request.json
    dataname = data['queryinfo']['query']
    pagenum = data['queryinfo']['pagenum']
    pagesize = data['queryinfo']['pagesize']
    (code,data) = dataservice.mytodolist(g.username,dataname,pagenum,pagesize)
    return jsonify({"status":code,"data":data})

@api.route("/data/uploadstl",methods=["POST"])
@login_required('3')
def uploadSTL():
    file = request.files['zipfile']
    dataid = request.form['dataid']
    (code,data) = dataservice.uploadSTL(dataid,file)
    return jsonify({"status":code,"data":data})

@api.route("/data/images/<dataid>",methods=["GET"])
@login_required('2')
def getimages(dataid):
    (code,data) = dataservice.getimages(g.username,dataid)
    return jsonify({"status":code,"data":data})

@api.route("/data/crop/<dataid>",methods=["POST"])
@login_required('2')
def crop(dataid):
    coordinate = request.json
    (code,data) = dataservice.crop(dataid,coordinate)
    return jsonify({"status":code,"data":data})


@api.route("/data/ai/<dataid>",methods=["GET"])
@login_required('2')
def aisegment(dataid):
    (code,data) = dataservice.aisegment(g.username,dataid)
    return jsonify({"status":code,"data":data})

@api.route("/data/datalist",methods=["POST"])
@login_required('4')
def alldatalist():
    data = request.json
    dataname = data['query']
    pagenum = data['pagenum']
    pagesize = data['pagesize']
    (code,data) = dataservice.alldatalist(dataname,pagenum,pagesize)
    return jsonify({"status":code,"data":data})



@api.route("/data/dicomzip/<dataid>",methods=["GET"])
def downloadDicom(dataid):
    rv = dataservice.downloadDicomZip(dataid)
    return rv


@api.route("/data/downloadSTL/<dataid>/<stl>",methods=["GET"])
def downloadSTL(dataid,stl):
    rv = dataservice.downloadSTL(ca.config['UPLOADSTL_DIR'],dataid,stl)
    return rv

@api.route('/data/aistl/<dataid>/<stl>',methods=['GET'])
def downloadAistl(dataid,stl):
    rv = dataservice.downloadSTL(ca.config['AISTL_DIR'],dataid,stl)
    return rv

















