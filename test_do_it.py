#!/usr/bin/python
# encoding: utf-8
import sys, os, unittest
sys.path.append(os.path.abspath('.'))
from do_it import *

class TestSomeStuff(unittest.TestCase):

    
    def setUp(self):
        pass

    def test_find_deelnummer(self):

        self.assertEqual(find_deelnummer('I, 1, 2, 3')[0].start() , 0)
        self.assertEqual(find_deelnummer('12345I, 1, 2, 3')[0].start() , 5)
        self.assertEqual(find_deelnummer('zie 12345I, 1, 2, 3')[0].start() , 0)
        self.assertEqual(find_deelnummer('zie 12345I, 1, 2, 3')[0].end() , 4)
        self.assertEqual(find_deelnummer('I, 1')[0].end(), 3)

        self.assertEqual(find_deelnummer('I, 1; II, 2')[0].end(), 3) 
        self.assertEqual(find_deelnummer('1; II, 2')[0].start(), 3) 
        self.assertEqual(find_deelnummer('1; II, 2')[0].end(), 7) 
        self.assertEqual(find_deelnummer('zie Frederik I, koning van Pruisen.')[1], 'zie')

    def test_teg_pages(self):
        self.assertEqual(tag_pages('I, 1; II, 2', 1), 'I, <page deel="I" number="1">1</page>; II, <page deel="II" number="2">2</page>')
        self.assertEqual(tag_pages('zie abc', 1), '<zie>zie abc</zie>')
        self.assertEqual(tag_pages('I, 1', 1), 'I, <page deel="I" number="1">1</page>')
        self.assertEqual(tag_pages('xxx I, 1 yyy', 1), 'xxx I, <page deel="I" number="1">1</page> yyy')
        self.assertEqual(tag_pages('I, 1, 2, 3 yyy', 1), \
           'I, <page deel="I" number="1">1</page>, <page deel="I" number="2">2</page>, <page deel="I" number="3">3</page> yyy'
            )

        self.assertEqual(tag_pages('abcd: I, 1 ',0), '<naam>abcd</naam>: I, <page deel="I" number="1">1</page> ')

    def test_parse_line(self):
        self.assertEqual(parse_line('Frederik III, keurvorst van Brandenburg 1688‑1701: zie Frederik I, koning van Pruisen.', 1), '<naam>Frederik III, keurvorst van Brandenburg 1688\xe2\x80\x911701:</naam><references> <zie>zie Frederik I, koning van Pruisen</zie></references></item>\n')
if __name__ == '__main__':
    unittest.main()
