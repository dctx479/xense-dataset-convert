import pytest

# Importing the lerobot2mcap package loads tabular2mcap and lerobot at module
# level. The lightweight CI test job installs neither, so skip there instead
# of failing collection; the suite runs wherever the project is installed.
pytest.importorskip("tabular2mcap")
pytest.importorskip("lerobot")

from lerobot2mcap import converter  # noqa: E402


def test_resolves_automatic_worker_count_from_available_cpus(monkeypatch):
    monkeypatch.setattr(converter, "available_cpu_count", lambda: 20)

    assert converter.resolve_intra_workers(None) == 8
    assert converter.resolve_intra_workers(0) == 8


def test_preserves_explicit_worker_count_and_rejects_negative(monkeypatch):
    monkeypatch.setattr(converter, "available_cpu_count", lambda: 20)

    assert converter.resolve_intra_workers(3) == 3
    with pytest.raises(ValueError, match="intra_workers"):
        converter.resolve_intra_workers(-1)
