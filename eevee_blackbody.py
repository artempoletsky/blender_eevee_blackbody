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

# class UnifyModifiersSizeOperator(bpy.types.Operator):
#     """Unify modifiers"""
#     bl_idname = "object.unify_modifiers_operator"
#     bl_label = "Unify modifiers"
#     bl_options = {'REGISTER', 'UNDO'}
#
#     use_names: bpy.props.BoolProperty(name="Use names", default=False)
#     copy_all: bpy.props.BoolProperty(name="Copy all attributes", default=False)
#
#     @classmethod
#     def poll(cls, context):
#         return (context.space_data.type == 'VIEW_3D'
#             and len(context.selected_objects) > 0
#             and context.view_layer.objects.active
#             and context.object.mode == 'OBJECT')
#
#     def execute(self, context):
#
#         return {'FINISHED'}

def eevee_light_settings(self, context):
    layout = self.layout
    layout.separator()
    light = context.light

    layout.prop(light, "color")
    # layout.operator_context = "INVOKE_DEFAULT"
    # layout.operator(ScaleWithModifiersOperator.bl_idname, text=ScaleWithModifiersOperator.bl_label)

# classes = (
#     ScaleWithModifiersOperator,
#     UnifyModifiersSizeOperator,
# )

def register():
    # from bpy.utils import register_class
    # for cls in classes:
    #     register_class(cls)


    bpy.types.DATA_PT_EEVEE_light.append(eevee_light_settings)

def unregister():
    # from bpy.utils import unregister_class
    # for cls in reversed(classes):
    #     unregister_class(cls)

    bpy.types.DATA_PT_EEVEE_light.remove(eevee_light_settings)



if __name__ == "__main__":
    register()
