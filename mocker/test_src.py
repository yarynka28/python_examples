import configparser
from unittest.mock import patch

import pytest

from mocker.src import MyClass


def custom_get_item(key):
    if key == 'DynamicProgramingParamaters':
        return {'wealth_state_total': 'Just a test 3!'}
    else:
        raise KeyError(str(key))


class CustomConfigParser1(configparser.ConfigParser):
    def __getitem__(self, key):
        if key == 'DynamicProgramingParamaters':
            return {'wealth_state_total': 'Just a test 4!'}
        else:
            raise KeyError(str(key))


class CustomConfigParser2(configparser.ConfigParser):
    def read(self, filenames, *args, **kwargs):
        # Intercept the calls to configparser -> read and replace it to read from your test data
        if './path' == filenames:
            # Option 1: If you want to manually write the configuration here
            self.read_string("[DynamicProgramingParamaters]\nwealth_state_total = Just a test 5!")

            # Option 2: If you have a test configuration file
            # super().read("./test_path")
        else:
            super().read(filenames, *args, **kwargs)



@pytest.fixture
def amend_read(mocker):  # Requires https://pypi.org/project/pytest-mock/ but you can also change this to just use the builtin unittest.mock
    original_func = configparser.ConfigParser.read

    def updated_func(self, filenames, *args, **kwargs):
        # Intercept the calls to configparser -> read and replace it to read from your test data
        if './path' == filenames:
            # Option 1: If you want to manually write the configuration here
            self.read_string("[DynamicProgramingParamaters]\nwealth_state_total = Just a test 6!")

            # Option 2: If you have a test configuration file
            # original_func.read(self, "./test_path")

            return

        return original_func(self, filenames, *args, **kwargs)

    mocker.patch('configparser.ConfigParser.read', new=updated_func)


@patch('configparser.ConfigParser')
def test_mock1(config_parser):
    # If you just want to mock the configparser without doing anything to its processing results
    obj = MyClass()
    result = obj.my_method()
    print(result)


@patch('configparser.ConfigParser.__getitem__', return_value={'wealth_state_total': 'Just a test 2!'})
def test_mock2(config_parser):
    # Change the returned value of configparser['DynamicProgramingParamaters']['wealth_state_total']
    obj = MyClass()
    result = obj.my_method()
    print(result)


@patch('configparser.ConfigParser.__getitem__', side_effect=custom_get_item)
def test_mock3(config_parser):
    # Same as test_mock2 only that we instead used a function to write the return
    obj = MyClass()
    result = obj.my_method()
    print(result)


@patch('configparser.ConfigParser', side_effect=CustomConfigParser1)
def test_mock4(config_parser):
    # Same as test_mock3 only that we instead used a class to write the return
    obj = MyClass()
    result = obj.my_method()
    print(result)


@patch('configparser.ConfigParser', side_effect=CustomConfigParser2)
def test_mock5(config_parser):
    # If have a configuration file for your test data, use this.
    obj = MyClass()
    result = obj.my_method()
    print(result)


def test_mock6(amend_read):
    # Same as test_mock5 only that we instead used a function to write the return
    obj = MyClass()
    result = obj.my_method()
    print(result)