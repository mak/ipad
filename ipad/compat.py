

import idaapi

def add_compat_functions(idc):

    if not hasattr(idc,'ExpandStruc'):
        def f_ExpandStruc(sid,off,delta,recalc):
            s = idaapi.get_struc(sid)
            return idaapi.expand_struc(s,off,delta,recalc)
        setattr(idc,'ExpandStruc',f_ExpandStruc)


    return idc
        
