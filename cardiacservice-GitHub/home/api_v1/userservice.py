from home.models import db
from home.models import User
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
import hashlib

def login(username,password):
    user = db.session.query(User).get(username)
    if user is None or hashlib.md5(password.encode('utf-8')).hexdigest() != user.password:
        return (101,'用户名或密码错误')
    if user.status == '0':
        return (101,'账号被禁用')
    previlege = user.previlege.split(",") if user.previlege is not None else []
    s = TimedJSONWebSignatureSerializer(current_app.config['USER_TOKEN_KEY'],expires_in= current_app.config['TOKEN_EXPIRE'])
    token = s.dumps({'id':user.username,'permission':previlege})
    result = (100, {'token': str(token,encoding='utf-8'), 'username': user.username})
    return result

def register(username,password,tip):
    user = db.session.query(User).get(username)
    if user is not None:
        return (101,'用户名已存在')
    userr = User(username=username,
                 password=hashlib.md5(password.encode('utf-8')).hexdigest(),
                 tip=tip,
                 status="1")
    db.session.add(userr)
    db.session.commit()
    return (100,'注册成功')

def users(username,pagenum,pagesize):
    query = db.session.query(User)
    if username is not None and username.strip() != "":
        query = query.filter(User.username == username)
    pn = query.paginate(pagenum, pagesize)
    total = pn.total
    items = pn.items
    result = [{'username': item.username,
               'tip': item.tip,
               'status': True if item.status == "1" else False,
               'rights': item.previlege.split(",") if item.previlege is not None else []
               } for item in items]
    return (100,{'total': total, 'list': result})

def setuserstatus(username,status):
    statuss = "1" if status else "0"
    db.session.query(User).filter(User.username == username).update({User.status: statuss})
    db.session.commit()
    return (100,'状态更新成功')

def setprevilege(username,rights):
    previlege = ",".join(rights) if len(rights)>0 else None
    db.session.query(User).filter(User.username == username).update({User.previlege: previlege})
    db.session.commit()
    return (100,'权限设置成功')

def getprevilege(username):
    user = db.session.query(User).get(username)
    previlege = user.previlege.split(",") if user.previlege is not None else []
    return (100, previlege)

def updatepassword(username,newpass):
    password = hashlib.md5(newpass.encode('utf-8')).hexdigest()
    db.session.query(User).filter(User.username == username).update({User.password: password})
    db.session.commit()
    return (100,'密码修改成功')
