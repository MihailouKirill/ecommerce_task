import pytest
from unittest.mock import MagicMock, patch
from pipeline.utils.db_connection import DataBasePostgreSQLConnection


@pytest.fixture
def fake_settings():
#Данные заглушки для теста
    settings=MagicMock()
    settings.db_host='test'
    settings.db_port=1341
    settings.db_user='test'
    settings.db_password='test'
    settings.db_name='test'
    return settings
#Мокнули подключение
@patch("pipeline.utils.db_connection.psycopg2.connect")
#Тест успешного закрытия КМ
def test_success_connection(mock_connect,fake_settings):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    with DataBasePostgreSQLConnection(fake_settings) as cursor:
        cursor.execute("SELECT * FROM products LIMIT 5")

    mock_conn.commit.assert_called_once()#COMMIT вызвался
    mock_conn.rollback.assert_not_called()#Hе вызывался ROLLBACK
    mock_conn.close.assert_called_once()#Успешно завершилось подключение
    mock_cursor.close.assert_called_once()#Успешно завершился курсор

@patch("pipeline.utils.db_connection.psycopg2.connect")
#Тест завершения с ошибкой
def test_failure_connection(mock_connect,fake_settings):
    mock_conn = MagicMock()
    mock_cursor =MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    with pytest.raises(Exception):
        with DataBasePostgreSQLConnection(fake_settings) :
            raise Exception

    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_cursor.close.assert_called_once()
