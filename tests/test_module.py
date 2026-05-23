import jmapc


def test_import() -> None:
    assert jmapc.Client
    assert jmapc.methods
    assert jmapc.models
    assert jmapc.errors
