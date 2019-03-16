import config
import os
import shutil
import subprocess
import sys


def test_does_this_file_exist():
    config.does_file_exist(__file__)


def test_get_conda_sh_filename():

    result = config.get_conda_sh_filename()
    assert isinstance(result, str)

    result_list = result.split(os.sep)
    assert 'conda.sh' == result_list[-1]
    assert 'Anaconda3' in result_list
    assert 'etc' in result_list
    assert 'profile.d' in result_list


def test_get_settings_json_filename():
    result = config.get_settings_json_filename()
    assert isinstance(result, str)

    result_list = result.split(os.sep)
    assert 'settings.json' == result_list[-1]
    assert 'Code' in result_list


def test_activate_conda_add():
    txt = (
        'alias log="git log --oneline --graph --color --decorate"\n'
    )

    result = config.activate_conda(txt)

    assert result[0]
    assert 'Anaconda3/etc/profile.d/conda.sh' in result[1]


def test_activate_conda_intact():
    txt = (
        '. /c/Users/travis/Anaconda3/etc/profile.d/conda.sh\n'
        'alias log="git log --oneline --graph --color --decorate"\n'
    )

    result = config.activate_conda(txt)

    assert not result[0]
    assert txt == result[1]


def test_which_git():
    assert config.which_git()


def test_bash_path():
    bash_path = config.get_bash_path()
    assert bash_path

    assert os.path.exists(bash_path), f"{bash_path} not found"


def test_get_bash_env_path():
    result = config.get_bash_env_path()

    assert isinstance(result, (str, bytes)), type(result)


def test_is_anaconda_in_bash_env_path():
    path_with_anaconda = (
        '/c/Users/travis/Anaconda3:'
        '/c/Users/travis/Anaconda3/Scripts:'
        '/c/Users/travis/Anaconda3/bin:'
        '/mingw64/bin:'
        '/usr/bin:'
        '/c/WINDOWS/system32:'
        '/c/WINDOWS:'
        '/cmd:'
        '/c/Users/travis/AppData/Local/Programs/Microsoft VS Code/bin'
    )

    result = config.is_anaconda_in_bash_env_path(path_with_anaconda)

    assert result, path_with_anaconda


def test_is_anaconda_in_bash_env_path_not():
    path_with_anaconda = (
        '/mingw64/bin:'
        '/usr/bin:'
        '/c/WINDOWS/system32:'
        '/c/WINDOWS:'
        '/cmd:'
        '/c/Users/travis/AppData/Local/Programs/Microsoft VS Code/bin'
    )

    result = config.is_anaconda_in_bash_env_path(path_with_anaconda)

    assert not result, path_with_anaconda


def test_which_python():
    result = config.which_python_win_path()
    assert isinstance(result, str)


def test_can_bash_find_python_yes():
    import sys
    input_string = sys.executable
    result = config.can_bash_find_python(input_string)
    assert result, input_string


def test_can_bash_find_python_no():
    input_string = ''
    result = config.can_bash_find_python(input_string)
    assert not result, input_string


def test_get_python_folder_from_sys():
    python_path = config.get_python_folder_from_sys()
    assert config.has_folder_python(python_path)


def test_add_python_folder_to_path():
    input_text = ''
    python_folder = os.path.split(sys.executable)[0]
    result = config.add_python_folder_to_path(input_text, bash_can_find_python=False, conda_folder=python_folder)
    assert config.get_unix_path(python_folder) in result[1], result


def test_add_python_folder_to_path_example():
    input_text = '''export LANG=en_US.utf8
export PATH=~/Anaconda3:$PATH
. ~/Anaconda3/etc/profile.d/conda.sh
alias log="git log --oneline --graph --all --decorate"
'''
    python_folder = os.path.split(sys.executable)[0]
    result = config.add_python_folder_to_path(input_text, bash_can_find_python=False, conda_folder=python_folder)
    assert config.get_unix_path(python_folder) in result[1], result


