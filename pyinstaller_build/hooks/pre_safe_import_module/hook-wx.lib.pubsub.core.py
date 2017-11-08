"""
wxpython 3.0.1.1, 4.0.0a1  pubsub
"""

import os
from PyInstaller.utils.hooks import get_module_file_attribute

from wx.lib.pubsub import policies

# add appropriate subdir for protocol-specific implementation
def pre_safe_import_module( psim_api ):
    '''
    print "{"
    print psim_api.module_name
    print get_module_file_attribute(psim_api.module_name)
    print "}"
    '''
    module_dir = os.path.dirname(get_module_file_attribute(psim_api.module_name))
    arg_dir = os.path.join(module_dir, policies.msgDataProtocol)
    psim_api.append_package_path(arg_dir)
