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


    
class IDBH(idaapi.IDB_Hooks):

    def __init__(self,ctrl):
        super(IDBH,self).__init__()
        self.ctrl = ctrl

    def cmt_changed(self, ea, rep):
        cmt = idc.GetCommentEx(ea,rep)
        self.ctrl._handle_action({'action':'cmt_changed','ea':ea,'rep':rep,'cmt':cmt})
        return 0

    ### handle enum changes
    def enum_created(self,enum):
        ename = idc.GetEnumName(enum)
        eflag = idc.GetEnumFlag(enum)
        self.ctrl._handle_action({'action':'enum_created','enum':enum,'ename':ename,'eflag':eflag})
        return 0
    
    def	enum_deleted(self, enum):
        ename = idc.GetEnumName(enum)
        self.ctrl._handle_action({'action':'enum_deleted','enum':enum,'ename':ename})
        return 0
    def	enum_bf_changed(self, enum):
        return 0
    def	enum_renamed(self, enum):
        ename = idc.GetEnumName(enum)
        self.ctrl._handle_action({'action':'enum_renamed',
                                  'enum':enum,'ename':ename})

        return 0
    def	enum_cmt_changed(self, enum):
        ename = idc.GetEnumName(enum)
        cmt = idc.GetEnumCmt(enum,0)
        self.ctrl._handle_action({'action':'enum_cmt_changed',
                                  'enum':enum,'ename':ename,
                                  'cmt':cmt})
        return 0
    def	enum_member_created(self, enum, cid):
        ename = idc.GetEnumName(enum)
        cname = idc.GetConstName(cid)
        self.ctrl._handle_action({'action':'enum_member_created',
                                  'enum':enum,'cid':cid,
                                  'ename':ename,'cname':cname})
        return 0	
    def	enum_member_deleted(self, enum, cid):
        ename = idc.GetEnumName(enum)
        cname = idc.GetConstName(cid)
        self.ctrl._handle_action({'action':'enum_member_deleted',
                                  'enum':enum,'cid':cid,
                                  'ename':ename,'cname':cname})

        return 0

    ## handle structs
    def	struc_created(self, struct):
        sname = idc.GetStrucName(struct)
        union = idc.IsUnion(struct)
        self.ctrl._handle_action({'action':'struct_created',
                                  'struct':struct,'sname':sname,'union':union})
        return 0

    def	struc_deleted(self, struct):
        sname = idc.GetStrucName(struct)
        self.ctrl._handle_action({'action':'struct_deleted',
                                  'struct':struct,'sname':sname})
        return 0

    def	struc_renamed(self, struct):
        sname = idc.GetStrucName(struct)
        self.ctrl._handle_action({'action':'struct_renamed',
                                  'struct':struct,'sname':sname})
        return 0
    
    def	struc_expanded(self, struct):
        sname = idc.GetStrucName(struct)
        size = idc.GetStrucSize(struct)
        self.ctrl._handle_action({'action':'struct_expanded',
                                  'struct':struct,'sname':sname,'size':size})
        return 0
    def	struc_cmt_changed(self, struct):        
        sname = idc.GetStrucName(struct)
        cmt = idc.GetEnumCmt(struct,0)
        self.ctrl._handle_action({'action':'struct_cmt_changed',
                                  'struct':struct,'sname':sname,
                                  'cmt':cmt})
        return 0
        
    def	struc_member_created(self, struct, membr):
        sname = idc.GetStrucName(struct)
        mname = idc.GetMemberName(struct,membr)
        return 0
    
    def	struc_member_deleted(self, struct, membr, arg2):
        return 0
    def	struc_member_renamed(self, struct, membr):
        return 0
    def	struc_member_changed(self, struct, membr):
        return 0
        
HOOKS = [IDPH,IDBH]
