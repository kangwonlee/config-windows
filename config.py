import json
import os
import re
import shutil
import subprocess
import sys


def get_bashrc_filename():

    return os.path.expanduser(os.path.join('~', '.bashrc'))


def does_file_exist(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'{filename} not found')


def get_unix_path(win_path):

    if ':' in win_path:
        drive, win_path_under_drive = win_path.split(':')
        unix_path_under_drive = win_path_under_drive.replace('\\', '/')
        unix_path = f"/{drive.lower()}{unix_path_under_drive}"
    else:
        unix_path = win_path.replace('\\', '/')

    return unix_path
        

def has_folder_python(folder):
    return ('python' in os.listdir(folder)) or ('python.exe' in os.listdir(folder))


def get_python_folder_from_sys():
    return os.path.split(sys.executable)[0]


def get_conda_sh_filename():
    python_path = get_python_folder_from_sys()
    conda_sh_filename = os.path.join(python_path, 'etc', 'profile.d', 'conda.sh')

    assert os.path.exists(conda_sh_filename), conda_sh_filename
    assert os.path.isfile(conda_sh_filename), conda_sh_filename

    return os.path.join(python_path, 'etc', 'profile.d', 'conda.sh')


def add_alias_line(bashrc_txt):

    alias_line = 'alias log="git log --oneline --graph --all --color --decorated"\n'

    return '\n'.join([bashrc_txt, alias_line])


def revise_bashrc(bash_filename=get_bashrc_filename(), conda_sh_filename=get_conda_sh_filename()):

    # does_file_exist(bash_filename)
    does_file_exist(conda_sh_filename)

    if os.path.exists(bash_filename):
        txt = read_file(bash_filename)
    else:
        txt = ''

    # add path
    # TODO : how to revise path?
    b_path, txt, _ = add_python_folder_to_path(txt)

    # activate conda
    b_conda, txt = activate_conda(txt)

    # write to file if revised
    print(f"b_path  = {b_path}\nb_conda = {b_conda}")
    if b_path or b_conda:
        print(f"writing to {bash_filename}")
        with open(bash_filename, 'w') as bashrc:
            bashrc.write(txt)


def which_python_win_path():
    result_win_path = shutil.which('python')
    if result_win_path is None:
        result_win_path = ''
    return result_win_path


def which_python_unix_path():
    return run_cmd_in_bash('which python').strip()


def can_bash_find_python(python_exe_path=which_python_win_path()):
    return os.path.exists(python_exe_path) and os.path.isfile(python_exe_path)


def get_re_export_path():
    return re.compile(r"^export\s+PATH=(.*)$", re.M)


def add_python_folder_to_path(bashrc_txt, bash_can_find_python=can_bash_find_python(), conda_folder=get_python_folder_from_sys()):

    assert_conda_folder_host(conda_folder)
    conda_unix_folder = get_unix_path(conda_folder)

    conda_lib_bin_folder_host = os.path.join(conda_folder, 'Library', 'bin')

    assert_conda_lib_bin_folder_host(conda_lib_bin_folder_host)
    conda_lib_bin_folder_unix = get_unix_path(conda_lib_bin_folder_host)

    export_path_re = get_re_export_path()

    bashrc_txt = condition_bashrc_txt(bashrc_txt, export_path_re,)

    match = get_last_match(export_path_re, bashrc_txt)

    export_path_line = match.group(0)
    exported_path = match.group(1)

    folders_in_path = split_path_into_folders(exported_path)

    new_folders = add_to_list_unique_at_0(folders_in_path, conda_unix_folder, conda_lib_bin_folder_unix)

    new_export_path_str = export_path_line.replace(exported_path, ':'.join(new_folders))

    new_bashrc_txt = bashrc_txt.replace(export_path_line, new_export_path_str) 
    
    return new_export_path_str != export_path_line, new_bashrc_txt, new_export_path_str


