import sys,os
import idc,idaapi

## for a case when old ida didn't expand path on its own
def realpath():
    my_path = os.path.abspath(os.path.expanduser(__file__))
    if os.path.islink(my_path):
        my_path = os.readlink(my_path)
    return os.path.dirname(my_path)
rp = realpath()
if rp not in sys.path:
    sys.path.append(rp)
plugin = os.path.join(rp,'ipad.py')


from ipad.compat import wait,test_imports
if not test_imports():
    idc.error('Failed to import needed libs')

idaapi.autoWait()
print idaapi.load_and_run_plugin(plugin,1)
