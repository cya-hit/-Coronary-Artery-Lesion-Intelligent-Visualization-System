from util.redis import Redis
from flask import current_app as ca
from flask import make_response
import os,datetime,shutil,zipfile,uuid
from io import BytesIO
from home.models import Cardiacdata,db
from util.box import generatePicture
from util.data import getBasicInfo
from util.dicom2nii import dcm2nii
from urllib.parse import quote



def uploadDicomZip(file,username):
    if not zipfile.is_zipfile(file):
        return (101, "不是zip格式")
    z = zipfile.ZipFile(file)
    if not all([i.endswith(".dcm") for i in z.namelist()]):
        return  (101, "数据格式不正确")


    extract_path = os.path.join(ca.config['DICOMZIP_DIR'],str(uuid.uuid1()))
    os.mkdir(extract_path)
    try:
        z.extractall(extract_path)
        # raise Exception("fff")
    except:
        return (101,'压缩包解压错误')
    z.close()

    try:
        info = getBasicInfo(extract_path)
    except:
        return (101,'数据属性缺失')

    #数据库添加记录
    t = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    cardiac=Cardiacdata(
                uploaduser=username,
                uploadtime=t,
                dimension=info['dimen'],
                spacing=info['spacing'],
                coordinate=info['coordinate'],
                dataname=info['name'],
                age=info['age'],
                aistatus="0")
    db.session.add(cardiac)
    db.session.commit()
    dataid = cardiac.dataid

    old_dir = os.path.join(extract_path)
    new_dir = os.path.join(ca.config['DICOM_DIR'],str(dataid))
    shutil.move(old_dir,new_dir)

    return (100,{"dataid":dataid})

def publishlist(dataname,pagenum,pagesize,username):
    query = db.session.query(Cardiacdata).filter(Cardiacdata.uploaduser == username)
    if dataname is not None and dataname.strip() != "":
        query = query.filter(Cardiacdata.dataname.like("%"+dataname+"%"))
    pn = query.order_by(Cardiacdata.uploadtime.desc()).paginate(pagenum, pagesize)
    total = pn.total
    items = pn.items
    result = [{'data_id':item.dataid,
            'data_name':item.dataname,
            'age':item.age,
            'upload_time':':'.join(item.uploadtime.split(':')[:2]),
            'ai_status':item.aistatus,
            'ai_finish_time':':'.join(item.aifinishtime.split(':')[:2]) if item.aifinishtime is not None else None,
            'process_user':item.processer,
            'finish_time':':'.join(item.finishtime.split(':')[:2]) if item.finishtime is not None else None,
            'box':item.box
            }for item in items]
    return (100,{'list':result,'total':total})

def todolist(dataname,pagenum,pagesize):
    query = db.session.query(Cardiacdata).filter(Cardiacdata.processer == None)
    if dataname is not None and dataname.strip() != "":
        query = query.filter(Cardiacdata.dataname.like("%" + dataname + "%"))
    pn = query.order_by(Cardiacdata.uploadtime.desc()).paginate(pagenum, pagesize)
    total = pn.total
    items = pn.items
    result = [{'data_id': item.dataid,
               'data_name': item.dataname,
               'age': item.age,
               'data_dimen':item.dimension,
               'data_space':item.spacing,
               'coordinate':item.coordinate,
               'upload_user':item.uploaduser,
               'upload_time': ':'.join(item.uploadtime.split(':')[:2]),
               } for item in items]
    return (100,{'list': result, 'total': total})


def gettask(username,dataid):
    cardiac = db.session.query(Cardiacdata).get(dataid)
    if cardiac.processer is not None:
        return (101,"任务领取失败")
    else:
        cardiac.processer = username
        db.session.commit()
        return (100,"任务领取成功")

