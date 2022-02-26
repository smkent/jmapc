def test_import() -> None:
    import jmapc

    assert jmapc.Client
    assert jmapc.methods
    assert jmapc.models
    assert jmapc.errors
