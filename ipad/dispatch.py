import idc
import idaapi
from ipad.compat import add_compat_functions

DEBUG = True
def debug(msg,*args):
    if DEBUG: print msg % args

idc = add_compat_functions(idc)
    
def dispath(args):

    
    ## dispatch args....
    class A(): pass
    a  =A()
    for name in args:
        setattr(a,name,args[name])
    del args


    ### dispath idp events 
    if a.action == 'rename':
        debug('[*] renaming %s to %s @ %x' ,a.old_name,a.new_name,a.ea)
        idc.MakeNameEx(a.ea,str(a.new_name),idaapi.SN_NOWARN)
        return 
    
    ## dispath idb events
    if a.action == 'cmt_changed':
        if not a.cmt: a.cmt = ''
        _pcmt = a.cmt if len(a.cmt)<10 else a.cmt[:10]+'...'
        debug('[*] cmt changed @ %X (rep:%s) - %s', a.ea,a.rep,_pcmt)
        if a.rep: idc.MakeRptCmt(a.ea,str(a.cmt))
        else: idc.MakeComm(a.ea,str(a.cmt))


    if a.action == 'struct_created':
        debug('[*] Struct %s created with id %x',a.sname,a.struct)
        print idc.AddStrucEx(-1,str(a.sname),a.union)

    if a.action == 'struct_deleted':
        sid = idc.GetStrucId(a.struct)
        sname = idc.GetStrucName(sid)
        debug('[*] Struct(%x) %s deleted',a.struct,sname)
        idc.DelStruc(sid)
        
    if a.action == 'struct_renamed':
        sid  = idc.GetStrucId(a.struct)
        sname  = idc.GetStrucName(sid)
        debug('[*] Struct(%d - %x) renamed from %s to %s',a.struct,sid,sname,a.sname)
        idc.SetStrucName(sid,str(a.sname))
              
    if a.action == 'struct_cmt_changed':
        sid  = idc.GetStrucId(a.struct)
        debug('[*] Struct(%d - %x) %s - cmt changed',a.struct,sid,a.sname)
        idc.SetStrucComment(sid,a.cmt,0)

    # if a.action == 'struct_expanded':
    #     debug('
        
    
    return 0

