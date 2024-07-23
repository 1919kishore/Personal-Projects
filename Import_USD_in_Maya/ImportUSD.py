"""USD FILES IMPORTED ON TO MAYA."""

from maya import cmds

cmds.loadPlugin("mayaUsdPlugin.so")


class ImportUSD:
    """Main Class."""

    def __init__(self, usd_file, character_name=None, animal_name=None, frame_range=None):

        """Construct the method for the class.
        Args:
            usd_file (str): files full directory paths.
            frame_range(int): Offset frame range.
        """
        if character_name:
            self.import_usd_files(usd_file, character_name)
            namespace_list = cmds.namespaceInfo(listOnlyNamespaces=True)
            for scene_namespace in namespace_list:
                if scene_namespace == character_name:
                    # getting group names with namespace
                    object_names = cmds.ls("{}:*".format(character_name), r=True)
                    self.set_translation(object_names[0], 5, 5)
                    self.assign_material(object_names[0])
                    if frame_range:
                        self.offset_blendshape_anim(frame_range, character_name)

        if animal_name:
            self.import_usd_files(usd_file, animal_name)
            namespace_list = cmds.namespaceInfo(listOnlyNamespaces=True)
            for scene_namespace in namespace_list:
                if scene_namespace == animal_name:
                    # getting group names with namespace
                    object_names = cmds.ls("{}:*".format(animal_name), r=True)
                    self.set_translation(object_names[0], -5, 5)
                    self.assign_material(object_names[0])
                    if frame_range:
                        self.offset_blendshape_anim(frame_range, animal_name)

        if not animal_name and not character_name:
            print("Please pass at least one of argument Character or Animal")
            return

    def import_usd_files(self, usd_file_path, name_space):
        """Import usd files.
        Args:
            usd_file_path (str): file full directory path
            name_space (str): name_space of the object.
        """
        file_path = usd_file_path
        cmds.file(
            file_path, preserveReferences=True, type="USD Import", i=True,
            renameAll=True, mergeNamespacesOnClash=False, namespace=name_space,
            options="shadingMode=[[useRegistry,rendermanForMaya],[pxrRis,none],"
                    "[useRegistry,UsdPreviewSurface],[displayColor,none],"
                    "[none,none]];preferredMaterial=none;"
                    "importRelativeTextures=Automatic;primPath=/;readAnimData=1;"
                    "useCustomFrameRange=1;startTime=1;endTime=1000;"
                    "importUSDZTextures=0;importInstances=1",
            importFrameRate=True,
            importTimeRange="override"
        )

    def set_translation(self, name_space, translate_x, translate_y):

        """Set a group position.
        Args:
            name_space (str): name_space of the object.
            translate_x (int): Number of translation values.
            translate_y (int): Number of translation values.
        """
        if name_space:
            cmds.setAttr(
                "{}.translateX".format(name_space), translate_x
            )
            cmds.setAttr(
                "{}.translateY".format(name_space), translate_y
            )
        if not name_space:
            cmds.warning("No name_space found in the scene.")
            return

    def assign_material(self, name_space):
        """Assign material to mesh's.
        Args:
            name_space (str) : name_space of the object.
        """
        shader = cmds.shadingNode("lambert", asShader=True, name="normal_mat")
        normal_mat = cmds.sets(
            renderable=True, noSurfaceShader=True, empty=True
        )
        cmds.connectAttr("{}.outColor".format(shader),
                         "{}.surfaceShader".format(normal_mat))
        cmds.sets(
            "{}".format(name_space),
            edit=True, forceElement=normal_mat
        )

    def offset_blendshape_anim(self, offset, name_space):

        """Offset blendshape aniimation.
        Args:
            offset (int): Number of frames to offset
            name_space (str): name_space of the selected object.
        """
        blendshapes = cmds.ls("{}:*".format(name_space), type="blendShape")
        if not blendshapes:
            cmds.warning("No blendshapes found in the scene.")
            return

        for shape in blendshapes:
            anim_curves = cmds.listConnections(shape, type="animCurve")
            if not anim_curves:
                cmds.warning(
                    "No anim curves found for blendshape - {}".format(shape)
                )
                continue

            for curve in anim_curves:
                cmds.selectKey(curve, keyframe=True)
                cmds.keyframe(
                    relative=True,
                    option="over",
                    animation="keys",
                    timeChange=offset
                )
                cmds.selectKey(clear=True)

