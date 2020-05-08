import sys
import os
import bpy

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

import eevee_blackbody
import imp
imp.reload(eevee_blackbody)
eevee_blackbody.register()
