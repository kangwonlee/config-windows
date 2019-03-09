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
