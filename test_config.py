import config
import os
import shutil


def test_does_this_file_exist():
    # Following should not raise an exception
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
    result = config.which_python()

    assert result


def test_get_python_path():
    result = config.get_python_folder()

    assert os.path.exists(result), f"{result} does not exist?"
    assert os.path.isdir(result), f"{result} is not a folder?"
    assert ('python' in os.listdir(result)) or ('python.exe' in os.listdir(result)), os.listdir(result)
    assert os.path.exists(os.path.join(str(result), 'python.exe'))


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
    assert ('python' in os.listdir(python_path)) or ('python.exe' in os.listdir(python_path)), os.listdir(python_path)
