from APISitter import APISitter
import unittest
import time

apikey = 10


def f(i):
    global apikey
    apikey += i
    return apikey


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_sitter = APISitter(15, f, 1)

    def test_01_new_key(self):
        ''' Tests creation of new key after timeout (15s) '''
        key = self.api_sitter.key
        time.sleep(16)
        self.assertNotEqual(key, self.api_sitter.key)

    def test_02_set_key(self):
        ''' Tests setting user-defined key and its replacement (15s)'''
        global apikey
        self.api_sitter.key = 0
        apikey = 0
        self.assertEqual(0, self.api_sitter.key)
        time.sleep(16)
        self.assertEqual(1, self.api_sitter.key)

    def test_03_time_remaining(self):
        ''' Tests time_remaining property '''
        self.api_sitter = APISitter(15, f, 1)
        self.api_sitter.key
        print(self.api_sitter.time_remaining)
        self.assertTrue(13 < self.api_sitter.time_remaining < 15)

    def test_04_set_time_remaining(self):
        ''' Tests setting user-defined time and its effects '''
        key = self.api_sitter.key
        self.api_sitter.time_remaining = 30
        time.sleep(16)
        self.assertEqual(key, self.api_sitter.key)

    def test_05_passing_args_to_fn(self):
        ''' Tests passing *args to fn (10s)'''
        self.api_sitter = APISitter(10, f, 4)
        key = self.api_sitter.key
        time.sleep(11)
        self.assertEqual(key + 4, self.api_sitter.key)

    def test_05_noncallable_exception(self):
        ''' Tests passing non-callable object as fn '''
        self.assertRaises(TypeError, APISitter, 30, None)

    def test_06_noninteger_timeout(self):
        ''' Tests passing non-integer value as timeout '''
        self.assertRaises(TypeError, APISitter, None, f)


if __name__ == '__main__':
    unittest.main(verbosity=2)
