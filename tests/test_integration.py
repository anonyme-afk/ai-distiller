"""Test integration components."""

def test_api_import():
    try:
        from ai_distiller.api.server import app
        assert True
    except ImportError:
        assert False
