import unittest
import json
from io import StringIO
from unittest import mock
from unittest.mock import mock_open, patch

from merge import SwaggerMerger

class TestSwaggerMerger(unittest.TestCase):

    def test_recursive_merge(self):
        sm = SwaggerMerger()
        d1 = {
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "username": {
                    "type": "string",
                    "maxLength": 30,
                    "minLength": 2
                }
            }    
        }
        d2 = {
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                }
            }
        }
        expected = {
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "username": {
                    "type": "string",
                    "maxLength": 30,
                    "minLength": 2
                }
            }
        }
        self.assertEqual(sm.recursive_merge(d1, d2), expected)


    @patch("builtins.open", new_callable=mock_open, read_data='{"foo": 42}')
    @patch("json.dump")
    @patch("json.load")
    def test_run(self, mock_load, mock_dump, mock_open):
        sm = SwaggerMerger(input1="foo.json", input2="bar.json", output="out.json")
        mock_load.side_effect = lambda f: {"foo": 42}
        sm.run()
        mock_load.assert_has_calls([mock.call(mock_open.return_value), mock.call(mock_open.return_value)])
        mock_dump.assert_called_once_with({"foo": 42}, mock_open.return_value, indent=4)


if __name__ == '__main__':
    unittest.main()