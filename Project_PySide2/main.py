from maya import cmds, mel
import json
import os


def set_audio(audio_path):
    """Set audio in maya file.
    Args:
        audio_path (str): file full directory path
    """
    audio_file_path = audio_path
    audio_file_name = audio_file_path.split("/")
    audio_name = audio_file_name[-1].split(".")
    cmds.sound(file=audio_file_path, name=audio_name[0])
    gPlayBackSlider = mel.eval("$tmpVar=$gPlayBackSlider;")
    cmds.timeControl(gPlayBackSlider, edit=True, sound=audio_name[0], displaySound=True)


def load_files(file_path):
    """Load the maya MB file.
    Args:
        file_path (str): file full directory path
    """
    cmds.file(
        file_path,
        preserveReferences=True, type="mayaBinary", i=True
    )


def export_characters(file_path, file_name):
    """Export select file in obj format.
    Args:
        file_path (str): file full directory path
        file_name (str): export file name
    """
    obj_file_path = "{}/{}".format(file_path, file_name)
    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
        except Exception as save_path_error:
            print(save_path_error)
            return
    try:
        cmds.file(
            obj_file_path, type="OBJexport",
            options="groups=0;ptgroups=1;materials=0;smoothing=0;normals=1",
            force=True, preserveReferences=True,
            exportSelected=True
        )
    except Exception as error:
        return error


def save_json(path, data, file_name):
    """Save the export controls anim key in json format.
    Args:
        path (str): file full directory path
        data (dist): dist data from keyframes
        file_name (str): export file name
    """
    json_path = "{}/{}_anim_export.json".format(path, file_name)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as save_path_error:
            print(save_path_error)
            return
    with open(json_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def export_anim_json(control_names, path):
    """Export select controls animation key to dist.
    Args:
        control_names (str): select controls name
        path (str): file full directory path
    """
    attributes = [
        'rotateX', 'rotateY', 'rotateZ',
        'translateX', 'translateY', 'translateZ', 'scaleX',
        'scaleY', 'scaleZ'
    ]
    data = {}
    character_name = ""
    try:
        for attr_name in control_names:
            character_name = attr_name.split(":")
            for attr in attributes:
                frames = cmds.keyframe(attr_name, q=True, at=attr)
                values = cmds.keyframe(attr_name, q=True, at=attr, valueChange=True)
                data["{}.{}".format(attr_name, attr)] = dict(zip(frames, values))
        # Save to JSON
        save_json(path, data, character_name[0])
    except Exception as error:
        return error


def generate_function(file_path, audio_path):
    """Generate load and audio files function.
    Args:
        file_path (str): file full directory
        audio_path (str): file full directory
    """
    cmds.file(new=True, force=True)
    set_audio(audio_path)
    load_files(file_path)
