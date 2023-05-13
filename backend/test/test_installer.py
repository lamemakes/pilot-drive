import pytest

from unittest.mock import MagicMock, patch

from pilot_drive.installer import Installer, FailedToExecuteCommandException

# Fixtures to create the installer with and without using default values
@pytest.fixture
def installer_not_default():
    return Installer(use_default=False)

@pytest.fixture
def installer_default():
    return Installer(use_default=True)

# Test that the use_default variable is properly set for both objects
def test_not_default(installer_not_default: Installer):
    assert installer_not_default.use_default is False

def test_default(installer_default: Installer):
    assert installer_default.use_default is True

@patch("pilot_drive.installer.subprocess.run")
def test_exec_cmd(mock_run, installer_default: Installer, installer_not_default: Installer):
    test_str = 'yeet!'
    mock_stdout = MagicMock()
    mock_stdout.configure_mock(
        **{
            "stdout": test_str,
            "stderr": ''
        }
    )

    mock_run.return_value = mock_stdout

    result = installer_default.exec_cmd('testing')
    assert result == test_str

    result_nd = installer_not_default.exec_cmd('testing')
    assert result_nd == test_str

@patch("pilot_drive.installer.subprocess.run")
def test_exec_cmd_exception(mock_run, installer_default: Installer, installer_not_default: Installer):
    test_str = 'yeet!'
    mock_stdout = MagicMock()
    mock_stdout.configure_mock(
        **{
            "stdout": '',
            "stderr": 'An error was raised!'
        }
    )

    mock_run.return_value = mock_stdout

    with pytest.raises(FailedToExecuteCommandException):
        installer_default.exec_cmd('testing')
    
    with pytest.raises(FailedToExecuteCommandException):
        installer_not_default.exec_cmd('testing')

def test_prompt_yes_no_yes(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    yes_val = "Y"
    monkeypatch.setattr('builtins.input', lambda _: yes_val)

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is True

    user_in = installer_not_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is True

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="n")
    assert user_in is False

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="n")
    assert user_in is False

def test_prompt_yes_no_no(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    no_val = "N"
    monkeypatch.setattr('builtins.input', lambda _: no_val)

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is False

    user_in = installer_not_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is False

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="n")
    assert user_in is True

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="n")
    assert user_in is True

def test_prompt_yes_no_default(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    default_val = ""
    monkeypatch.setattr('builtins.input', lambda _: default_val)

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is True

    user_in = installer_not_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is True

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="n")
    assert user_in is True

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="n")
    assert user_in is True

def test_prompt_yes_no_exception(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    no_val = "N"
    monkeypatch.setattr('builtins.input', lambda _: no_val)

    with pytest.raises(ValueError):
        installer_default.prompt_yes_no(prompt="yeet?", default_in="skeeb")

    with pytest.raises(ValueError):
        installer_not_default.prompt_yes_no(prompt="yeet?", default_in="skeeb")