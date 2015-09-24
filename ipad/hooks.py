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

    def savebase(self):
        if idc.AskYN(True,'Clear current history?') > 0:
            self.ctrl.db.clear_history()
            self.ctrl.uhist._clear()
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
        ### we have to maintain our own struct db
        ## becuse ida sux... 
        sname = idc.GetStrucName(struct)
        union = idc.IsUnion(struct)
        idx = idc.GetStrucIdx(struct)
        self.ctrl._handle_action({'action':'struct_created',
                                  'struct':idx,'sname':sname,'union':union})
        self.ctrl.db.struct_add(struct,idx)
        return 0

    def	struc_deleted(self, sid):
        print sid
        idx = self.ctrl.db.struct_get_idx(sid)
        self.ctrl._handle_action({'action':'struct_deleted','struct':idx})
        self.ctrl.db.struct_del(sid)
        return 0

    def	struc_renamed(self, struct):
        sid = struct.id
        idx = idc.GetStrucIdx(sid)
        sname = idc.GetStrucName(sid)
        self.ctrl._handle_action({'action':'struct_renamed',
                                  'struct':idx,'sname':sname})
        return 0
    
    def	struc_expanded(self, struct):
        sid = struct.id
        sname = idc.GetStrucName(sid)
        size = idc.GetStrucSize(sid)
        idx = idc.GetStrucIdx(sid)
        self.ctrl._handle_action({'action':'struct_expanded',
                                  'struct':idx,'sname':sname,'size':size})
        return 0
    def	struc_cmt_changed(self, sid):
        idx = idc.GetStrucIdx(sid)
        sname = idc.GetStrucName(sid)
        cmt = idc.GetEnumCmt(sid,0)
        self.ctrl._handle_action({'action':'struct_cmt_changed',
                                  'struct':idx,'sname':sname,
                                  'cmt':cmt})
        return 0
        
    def	struc_member_created(self, struct, membr):
        sid= struct.id
        mid = membr.id
        moff =membr.soff 
        flag = membr.flag
        size = idc.GetMemberSize(sid,moff)
        sname = idc.GetStrucName(sid)
        mname = idc.GetMemberName(sid,moff)
        idx = idc.GetStrucIdx(sid)
        self.ctrl._handle_action({'action':'struct_member_created','struct':idx,'member':mid,
                                  'sname':sname,'mname':mname,
                                  'off':moff,'flag':flag,'size':size})
        return 0
    
    def	struc_member_deleted(self, struct, mid, moff):
        sid= struct.id
        idx = idc.GetStrucIdx(sid)
        sname = idc.GetStrucName(sid)
        self.ctrl._handle_action({'action':'struct_member_deleted','struct':idx,'sname':sname,'member':mid,'off':moff})
        return 0
    
    def	struc_member_renamed(self, struct, membr):
        sid= struct.id
        mid = membr.id
        moff =membr.soff
        idx = idc.GetStrucIdx(sid)
        sname = idc.GetStrucName(sid)
        mname = idc.GetMemberName(sid,moff)
        self.ctrl._handle_action({'action':'struct_member_renamed','struct':idx,'member':mid,
                                  'sname':sname,'mname':mname,'off':moff})
        return 0
    def	struc_member_changed(self, struct, membr):
        sid= struct.id
        mid = membr.id
        moff =membr.soff 
        sname = idc.GetStrucName(sid)
        mname = idc.GetMemberName(sid,moff)
        idx = idc.GetStrucIdx(sid)
        flag = membr.flag
        size = idc.GetMemberSize(sid,moff)
        self.ctrl._handle_action({'action':'struct_member_changed','struct':idx,'member':mid,
                                  'sname':sname,'mname':mname,
                                  'off':moff,'flag':flag,'size':size})

        return 0
        
HOOKS = [IDPH,IDBH]
