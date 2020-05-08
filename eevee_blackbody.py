bl_info = {
    "name": "Eevee blackbody",
    "author": "Artem Poletsky",
    "version": (1, 0, 0),
    "blender": (2, 82, 0),
    "location": "Eevee -> light settings",
    "description": "Adds support of blackbody to eevee",
    "warning": "",
    "wiki_url": "",
    "category": "Lighting",
}

import bpy

def driver_add(light):
    driver = light.driver_add('color')

    return

def driver_remove(light):
    light.driver_remove('color')
    return

def eevee_light_settings(self, context):
    layout = self.layout
    layout.separator()
    light = context.light

    layout.prop(light, "use_blackbody")
    if light.use_blackbody:
        layout.prop(light, "blackbody")

blackbody_table_r = [
    [2.52432244e+03, -1.06185848e-03, 3.11067539e+00],
    [3.37763626e+03, -4.34581697e-04, 1.64843306e+00],
    [4.10671449e+03, -8.61949938e-05, 6.41423749e-01],
    [4.66849800e+03, 2.85655028e-05, 1.29075375e-01],
    [4.60124770e+03, 2.89727618e-05, 1.48001316e-01],
    [3.78765709e+03, 9.36026367e-06, 3.98995841e-01],
];

blackbody_table_g = [
    [-7.50343014e+02, 3.15679613e-04, 4.73464526e-01],
    [-1.00402363e+03, 1.29189794e-04, 9.08181524e-01],
    [-1.22075471e+03, 2.56245413e-05, 1.20753416e+00],
    [-1.42546105e+03, -4.01730887e-05, 1.44002695e+00],
    [-1.18134453e+03, -2.18913373e-05, 1.30656109e+00],
    [-5.00279505e+02, -4.59745390e-06, 1.09090465e+00],
];

blackbody_table_b = [
    [0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0],
    [-2.02524603e-11, 1.79435860e-07, -2.60561875e-04, -1.41761141e-02],
    [-2.22463426e-13, -1.55078698e-08, 3.81675160e-04, -7.30646033e-01],
    [6.72595954e-13, -2.73059993e-08, 4.24068546e-04, -7.52204323e-01],
];

def blackbody_temp_to_color(t):
    if t >= 12000.0:
        return [0.826270103, 0.994478524, 1.56626022];
    if t < 965.0:
        return [4.70366907, 0.0, 0.0]

    i = 0
    if t >= 6365.0:
        i = 5
    elif t >= 3315.0:
        i = 4
    elif t >= 1902.0:
        i = 3
    elif t >= 1449.0:
        i = 2
    elif t >= 1167.0:
        i = 1
    else:
        i = 0

    r = blackbody_table_r[i]
    g = blackbody_table_g[i]
    b = blackbody_table_b[i]

    t_inv = 1 / t
    return [r[0] * t_inv + r[1] * t + r[2],
           g[0] * t_inv + g[1] * t + g[2],
           ((b[0] * t + b[1]) * t + b[2]) * t + b[3]]

def update_light(light):
    if not light.use_blackbody:
        return

    light.use_nodes = False
    blackbody = light.blackbody
    light.color = blackbody_temp_to_color(blackbody)

def on_update_scene(scene):
    lights = [o for o in scene.objects if o.type == 'LIGHT']
    for l in lights:
        update_light(l.data)

def register():

    bpy.types.Light.blackbody =  bpy.props.IntProperty(name="Blackbody temperature", default=1500)
    bpy.types.Light.use_blackbody =  bpy.props.BoolProperty(name="Use blackbody temperature", default=False)
    bpy.types.DATA_PT_EEVEE_light.append(eevee_light_settings)
    bpy.types.CYCLES_LIGHT_PT_light.append(eevee_light_settings)
    bpy.app.handlers.depsgraph_update_post.append(on_update_scene)
    bpy.app.handlers.frame_change_post.append(on_update_scene)

def unregister():

    bpy.types.DATA_PT_EEVEE_light.remove(eevee_light_settings)
    bpy.app.handlers.depsgraph_update_post.remove(on_update_scene)
    bpy.types.CYCLES_LIGHT_PT_light.remove(eevee_light_settings)
    bpy.app.handlers.frame_change_post.remove(on_update_scene)

if __name__ == "__main__":
    register()
