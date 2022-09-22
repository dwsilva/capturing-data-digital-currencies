import datetime
import pytest
from capturing_data_digital_currencies.ingestors import DataIngestor
from capturing_data_digital_currencies.writers import DataWriter
from unittest.mock import patch, mock_open


# from ingestors import DataIngestor

@pytest.fixture
@patch("ingestors.DataIngestor.__abstractmethod__", set())
def data_ingestor_fixture():
    return DataIngestor(
        writer=DataWriter,
        coins=['Test1', 'Test2'],
        default_start_date=datetime.datetime(2022, 6, 12)
    )


@patch("ingestors.DataIngestor.__abstractmethod__", set())
class TestIngestors:
    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename
        expected = 'DataIngestor.checkpoint'
        assert actual == expected

    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime.datetime(2022, 6, 12)
        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2022-06-15")
    def test_load_checkpoint_existing_checkpoint(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime.datetime(2022, 6, 15)
        assert actual == expected

    @patch("ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_updated(self, mock, data_ingestor_fixture):
        data_ingestor_fixture._update_checkpoint(value=datetime.datetime(2022, 6, 1))
        actual = data_ingestor_fixture._checkpoint
        expected = datetime.datetime(2022, 6, 1)
        assert actual == expected

    @patch("ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_written(self, mock, data_ingestor_fixture):
        data_ingestor_fixture._update_checkpoint(value=datetime.datetime(2022, 6, 1))
        mock.assert_called.once()

    @patch("builtins.open", new_callable=mock_open, read_data="2022-06-15")
    @patch("ingestors.DataIngestor._checkpoint_filename", return_value='foobar.checkpoint')
    def test_write_checkpoint(self, mock_checkpoint_filename, mock_open_file, data_ingestor_fixture):
        data_ingestor_fixture._write_checkpoint()
        mock_open_file.assert_called_with(mock_checkpoint_filename, 'w')
