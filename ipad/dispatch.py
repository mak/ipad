import idc
import idaapi

DEBUG = True
def debug(msg):
    if DEBUG: print msg


    
def dispath(args):

    
    ## dispatch args....
    class A(): pass
    a  =A()
    for name in args:
        setattr(a,name,args[name])
    del args


    ### dispath idp events 
    if a.action == 'rename':
        debug('[*] renaming %s to %s @ %x' % (a.old_name,a.new_name,a.ea))
        idc.MakeNameEx(a.ea,str(a.new_name),idaapi.SN_NOWARN)
        return 
    
    ## dispath idb events
    if a.action == 'cmt_changed':
        if not a.cmt: a.cmt = ''
        _pcmt = a.cmt if len(a.cmt)<10 else a.cmt[:10]+'...'
        debug('[*] cmt changed @ %X (rep:%s) - %s' % (a.ea,a.rep,_pcmt))
        if a.rep: idc.MakeRptCmt(a.ea,str(a.cmt))
        else: idc.MakeComm(a.ea,str(a.cmt))

    
    return 0

