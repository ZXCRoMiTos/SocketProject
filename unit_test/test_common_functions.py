import sys
import os
import time
import unittest
from unittest.mock import patch
from unittest import mock
sys.path.append(os.path.join(os.getcwd(), '..'))
from main.common_functions import decode_message, encode_message, create_address, is_ip, send_message, receive_message
from main.settings import DEFAULT_IP, DEFAULT_PORT, DEFAULT_ANSWERS


class TestCommonFunctions(unittest.TestCase):

    def test_decode_message(self):
        test = decode_message(b'{"response": 200, "alert": "Success"}')
        self.assertEqual(test, {"response": 200, "alert": "Success"})

    def test_decode_message_dict_value_error(self):
        self.assertRaises(ValueError, decode_message, b'"some_str"')

    def test_decode_message_bytes_value_error(self):
        self.assertRaises(ValueError, decode_message, 'some_str')

    def test_encode_message(self):
        test = encode_message({"response": 200, "alert": "Success"})
        self.assertEqual(test, b'{"response": 200, "alert": "Success"}')

    def test_encode_message_wrong(self):
        self.assertRaises(TypeError, encode_message, ["response", "200", "alert", "Success"])

    def test_is_ip(self):
        self.assertTrue(is_ip('127.0.0.1'))

    def test_is_ip_wrong(self):
        self.assertFalse(is_ip('wrong'))

    def test_create_address(self):
        test_argv = ['', '-ip', '127.0.0.1', '-p', '7777']
        with patch.object(sys, 'argv', test_argv):
            test = create_address()
            self.assertEqual(test, ('127.0.0.1', 7777))

    def test_create_address_wrong_port(self):
        test_argv = ['', '-ip', '127.0.0.1', '-p', '77777']
        with patch.object(sys, 'argv', test_argv):
            self.assertRaises(SystemExit, create_address)

    def test_create_address_wrong_ip(self):
        test_argv = ['', '-ip', '127.0.0.а', '-p', '7777']
        with patch.object(sys, 'argv', test_argv):
            self.assertRaises(SystemExit, create_address)

    def test_create_address_none_ip(self):
        test_argv = ['', '-ip', '-p', '7777']
        with patch.object(sys, 'argv', test_argv):
            self.assertRaises(SystemExit, create_address)

    def test_create_address_none_port(self):
        test_argv = ['', '-ip', '127.0.0.1', '-p', 'port']
        with patch.object(sys, 'argv', test_argv):
            self.assertRaises(SystemExit, create_address)

    def test_create_address_default(self):
        self.assertEqual(create_address(), (DEFAULT_IP, DEFAULT_PORT))

    def test_send_message(self):
        client = mock.Mock()
        message = DEFAULT_ANSWERS['presence']
        self.assertIsNone(send_message(client, message))

    def test_receive_message(self):
        msg = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": "guest",
                "status": "I'm here"
            }
        }
        client = mock.Mock()
        client.recv.return_value = encode_message(msg)
        self.assertEqual(receive_message(client), msg)


if __name__ == '__main__':
    unittest.main()