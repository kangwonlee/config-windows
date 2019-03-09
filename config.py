import json
import os
import shutil


def get_bashrc_filename():
    return os.path.expanduser(os.path.join('~', '.bashrc'))


def does_file_exist(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'{filename} not found')


def get_conda_sh_filename():
    return os.path.expanduser(os.path.join('~', 'Anaconda3', 'etc', 'profile.d', 'conda.sh'))


def revise_bashrc(bash_filename=get_bashrc_filename(), conda_sh_filename=get_conda_sh_filename()):

    does_file_exist(bash_filename)
    does_file_exist(conda_sh_filename)

    txt = read_file(bash_filename)

    # add path

    # activate conda
    b_conda, txt = activate_conda(txt)

    # write to file if revised
    if b_conda:
        with open(bash_filename, 'w') as bashrc:
            bashrc.write(txt)


def which_git():
    return shutil.which('git')


def activate_conda(txt):
    b_revised = False
    if "Anaconda3/etc/profile.d/conda.sh" not in txt:
        txt += '\n. ~/Anaconda3/etc/profile.d/conda.sh\n'
        b_revised = True
    return b_revised, txt


def read_file(filename):
    txt = ''
    with open(filename, 'r') as fp:
        txt = fp.read()
    return txt

    # TODO : how to revise path?


def get_settings_json_filename():
    return os.path.expandvars(os.path.join('$APPDATA', 'Code', 'User', 'settings.json'))


def revise_settings_json(json_filename=get_settings_json_filename()):
    with open(json_filename, 'r') as json_file:
        settings = json.load(json_file)

    print(settings)


def main():
    revise_settings_json()
    does_file_exist(get_bashrc_filename())
    does_file_exist(get_conda_sh_filename())
    does_file_exist(get_settings_json_filename())


if "__main__" == __name__:
    main()
