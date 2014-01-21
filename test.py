import unittest
import encoders
import re
import base64

class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = encoders.Encoder()

    def test_no_subencoders(self):
        result = self.encoder.feed(b'foobar')
        self.assertEqual(b'foobar', result,
                         'With no encoders, the passed `data`'
                         ' argument should be returned by `Encoder.feed`.')

    def test_only_accept_bytes(self):
        try:
            self.encoder.feed(b'abc')
        except:
            self.fail('`bytes` was not accepted by `Encoder.feed`.')

        with self.assertRaises(TypeError):
            self.encoder.feed(123)
            self.encoder.feed('abc')

class TestHttpRequestLineEncoder(unittest.TestCase):
    def setUp(self):
        self.httpVerbs = ['GET', 'POST', 'HEAD']
        self.regexp = '(GET|POST|HEAD) ([A-Za-z0-9/_\\-]*=*) HTTP/1.1'
        self.encoder = encoders.HttpRequestLineEncoder()

    def test_verb_choice(self):
        for i in range(10):
            e = encoders.HttpRequestLineEncoder()
            self.assertIn(e.verb, self.httpVerbs)

    def test_invalid_verbs(self):
        with self.assertRaises(encoders.HttpRequestLineEncoder.InvalidHttpVerbError):
            e = encoders.HttpRequestLineEncoder(verb='FOO')

    def test_format(self):
        rest = data = b'abcdefghijklmnopqrstuvwxyz'
        while data != b'':
            self.encoder.feed(data)
            if rest == data:
                self.fail('Nothing was consumed.')
        output = self.encoder.getOutput()
        self.assertNotEqual(None, re.match(self.regexp, output))

    def test_encoding(self):
        rest = data = b'aaaaaaaa'
        while data != b'':
            rest = self.encoder.feed(data)
            if rest == data:
                self.fail('Nothing was consumed.')
        output = self.encoder.getOutput()
        encoded = re.match(self.regexp, output).group(2).replace('/', '')
        decoded = base64.urlsafe_b64encode(encoded)
        self.assertTrue(all(c == b'a' for c in decoded), 'Data not encoded correctly.')
            
if __name__ == '__main__':
    unittest.main()
