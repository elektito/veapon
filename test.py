import unittest
import encoders

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

if __name__ == '__main__':
    unittest.main()
