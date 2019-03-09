import config
import os


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
