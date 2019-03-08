import json
import os


def get_bashrc_filename():
    return os.path.expanduser(os.path.join('~', '.bashrc'))


def revise_bashrc(bash_filename=get_bashrc_filename()):

    with open(bash_filename, 'r') as bashrc:
        txt = bashrc.read()

    if "Anaconda3/etc/profile.d/conda.sh" not in txt:
        txt += '\n. ~/Anaconda3/etc/profile.d/conda.sh\n'

        with open(bash_filename, 'w') as bashrc:
            bashrc.write(txt)


def get_settings_json_filename():
    return os.path.expandvars(os.path.join('$APPDATA', 'Code', 'User', 'settings.json'))


def revise_settings_json(json_filename=get_settings_json_filename()):
    with open(json_filename, 'r') as json_file:
        settings = json.load(json_file)

    print(settings)
