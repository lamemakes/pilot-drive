import pytest

from unittest.mock import MagicMock, patch

import pilot_drive.installer
from pilot_drive.installer import Installer

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
    mock_stdout = MagicMock()
    mock_stdout.configure_mock(
        **{
            "stdout": '',
            "stderr": 'An error was raised!'
        }
    )

    mock_run.return_value = mock_stdout

    with pytest.raises(pilot_drive.installer.FailedToExecuteCommandException):
        installer_default.exec_cmd('testing')

    with pytest.raises(pilot_drive.installer.FailedToExecuteCommandException):
        installer_not_default.exec_cmd('testing')


def test_prompt_yes_no_yes(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    yes_val = "Y"
    monkeypatch.setattr('builtins.input', lambda _: yes_val)

    user_in = installer_default.prompt_yes_no(prompt="yeet?", default_in="y")
    assert user_in is True

    user_in = installer_not_default.prompt_yes_no(
        prompt="yeet?", default_in="y")
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

    user_in = installer_not_default.prompt_yes_no(
        prompt="yeet?", default_in="y")
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

    user_in = installer_not_default.prompt_yes_no(
        prompt="yeet?", default_in="y")
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


def test_prompt_list_select(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    list_selection = "2"
    opts_list = ["Test Option #1", "Test Option #2", "Test Option #3"]
    monkeypatch.setattr('builtins.input', lambda _: list_selection)

    user_in_default = installer_default.prompt_list(
        prompt="yeet?", options=opts_list, default_in=0)

    assert user_in_default == int(list_selection)

    user_in = installer_not_default.prompt_list(
        prompt="yeet?", options=opts_list, default_in=0)

    assert user_in == int(list_selection)


def test_prompt_list_default(monkeypatch, installer_default: Installer, installer_not_default: Installer):
    default_selection = ""
    default_opt = 1
    opts_list = ["Test Option #1", "Test Option #2", "Test Option #3"]
    monkeypatch.setattr('builtins.input', lambda _: default_selection)

    user_in_default = installer_default.prompt_list(
        prompt="yeet?", options=opts_list, default_in=default_opt)

    assert user_in_default == int(default_opt)

    user_in = installer_not_default.prompt_list(
        prompt="yeet?", options=opts_list, default_in=default_opt)

    assert user_in == int(default_opt)


def test_distro_detect_yum(monkeypatch, installer_default: Installer):

    def yum_cmd_test(_, param: str):
        if param == "yum":
            return "yum works!"
        else:
            raise pilot_drive.installer.FailedToExecuteCommandException

    monkeypatch.setattr(
        "pilot_drive.installer.Installer.exec_cmd", yum_cmd_test)

    distro_detect = installer_default.detect_distro_manager()

    assert distro_detect == "yum"


def test_distro_detect_apt(monkeypatch, installer_default: Installer):

    def apt_cmd_test(_, param: str):
        if param == "apt":
            return "apt works!"
        else:
            raise pilot_drive.installer.FailedToExecuteCommandException

    monkeypatch.setattr(
        "pilot_drive.installer.Installer.exec_cmd", apt_cmd_test)

    distro_detect = installer_default.detect_distro_manager()

    assert distro_detect == "apt"


def test_distro_detect_fail(monkeypatch, installer_default: Installer):

    def fail_cmd_test(_, param: str):
        raise pilot_drive.installer.FailedToExecuteCommandException

    monkeypatch.setattr(
        "pilot_drive.installer.Installer.exec_cmd", fail_cmd_test)

    with pytest.raises(pilot_drive.installer.FailedToDetectDistroManagerException):
        installer_default.detect_distro_manager()


def test_detect_sys_arch_valid(monkeypatch, installer_default: Installer):

    for arch in pilot_drive.installer.CommonArchs:

        class ArchClass:
            machine = arch

        monkeypatch.setattr("platform.uname", lambda: ArchClass())
        assert installer_default.detect_current_arch() == arch


def test_detect_sys_arch_fail(monkeypatch, installer_default: Installer):
    class ArchClass:
        machine = "yeet"

    monkeypatch.setattr("platform.uname", lambda: ArchClass())

    with pytest.raises(pilot_drive.installer.FailedToDetectSysArchException):
        installer_default.detect_current_arch()
