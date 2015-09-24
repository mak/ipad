
import idaapi,idc
import threading

def add_compat_functions(idc):

    if not hasattr(idc,'ExpandStruc'):
        def f_ExpandStruc(sid,off,delta,recalc):
            s = idaapi.get_struc(sid)
            return idaapi.expand_struc(s,off,delta,recalc)
        setattr(idc,'ExpandStruc',f_ExpandStruc)


    return idc
        

def wait(n):
    threading.Event().wait(n)

## this is strage, use pressed keys to open file in ida...
try:
    from pykeyboard import PyKeyboard
    HAVE_KEYBOARD =True
except ImportError:
    HAVE_KEYBOARD = False

class Opener(object):

    def __init__(self):
        if HAVE_KEYBOARD:
            self.k = PyKeyboard()
    def type_file(self,f):
        if HAVE_KEYBOARD:
            wait(0.5) 
            self.k.type_string(f)
            wait(0.3)
            self.k.tap_key('Escape')
            self.k.tap_key(36)

            
    def open_file(self,f):
        if HAVE_KEYBOARD:
            threading.Thread(target=self.type_file,args=(f,)).start()
            self.k.press_key(self.k.alt_key)
            self.k.press_key('f')
            self.k.release_key(self.k.alt_key)  
            self.k.release_key('f') 
            self.k.tap_key(116)
            wait(0.2)
            self.k.tap_key(36)
        else:
            idc.Warning('Please open file: %s' % f)
            idc.ProcessUiAction('LoadFile')
        