def mytodolist(username,dataname,pagenum,pagesize):
    query = db.session.query(Cardiacdata).filter(Cardiacdata.processer == username)
    if dataname is not None and dataname.strip() != "":
        query = query.filter(Cardiacdata.dataname.like("%" + dataname + "%"))
    pn = query.order_by(Cardiacdata.uploadtime.desc()).paginate(pagenum, pagesize)
    total = pn.total
    items = pn.items
    result = [{'data_id':item.dataid,
               'data_name':item.dataname,
               'age':item.age,
               'data_dimen':item.dimension,
               'data_space':item.spacing,
               'coordinate':item.coordinate,
               'upload_user':item.uploaduser,
               'upload_time':':'.join(item.uploadtime.split(':')[:2]),
               'ai_status':item.aistatus,
               'ai_finish_time':':'.join(item.aifinishtime.split(':')[:2]) if item.aifinishtime is not None else None,
               'finish_time':':'.join(item.finishtime.split(':')[:2]) if item.finishtime is not None else None}
              for item in items]
    return (100,{"list":result,"total":total})

def uploadSTL(dataid,file):
    cardiac = db.session.query(Cardiacdata).get(dataid)
    if cardiac.finishtime is not None:
        return (101,"请勿重复提交")
    #校验格式是否正确
    if not zipfile.is_zipfile(file):
        return (101, "不是zip格式")
    z = zipfile.ZipFile(file)
    fileset = set(['AO.stl','EE.stl','LA.stl','LV.stl','PA.stl','RA.stl','RV.stl','SVC.stl'])
    if not set(z.namelist()) == fileset:
        return (101,"内部文件命名错误")
    #解压至目录并更新数据库
    dir = os.path.join(ca.config['UPLOADSTL_DIR'],dataid)
    os.mkdir(dir)
    for i in z.namelist():
        z.extract(i, dir)
    z.close()
    t = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    cardiac.finishtime = t
    db.session.commit()
    return (100,"上传成功")

def getimages(username,dataid):
    cardiac = db.session.query(Cardiacdata).get(dataid)
    if cardiac is None: return (101,'数据不存在')
    if cardiac.uploaduser != username: return (105,'权限错误')
    path = os.path.join(ca.config['IMG_DIR'], dataid)
    if not os.path.exists(path):
        os.mkdir(path)
        dicomdir = os.path.join(ca.config['DICOM_DIR'], dataid)
        generatePicture(dicomdir, path)
    dimen = [int(i) for i in cardiac.dimension.split(",")]
    view1 = [dimen[0],dimen[1]]
    view2 = [dimen[1],dimen[2]]
    view3 = [dimen[0],dimen[2]]
    IMG_DIR = ca.config['IMG_DIR']
    file1 = os.listdir(os.path.join(IMG_DIR,dataid,'View1'))
    file2 = os.listdir(os.path.join(IMG_DIR,dataid,'View2'))
    file3 = os.listdir(os.path.join(IMG_DIR,dataid,'View3'))
    file1.sort(key = lambda x: int(x[:-4]))
    file2.sort(key=lambda x: int(x[:-4]))
    file3.sort(key=lambda x: int(x[:-4]))
    IMG_PREFIX = ca.config['IMG_PREFIX']
    view1url = [IMG_PREFIX+ dataid + "/View1/" + i for i in file1]
    view2url = [IMG_PREFIX+ dataid + "/View2/" + i for i in file2]
    view3url = [IMG_PREFIX+ dataid + "/View3/" + i for i in file3]
    data = {'size1':view1,'size2':view2,'size3':view3,'view1':view1url,'view2':view2url,'view3':view3url}
    return (100,data)

def crop(dataid,coordinate):
    cardiac = db.session.query(Cardiacdata).get(dataid)
    box = str(coordinate["x"][0])+","+str(coordinate["x"][1])+";"+\
          str(coordinate["y"][0])+","+str(coordinate["y"][1])+";"+\
          str(coordinate["z"][0])+","+str(coordinate["z"][1]);
    cardiac.box = box
    db.session.commit()
    return (100,'裁剪完成')

