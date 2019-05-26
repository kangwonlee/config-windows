import os
import re
import shutil
import subprocess
import tempfile
import time

import pytest


def test_git_flow_init_d():
    temp_root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    assert os.path.exists(temp_root), temp_root

    tempdir = os.path.join(temp_root, 'temp')

    os.mkdir(tempdir)

    assert os.path.exists(tempdir), tempdir

    test_file_path = os.path.join(tempdir, 'test.txt')
    
    commands = (
            ('git', 'init',),
            ('git', 'config', 'user.name', '"name"',),
            ('git', 'config', 'user.email', 'nobody@nowhere.net',),
            ('touch', test_file_path,),
            ('git', 'add', test_file_path,),
            ('git', 'commit', '-m', '"test.txt"',),
    )

    list(map(lambda cmd: subprocess.check_call(cmd, cwd=tempdir), commands))

    script_folder = os.path.dirname(__file__)
    script_path = os.path.join(script_folder, 'config_git_flow.bat')

    assert os.path.exists(script_path), script_path

    # script under test
    subprocess.check_call(script_path, cwd=tempdir)

    p_init = subprocess.run((
            'git', 'flow', 'init', '-d',
        ), capture_output=True, text=True, cwd=tempdir)

    found = re.findall(r"^\w+?\sbranches?\s\[(.*?)\]\s*", p_init.stdout)

    try:
        assert found, (found, p_init.stdout, p_init.stderr)
        subprocess.check_call(('rm', '-rf', tempdir), cwd=temp_root)
    except BaseException as e:
        print(e)
        subprocess.check_call(('rm', '-rf', tempdir), cwd=temp_root)
        raise e
