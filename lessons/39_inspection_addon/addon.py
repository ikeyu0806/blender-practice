"""選択Meshの情報を表示する、小さなローカル用アドオン。"""

import bpy

bl_info = {
    "name": "Lesson 39 Mesh Inspector",
    "author": "Blender Practice",
    "version": (1, 0, 0),
    "blender": (5, 2, 0),
    "location": "View3D > Sidebar > Lesson39",
    "description": "選択Meshの頂点・面数を調べる学習用パネル",
    "category": "Mesh",
}
WARNING_FACE_COUNT = 1000


class LESSON39_OT_inspect(bpy.types.Operator):
    bl_idname = "lesson39.inspect"
    bl_label = "Inspect Selected Mesh"
    bl_description = "元のMeshの要素数を記録する。Modifier評価後の数とは別"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "MESH"
            and context.active_object.mode == "OBJECT"
        )

    def execute(self, context):
        mesh_object = context.active_object
        source_mesh = mesh_object.data
        # この操作は形を変えず、ObjectのCustom Propertiesへ観察値を残す。
        mesh_object["lesson39_vertex_count"] = len(source_mesh.vertices)
        mesh_object["lesson39_face_count"] = len(source_mesh.polygons)
        self.report(
            {"INFO"},
            f"{source_mesh.name}: {len(source_mesh.vertices)} vertices / {len(source_mesh.polygons)} faces",
        )
        return {"FINISHED"}


class LESSON39_PT_tools(bpy.types.Panel):
    bl_label = "Mesh Inspection"
    bl_idname = "LESSON39_PT_tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lesson39"

    def draw(self, context):
        self.layout.operator("lesson39.inspect")
        mesh_object = context.active_object
        if mesh_object and mesh_object.type == "MESH":
            face_count = len(mesh_object.data.polygons)
            self.layout.label(text=f"Source faces: {face_count}")
            if face_count > WARNING_FACE_COUNT:
                self.layout.label(text="Many faces: review density", icon="ERROR")
        else:
            self.layout.label(text="Select a Mesh in Object Mode")


CLASSES = (LESSON39_OT_inspect, LESSON39_PT_tools)


def unregister():
    # Text Editorで再実行すると新しいPythonクラスができるので、
    # bpy.typesに登録済みの実体を調べて解除する。
    for addon_class in reversed(CLASSES):
        registered_class = getattr(bpy.types, addon_class.__name__, None)
        if registered_class is not None:
            bpy.utils.unregister_class(registered_class)


def register():
    unregister()
    for addon_class in CLASSES:
        bpy.utils.register_class(addon_class)


if __name__ == "__main__":
    register()
