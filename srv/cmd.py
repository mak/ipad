import os
import json
import hashlib
from functools import wraps

## bottle
import bottle
from bottle import HTTPError
from bottle import route, request, response,template,abort

## my stuff
import config
import db

## only logged users...
def with_user(f):
    @wraps(f)
    def wrapper(*a,**kw):
        if not get_user():
            abort(403,'Wrong user')
        return f(*a,**kw)
    return wrapper

def get_user():
    user = request.forms.get('user')
    key =  request.forms.get('key')
    user = db.get_user(user,key)
    return user
    

#application = bottle.default_app()

@route('/create_idb',method='POST')
@with_user
def save_idb():
    data =request.files.get('data')
    d = ''.join( data.file.read() )
    _sha = hashlib.sha256(d).hexdigest()
    h = request.forms.get('hash')
    tag=request.forms.get('tag','init')
    uid=request.forms.get('uid')
    ssid=request.forms.get('ssid',None)
    name=data.filename

    if h != _sha:
        abort(500,'data-hash mismath')

    t = d.startswith('IDA')
    tm = db.save_idb(t,h,uid,tag,name,get_user(),ssid)
    if not tm:
        abort(403,'This is not your idb go away')
        
    idb_path = os.path.realpath(os.path.join(config.STOREDIR,uid))
    ses_path = os.path.realpath(os.path.join(idb_path,tm))
    if not idb_path.startswith(config.STOREDIR):
        abort(500,'I dont like it...')
    try:
        os.mkdir(idb_path)
    except:
        pass
    
    os.mkdir(ses_path)
    with open(os.path.join(ses_path,h+'.idb'),'w') as f:
        f.write(d)

    response.content_type = 'application/json'
    return {'session':int(tm)}

@route('/list_my',method='POST')
@with_user
def get_my_sessions():
    user = get_user()
    ret= {}
    for idb in db.get_my_idbs(user):
        ret[idb.name]= [ ]    
        for ses in idb.sessions:
            ret[idb.name].append({'tm':ses.timestamp.strftime('%s'),'tag':ses.tag,'ssid':ses.ssid})
        
    response.content_type = 'application/json'
    return json.dumps(ret)     

@route('/list',method='POST')
@with_user
def list_available_idbs():
    ### idb is available for user if there
    ##x exists a group, which he is a member of, that have readable
    ## rights to it
    r = {}
    user = get_user()
    for s in user.get_readable():
        if not s.idb.name in r:
            r[s.idb.name] = []
        r[s.idb.name].append({'uid':s.idb.uid,'tm':s.timestamp.strftime('%s'),'tag':s.tag,'ssid':s.ssid})
        
    response.content_type = 'application/json'
    return json.dumps(r)     

@route('/get',method='POST')
@with_user
def get_idb():
    user = get_user()
    uid=request.forms.get('uid')
    ssid=request.forms.get('ssid',None)
    ss = user.get_session(ssid)
    if not ss:
        abort(404,'This is not a session you are lookig for')

    if ss.idb.uid != uid:
        abort(404,'This is not a idb you are lookig for')

    path = os.path.join(config.STOREDIR,ss.idb.uid,str(ss.ssid),ss.hash + '.idb')
    path = os.path.realpath(path)
    if not path.startswith(config.STOREDIR):
        abort(500,'I dont like it...')

    with open(path) as f: data= f.read()
    response.set_header('X-IDB-Name',ss.idb.name)
    return data

@route('/get_stype',method='POST')
@with_user
def get_stype():
    ssid =  request.forms.get('ssid')
    ss = db.get_session(ssid)
    r = {'r':ss.type}
    response.content_type = 'application/json'
    return json.dumps(r)     



def run_server():
    db.start_db()
    bottle.run(host=config.CMD_HOST, port=config.CMD_PORT)
