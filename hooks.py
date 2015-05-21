import idc
import idaapi

class IDPH(idaapi.IDP_Hooks):

    def __init__(self,ctrl):
        super(IDPH,self).__init__()
        self.ctrl = ctrl
    
    def rename(self,ea,new_name):
        old_name = idc.Name(ea)
        self.ctrl._handle_action({'ea':ea,'old_name':old_name,'new_name':new_name,'action':'rename'})
        return 0



HOOKS = [IDPH]
