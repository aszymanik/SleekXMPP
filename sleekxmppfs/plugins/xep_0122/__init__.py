
from sleekxmppfs.plugins.base import register_plugin
from sleekxmppfs.plugins.xep_0122.stanza import FormValidation
from sleekxmppfs.plugins.xep_0122.data_validation import XEP_0122


register_plugin(XEP_0122)


# Retain some backwards compatibility
xep_0122 = XEP_0122