def aisegment(username,dataid):
    cardiac = db.session.query(Cardiacdata).get(dataid)
    if cardiac is None: return (101,'数据不存在')
    if cardiac.uploaduser != username: return (105,'权限错误')
    if cardiac.aistatus == '1': return (101,'正在计算，请勿重复提交')
    if cardiac.box is None or cardiac.box == '': return (101,'数据尚未裁剪')
    if Redis.llen(ca.config['MSG_QUEUE'])>ca.config['QUEUE_MAX']: return (101,'系统繁忙，请稍后重试')
    nii_file = os.path.join(ca.config['NIIDATA_DIR'], str(dataid) + '.nii')
    if not os.path.exists(nii_file):
        dcm_dir = os.path.join(ca.config['DICOM_DIR'], dataid)
        dcm2nii(dcm_dir,nii_file)
    [x,y,z] = cardiac.box.split(';')
    data = {'dataid':dataid,'nii':nii_file,'box':{'x':x.split(','),'y':y.split(','),'z':z.split(',')}}
    v=Redis.lpush(ca.config['MSG_QUEUE'],data)
    cardiac.aistatus = '1'
    cardiac.aifinishtime = None
    db.session.commit()
    return (100,'提交成功')

def alldatalist(dataname,pagenum,pagesize):
    query = db.session.query(Cardiacdata)
    if dataname is not None and dataname.strip() != "":
        query = query.filter(Cardiacdata.dataname.like("%" + dataname + "%"))
    pn = query.order_by(Cardiacdata.uploadtime.desc()).paginate(pagenum, pagesize)
    total = pn.total
    items = pn.items
    result = [{'data_id': item.dataid,
               'data_name': item.dataname,
               'age': item.age,
               'upload_user':item.uploaduser,
               'upload_time': ':'.join(item.uploadtime.split(':')[:2]),
               'data_dimen':item.dimension,
               'box':item.box,
               'process_user': item.processer,
               'finish_time': ':'.join(item.finishtime.split(':')[:2]) if item.finishtime is not None else None,
               'ai_status':item.aistatus,
               'ai_finish_time': ':'.join(item.aifinishtime.split(':')[:2]) if item.aifinishtime is not None else None,
               } for item in items]
    return (100, {'list': result, 'total': total})

def downloadSTL(base_path,dataid,code):
    filedir = os.path.join(base_path, dataid)
    dic = {0: 'PA.stl', 1: 'LA.stl', 2: 'SVC.stl', 3: 'AO.stl', 4: 'RA.stl', 5: 'RV.stl', 6: 'LV.stl', 7: 'EE.stl'}
    filenames = []
    for i, c in enumerate(code):
        if c == '1':
            filenames.append(dic[i])
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for _file in filenames:
            ff = os.path.join(filedir, _file)
            if os.path.exists(ff):
                with open(ff, 'rb') as fp:
                    zf.writestr(_file, fp.read())
    rv = make_response(memory_file.getvalue())
    memory_file.close()
    rv.headers["Cache-Control"] = "no-cache"
    rv.headers['Content-Disposition'] = 'attachment; filename={}.zip'.format(dataid)
    return rv

def downloadDicomZip(dataid):
    cardiac = db.session.query(Cardiacdata).get(dataid)
    dicom_dir = os.path.join(ca.config['DICOM_DIR'],str(dataid))
    filenames = os.listdir(dicom_dir)
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for _file in filenames:
            ff = os.path.join(dicom_dir, _file)
            if os.path.exists(ff):
                with open(ff, 'rb') as fp:
                    zf.writestr(_file, fp.read())

    rv = make_response(memory_file.getvalue())
    memory_file.close()
    rv.headers["Cache-Control"] = "no-cache"
    rv.headers['Content-Disposition'] = "attachment; filename*=UTF-8''{}.zip".format(quote(cardiac.dataname.encode('utf-8')))
    return rv

