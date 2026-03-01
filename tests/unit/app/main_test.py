import pytest


def test_main_imports():
    """Test that main.py can be imported without errors."""
    # This test ensures the main module structure is intact
    try:
        import importlib.util

        spec = importlib.util.find_spec("src.main")
        assert spec is not None
    except ImportError:
        pytest.fail("Failed to import main module")


def test_main_module_structure():
    """Test that main module has expected structure."""
    import src.main

    # Check that the module exists and has basic attributes
    assert hasattr(src.main, "__file__")
    assert "main.py" in src.main.__file__
