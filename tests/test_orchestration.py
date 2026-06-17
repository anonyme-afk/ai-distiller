"""Test orchestration components."""

def test_crew_builder_import():
    try:
        from ai_distiller.orchestration.crew_builder import CrewBuilder
        assert True
    except ImportError:
        assert False
