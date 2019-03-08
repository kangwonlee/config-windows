import config


def test_does_this_file_exist():
    # Following should not raise an exception
    config.does_file_exist(__file__)
