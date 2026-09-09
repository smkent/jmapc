import jmapc


def test_import() -> None:
    assert jmapc.Client
    assert jmapc.methods  # ty: ignore[redundant-condition]
    assert jmapc.models  # ty: ignore[redundant-condition]
    assert jmapc.errors  # ty: ignore[redundant-condition]
