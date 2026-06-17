"""Test distillation components."""

def test_teacher_connector_import():
    try:
        from ai_distiller.distillation.teacher import TeacherConnector
        assert True
    except ImportError:
        assert False
