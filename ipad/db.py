import os
import sqlite3
import json


class DB(object):
    def __init__(self,db):
        self.db = db
        self._init_db()
        self.conn = None
    def _init_db(self):
        if os.path.exists(self.db):
            return
        try:
            with self.get_db() as c:
                c.execute('CREATE TABLE changes (id integer primary key,timestamp int,action text,data text)')
        finally:
            self.__close()
            
    def __close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def get_db(self):
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def record(self,msg):
        
        ac = msg['action']
        del msg['action']
        t = msg['timestamp']
        del msg['timestamp']

        try:
            with self.get_db() as c:
                c.execute('insert into changes(timestamp,action,data) values(?,?,?)',(t,ac,json.dumps(msg)))
        finally:
            self.__close()

    def clear_history(self):
        self.delete_commits(0)
            
    def delete_commits(self,t):
        try:
            with self.get_db() as c:
                c.execute('delete from changes where timestamp > ?',(t,))
        finally:
            self.__close()
                
    def _get_commits(self,op,t):
        r= []
        try:
            with self.get_db() as c:
                cr= c.cursor()
                cr.execute('select timestamp,action,data from changes where timestamp %s ? order by timestamp desc'%op,(t,))
                for t,a,d in cr.fetchall():
                    m = json.loads(d)
                    m.update({'action':a,'timestamp':t})
                    r.append(m)
        finally:
            self.__close()
        return r
        

    def get_commit_via_id(self,_id):
        r = None
        try:
            with self.get_db() as c:
                cr= c.cursor()
                cr.execute('select timestamp,action,data from changes where id = ?',(_id,))
                r = cr.fetchone()
        finally:
            self.__close()
        return r

    
    def get_all_commits(self):
        return self._get_commits('>',0)
