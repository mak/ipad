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
