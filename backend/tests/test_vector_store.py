from unittest.mock import patch, MagicMock

from app.services.vector_service import get_index_stats


@patch("app.services.vector_service.get_vector_store", return_value=None)
def test_index_stats_no_store(mock_store):
    stats = get_index_stats()
    assert stats["loaded"] is False
    assert stats["documents_count"] == 0


@patch("app.services.vector_service.get_vector_store")
def test_index_stats_with_store(mock_get):
    mock_store = MagicMock()
    mock_store.index.ntotal = 42
    mock_get.return_value = mock_store

    stats = get_index_stats()
    assert stats["loaded"] is True
    assert stats["documents_count"] == 42
