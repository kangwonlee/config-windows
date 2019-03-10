import json
import os
import shutil
import subprocess
import sys


def get_bashrc_filename():
    return os.path.expanduser(os.path.join('~', '.bashrc'))


def does_file_exist(filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(f'{filename} not found')


def get_python_folder_from_sys():
    return os.path.split(sys.executable)[0]


def get_conda_sh_filename():
    python_path = get_python_folder_from_sys()
    conda_sh_filename = os.path.join(python_path, 'etc', 'profile.d', 'conda.sh')

    assert os.path.exists(conda_sh_filename), conda_sh_filename
    assert os.path.isfile(conda_sh_filename), conda_sh_filename

    return os.path.join(python_path, 'etc', 'profile.d', 'conda.sh')


def revise_bashrc(bash_filename=get_bashrc_filename(), conda_sh_filename=get_conda_sh_filename()):

    does_file_exist(bash_filename)
    does_file_exist(conda_sh_filename)

    txt = read_file(bash_filename)

    # add path
    # TODO : how to revise path?
    b_path, txt = add_python_folder_to_path(txt)

    # activate conda
    b_conda, txt = activate_conda(txt)

    # write to file if revised
    if b_path or b_conda:
        with open(bash_filename, 'w') as bashrc:
            bashrc.write(txt)


def which_python():
    return shutil.which('python')


def can_bash_find_python(python_exe_path=which_python()):
    return os.path.exists(python_exe_path) and os.path.isfile(python_exe_path)


def add_python_folder_to_path(bashrc_txt, bash_can_find_python=can_bash_find_python(), python_folder=get_python_folder_from_sys()):
    b_path = False
    if not bash_can_find_python:

        assert os.path.exists(python_folder), python_folder
        assert os.path.isdir(python_folder), python_folder
        assert ('python' in os.listdir(python_folder)) or ('python.exe' in os.listdir(python_folder)), os.listdir(python_folder)

        b_path = True

        bashrc_txt += f'\nexport PATH={python_folder}:$PATH\n'
    
    return b_path, bashrc_txt


def which_git():
    return shutil.which('git')


def get_bash_path():
    git_exe_path = which_git()
    git_path_list = git_exe_path.split(os.sep)
    result = os.sep.join(git_path_list[:-3] + ['bin', 'bash.exe'])

    assert os.path.exists(result), result
    assert os.path.isfile(result), result

    return result


def get_bash_env_path():
    return subprocess.check_output([get_bash_path(), '-c', 'echo $PATH'])


def is_anaconda_in_bash_env_path(bash_env_path=get_bash_env_path()):
    env_path_list = bash_env_path.split(':')
    return any(map(lambda x : '/Anaconda3' in x, env_path_list))


def get_python_folder():
    python_exe_path = which_python()
    python_path_str = os.path.split(python_exe_path)[0]
    return python_path_str


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
