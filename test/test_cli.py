import sys
from socaity.cli import main
import socaity
from socaity.sdk import face2face


def _capture_cli_output(args):
    """Helper to capture CLI output, works with or without pytest fixtures."""
    import io
    import contextlib

    old_argv = sys.argv
    sys.argv = args

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv

    val, err = stdout_capture.getvalue(), stderr_capture.getvalue()
    print(f"stdout: {val}, stderr: {err}")

    return val, err


def test_socaity_cli_help():
    """
    Tests that the CLI runs and produces help output.
    This confirms the entry point is wired correctly and arguments are parsed.
    """
    captured_out, captured_err = _capture_cli_output(["socaity", "--help"])

    assert "usage:" in captured_out or "usage:" in captured_err
    assert "Install a specific AI service or 'all'" in captured_out or "Install a specific AI service or 'all'" in captured_err


def test_socaity_install_function_exposed():
    """
    Tests that the install function is exposed in the top-level package.
    """
    assert hasattr(socaity, "install"), "socaity package should expose 'install' function"
    assert callable(socaity.install), "socaity.install should be callable"


def test_install_of_services():
    """
    Services to install
    """
    services_to_install = ["black-forest-labs/flux-schnell", "deepseek-ai/deepseek-v3", "tencent/hunyuan-video", "prunaai/hunyuan3d-2"]
    for service in services_to_install:
        captured_out, captured_err = _capture_cli_output(["socaity", "-i", service])
        assert f"Installing service: {service}..." in captured_out or f"Installing service: {service}..." in captured_err


if __name__ == "__main__":
    test_socaity_cli_help()
    test_socaity_install_function_exposed()
    test_install_of_services()
    print("All tests passed")
