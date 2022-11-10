def test_import() -> None:
    import jmapc

    assert jmapc.Client  # type: ignore[truthy-function]
    assert jmapc.methods
    assert jmapc.models
    assert jmapc.errors
