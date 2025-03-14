'''Tests application'''
# pylint: disable=unused-import
import pytest

from app import App

def test_app_get_environment_variable():
    '''
    Test the App.getEnvironmentVariable method for retrieving the environment setting.
    This test initializes an instance of the App class and retrieves the value of the 'ENVIRONMENT'
    variable using the getEnvironmentVariable method. It then asserts that the returned value is one of
    the valid environment settings: 'DEVELOPMENT', 'TESTING', or 'PRODUCTION'. An AssertionError is raised
    if the environment variable does not match any of the expected values.
    '''
    app = App()
#   Retrieve the current environment setting
    current_env = app.getEnvironmentVariable('ENVIRONMENT')
    # Assert that the current environment is what you expect
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"



def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as _:
        app.start()
    # Optionally, check for specific exit code or message
    # assert excinfo.value.code == expected_exit_code
    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out