def test_add_python_folder_to_path_default():
    bashrc_text = config.read_file(os.path.expanduser('~/.bashrc'))
    b_update, result = config.add_python_folder_to_path(bashrc_text)

    result_lines = result.splitlines()

    b_anaconda_in_path = False

    for line in result_lines:
        if line.startswith("export"):
            words = line.strip().split()
            if "export"==words[0] and words[1].startswith('PATH='):
                # located PATH line
                bash_path = str(subprocess.check_output([config.get_bash_path(), '-c', f"{words[1]};echo $PATH"]), 'utf-8')
                unix_path_list = bash_path.split(':')

                for folder in unix_path_list:
                    if 'Anaconda3' in folder:
                        b_anaconda_in_path = True
                        break

    assert (b_anaconda_in_path) or ((not b_update) and config.can_bash_find_python()), ("\n"
        f"b_anaconda_in_path = {b_anaconda_in_path}\n"
        f"not b_update = {not b_update}\n"
        f"config.can_bash_find_python() = {config.can_bash_find_python()}\n"
        )


def test_has_folder_python():
    assert config.has_folder_python(os.path.split(sys.executable)[0])


def test_has_folder_python_no():

    pardir_of_python_folder = os.path.abspath(
            os.path.join(
                os.path.split(sys.executable)[0], os.pardir
            )
        )

    assert not config.has_folder_python(pardir_of_python_folder), (pardir_of_python_folder, config.has_folder_python(pardir_of_python_folder))


def test_revise_settings_json():
    config.revise_settings_json(b_save=False)


def test_get_unix_path_without_drive():
    input_win_path = 'Users\\user\\.bashrc'
    result = config.get_unix_path(input_win_path)
    expected = 'Users/user/.bashrc'

    assert expected == result, f"\nexpected : {expected}\nresult : {result}"


def test_which_python_unix_path():
    result = config.which_python_unix_path()

    assert result.startswith('/'), (sys.executable, result)
    assert result.strip().endswith('python'), (sys.executable, result)

    drive_letter = result[1].upper()
    result_list = result.split('/')
    result_win_path = drive_letter + ':\\' + os.sep.join(result_list[2:]) + '.exe'

    # `which python` result may be different from `sys.executable`

    assert os.path.exists(result_win_path), (sys.executable, result_win_path)
    assert os.path.isfile(result_win_path), (sys.executable, result_win_path)


def test_run_cmd_in_bash():
    result = config.run_cmd_in_bash('true && echo $?')
    expected = '0\n'

    assert result == expected, result


def test_get_unix_path_with_drive():
    input_win_path = 'C:\\Users\\user\\.bashrc'
    result = config.get_unix_path(input_win_path)
    expected = '/c/Users/user/.bashrc'

    assert expected == result, f"\nexpected : {expected}\nresult : {result}"


def test_add_alias_line():
    input_string = '# 1 2 3'

    result = config.add_alias_line(input_string)

    assert input_string in result, result
    assert 'alias' in result, result


def test_get_re_export_path():
    expected = 'Find/This/line:Expected'
    expected_1 = 'Find/This/line:Expected1'

    not_expected = 'DontFind/This/line:NotExpected1'

    r = config.get_re_export_path()

    input_text = (
        'abc\n'
        f'export PATH={expected}\n'
        'def\n'
        f'export PATH={expected_1}\n'
        'ghi\n'
        f'export NOTPATH={not_expected}\n'
        'jkl\n'
    )

    result = r.findall(input_text)

    assert expected in result, (r, result, input_text)
    assert expected_1 in result, (r, result, input_text)
    assert not_expected not in result, (r, result, input_text)


def test_get_re_export_path_sample():
    expected = '~/Anaconda3:$PATH'
    expected_1 = '~/Anaconda3:/~/Anaconda3/Library/bin:$PATH'

    r = config.get_re_export_path()

    input_text = f'''export LANG=en_US.utf8
export PATH={expected}
. ~/Anaconda3/etc/profile.d/conda.sh
alias log="git log --oneline --graph --all --decorate"

export PATH={expected_1}
'''

    result = r.findall(input_text)

    assert expected in result, (r, result, input_text)
    assert expected_1 in result, (r, result, input_text)


def test_add_to_list_unique_at_0():
    list_input = ['zzz']
    add0 = 'abc'
    add1 = 'def'

    result = config.add_to_list_unique_at_0(list_input, add0, add1)

    assert result[0] == add0, result
    assert result[1] == add1, result