def condition_bashrc_txt(bashrc_txt, export_path_re=get_re_export_path()):

    if not export_path_re.search(bashrc_txt):
        # if no line with "export PATH="
        bashrc_txt += '\nexport PATH=$PATH\n'
    else:
        # typo 
        for match in export_path_re.finditer(bashrc_txt):
            path_value = match.group(1)
            folder_list = split_path_into_folders(path_value)
            for folder in folder_list:
                assert any((
                        os.path.exists(folder),
                        os.path.exists(os.path.expanduser(folder)),
                        os.path.exists(os.path.expandvars(folder)),
                    )), (folder, folder_list)

    return bashrc_txt


def assert_conda_lib_bin_folder_host(conda_lib_bin_folder_host):
    assert os.path.exists(conda_lib_bin_folder_host), conda_lib_bin_folder_host
    assert os.path.isdir(conda_lib_bin_folder_host), conda_lib_bin_folder_host


def assert_conda_folder_host(conda_folder):
    assert_conda_lib_bin_folder_host(conda_folder)
    assert ('python' in os.listdir(conda_folder)) or ('python.exe' in os.listdir(conda_folder)), os.listdir(conda_folder)


def get_last_match(export_path_re, bashrc_txt):

    match = False

    for match in export_path_re.finditer(bashrc_txt):
        pass

    return match


def split_path_into_folders(path_str):
    return path_str.split(':')


def add_to_list_unique_at_0(this_list, *args):
    index = 0

    for arg in args:
        if arg not in this_list:
            this_list.insert(index, arg)
            index += 1

    return this_list


def which_git():
    result = shutil.which('git')
    if result is None:
        result = ''
    return result


def which_git_unix_path():
    return run_cmd_in_bash('which git')


def get_bash_path():
    git_exe_path = which_git()
    git_path_list = git_exe_path.split(os.sep)

    while 'git' != git_path_list[-1].lower():
        git_path_list.pop()

    result = os.sep.join(git_path_list + ['bin', 'bash.exe'])

    assert os.path.exists(result), f'\nresult = {result}\nwhich_git() = {which_git()}'
    assert os.path.isfile(result), f'\nresult = {result}\nwhich_git() = {which_git()}'

    return result


def get_bash_env_path():
    return run_cmd_in_bash('echo $PATH')


def run_cmd_in_bash(cmd_str):
    return str(subprocess.check_output([get_bash_path(), '-c', cmd_str]), encoding='utf-8')


def is_anaconda_in_bash_env_path(bash_env_path=get_bash_env_path()):
    env_path_list = bash_env_path.split(':')
    return any(map(lambda x : '/Anaconda3' in x, env_path_list))


def activate_conda(txt):
    b_revised = False
    if "Anaconda3/etc/profile.d/conda.sh" not in txt:
        txt += '\n. ~/Anaconda3/etc/profile.d/conda.sh\n'
        b_revised = True
    return b_revised, txt


def read_file(filename):
    txt = ''
    if os.path.exists(filename):
        with open(filename, 'r') as fp:
            txt = fp.read()
    return txt


def get_settings_json_filename():
    return os.path.expandvars(os.path.join('$APPDATA', 'Code', 'User', 'settings.json'))


def revise_settings_json(json_filename=get_settings_json_filename(), b_save=False):

    json_for_bash = {
        'python.pythonPath': os.path.join(get_python_folder_from_sys(), 'python.exe'),
        'terminal.integrated.shell.windows': get_bash_path(),
    }

    if os.path.exists(get_settings_json_filename()):
        with open(json_filename, 'r') as json_file:
            settings = json.load(json_file)
    else:
        settings = {}

    backup = dict(settings)

    print(f'before : {settings}')

    settings.update(json_for_bash)

    print(f'after  : {settings}')

    assert os.path.exists(settings['terminal.integrated.shell.windows']), settings
    assert os.path.isfile(settings['terminal.integrated.shell.windows']), settings

    print(f"b_save  = {b_save}\n")
    if b_save and (settings != backup):
        print(f'writing to {json_filename}')
        with open(json_filename, 'w') as json_file:
            json.dump(settings, json_file)

    return settings


def main():
    revise_bashrc()
    revise_settings_json(b_save=True)
    does_file_exist(get_bashrc_filename())
    does_file_exist(get_conda_sh_filename())
    does_file_exist(get_settings_json_filename())


if "__main__" == __name__:
    main()
