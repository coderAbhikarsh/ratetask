from unittest import TestCase
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.service.rates_service import RatesService


class TestRatesService(TestCase):

    def setUp(self):
        self.connection = MagicMock()
        self.rates_service = RatesService(self.connection)

    @patch('src.service.rates_service.RatesService._check_port_code')
    def test_get_rates_origin_code_destination_code(self, mock_port_code):
        """
        Test case for when both origin and destination are port codes

        """
        mock_port_code.return_value = []
        mock_cursor = MagicMock()
        self.connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = MagicMock()
        mock_cursor.fetchall.return_value = [(1124.5, 3, datetime.strptime("2016-01-11", "%Y-%m-%d"))]

        _input = {"date_from": "2016-01-10", "date_to": "2016-01-11", "origin": "DEBRV", "destination": "CNLYG"}
        expected_output = [{"average_price": 1124.5, "day": "2016-01-11"}]
        response = self.rates_service.get_rates(**_input)
        self.assertEqual(response, expected_output)

    @patch('src.service.rates_service.RatesService._check_port_code')
    def test_get_rates_origin_slug_destination_code(self, mock_port_code):
        """
        Test case for when origin could be a slug/parent_slug and destination is port code

        """
        mock_port_code.side_effect = [["north_europe_main"], []]
        mock_cursor = MagicMock()
        self.connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = MagicMock()
        mock_cursor.fetchall.return_value = [(1124.5, 3, datetime.strptime("2016-01-11", "%Y-%m-%d"))]

        _input = {"date_from": "2016-01-10", "date_to": "2016-01-11", "origin": "north_europe_main",
                  "destination": "CNLYG"}
        expected_output = [{"average_price": 1124.5, "day": "2016-01-11"}]
        response = self.rates_service.get_rates(**_input)
        self.assertEqual(response, expected_output)

    @patch('src.service.rates_service.RatesService._check_port_code')
    def test_get_rates_origin_port_destination_slug(self, mock_port_code):
        """
        Test case for when origin is a port code and destination could be a slug/parent_slug

        """
        mock_port_code.side_effect = [[], ["north_europe_main"]]
        mock_cursor = MagicMock()
        self.connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = MagicMock()
        mock_cursor.fetchall.return_value = [(1124.5, 3, datetime.strptime("2016-01-11", "%Y-%m-%d"))]

        _input = {"date_from": "2016-01-10", "date_to": "2016-01-11", "origin": "DEBRV",
                  "destination": "north_europe_main"}
        expected_output = [{"average_price": 1124.5, "day": "2016-01-11"}]
        response = self.rates_service.get_rates(**_input)
        self.assertEqual(response, expected_output)

    @patch('src.service.rates_service.RatesService._check_port_code')
    def test_get_rates_origin_slug_destination_slug(self, mock_port_code):
        """
        Test case for when both origin and destination could be slug/parent_slug

        """
        mock_port_code.return_value = ["north_europe_main"]
        mock_cursor = MagicMock()
        self.connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = MagicMock()
        mock_cursor.fetchall.return_value = [(1124.5, 3, datetime.strptime("2016-01-11", "%Y-%m-%d"))]

        _input = {"date_from": "2016-01-10", "date_to": "2016-01-11", "origin": "north_europe_main",
                  "destination": "north_europe_main"}
        expected_output = [{"average_price": 1124.5, "day": "2016-01-11"}]
        response = self.rates_service.get_rates(**_input)
        self.assertEqual(response, expected_output)
