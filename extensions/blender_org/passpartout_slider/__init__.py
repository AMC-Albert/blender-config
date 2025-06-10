import bpy
import time

class VIEW3D_OT_passepartout_slider(bpy.types.Operator):
    bl_idname = "view3d.passepartout_slider"
    bl_label = "Camera Passepartout Slider"
    bl_options = {'GRAB_CURSOR', 'BLOCKING'}

    def invoke(self, context, event):
        camera = context.scene.camera
        if camera:
            self.init_mouse_x = event.mouse_x
            self.init_mouse_y = event.mouse_y
            self.init_value = camera.data.passepartout_alpha
            self.start_time = time.time()

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active camera found")
            return {'CANCELLED'}

    def modal(self, context, event):
        camera = context.scene.camera
        if not camera:
            return {'CANCELLED'}

        if event.type == 'MOUSEMOVE':
            if not camera.data.show_passepartout:
                camera.data.show_passepartout = 1
                return {'RUNNING_MODAL'}
            delta_x = (event.mouse_x - self.init_mouse_x) / 1000.0
            self.passepartout_opacity = self.init_value + delta_x
            self.passepartout_opacity = max(min(self.passepartout_opacity, 1.0), 0.0)
            camera.data.passepartout_alpha = self.passepartout_opacity
            context.area.header_text_set(f"Passepartout Opacity: {self.passepartout_opacity * 100:.1f}%")
            return {'RUNNING_MODAL'}
        elif event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set(None)  # Clear the header text
            if event.type == 'RIGHTMOUSE' or event.type == 'ESC':
                camera.data.passepartout_alpha = self.init_value
            return {'CANCELLED' if event.type in {'RIGHTMOUSE', 'ESC'} else 'FINISHED'}
        elif event.type == 'P' and event.value == 'RELEASE':
            mouse_distance = ((event.mouse_x - self.init_mouse_x)**2 + (event.mouse_y - self.init_mouse_y)**2)**0.5
            if (time.time() - self.start_time) < 0.3 and mouse_distance < 10:
                camera.data.show_passepartout = not camera.data.show_passepartout
            context.area.header_text_set(None)  # Clear the header text
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.area.header_text_set(None)  # Clear the header text

def register():
    bpy.utils.register_class(VIEW3D_OT_passepartout_slider)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    km.keymap_items.new("view3d.passepartout_slider", 'P', 'PRESS')

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_passepartout_slider)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps['3D View']
    for kmi in km.keymap_items:
        if kmi.idname == "view3d.passepartout_slider":
            km.keymap_items.remove(kmi)
            break

if __name__ == "__main__":
    register()
