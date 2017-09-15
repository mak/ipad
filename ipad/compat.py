import idaapi,idc
import threading
from qtglue import QProcess
def add_compat_functions(idc):

    if not hasattr(idc,'ExpandStruc'):
        def f_ExpandStruc(sid,off,delta,recalc):
            s = idaapi.get_struc(sid)
            return idaapi.expand_struc(s,off,delta,recalc)
        setattr(idc,'ExpandStruc',f_ExpandStruc)


    return idc
        

def wait(n):
    threading.Event().wait(n)


def open_idb(path):
    cmd = idaapi.idadir('ida')
    if float(idaapi.get_kernel_version()) < 7:
        cmd += 'q'
    if path.endswith('.i64'):
        cmd += '64'
        
    p = QProcess()
    p.startDetached(cmd,[path])
    if not p.waitForStarted():
        print '[-] failed to run ida'
    idaapi.qexit(0)

def test_import(n,p=None):
    msg_t = "couldn't import %s - you should install %s"
    r = False
    try:
        __import__(n)
        r = True
    except ImportError:
        msg= msg_t % (n,p or n)
        print '[-]',msg
        idc.warning(msg)
    return r
def test_imports():
    return test_import('zmq','pyzmq and zmq') and \
           test_import('requests')
        

def is_64bit():
    try:
        return idaapi.get_inf_structure().is_64bit()
    except:
        return idaapi.BADADDR > 0xffffffff
