import unittest

import ebookgen

class TestPeek(unittest.TestCase):
    def test_peeker(self):
        x = ebookgen.Peeker(range(10))
        self.assertEqual(x.peek(), 0)
        self.assertEqual(x.peek(1), 1)
        self.assertEqual(x.peek(1), 1)
        self.assertEqual(x.peek(2), 2)
        self.assertEqual(x.next(), 0)
        self.assertEqual(x.peek(), 1)
        self.assertEqual(x.peek(), 1)
        x.pop()
        self.assertEqual(x.peek(), 2)
        self.assertEqual(x.next(), 2)
        self.assertEqual(list(x), range(3,10))

        x = ebookgen.Peeker(range(1))
        self.assertEqual(x.peek(), 0)
        self.assertRaises(ebookgen.PeekDone, x.peek, 1)

        x = ebookgen.Peeker(range(2))
        self.assertEqual(x.peek(), 0)
        self.assertEqual(x.pop(), 0)
        self.assertEqual(x.peek(), 1)
        self.assertEqual(x.pop(), 1)
        self.assertRaises(ebookgen.PeekDone, x.peek)
        self.assertRaises(StopIteration, x.next)
        self.assertEqual(x.pop(), None)


if __name__ == '__main__':
    unittest.main()
