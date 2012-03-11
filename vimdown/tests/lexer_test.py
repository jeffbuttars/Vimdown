#!/usr/bin/env python
# encoding: utf-8

import logging
import os
import sys 
import unittest2 as unittest

# Tweak the sys.path to include the local vimdown if we think it's here
THIS_DIR_ROOT = os.path.dirname(os.path.realpath(__file__))
THIS_DIR_PARENT_ROOT = os.path.normpath(os.path.join(THIS_DIR_ROOT, '../'))

if (os.path.basename(THIS_DIR_PARENT_ROOT) == 'vimdown') and os.path.exists(
    os.path.join(THIS_DIR_PARENT_ROOT, 'lexer.py')):
    sys.path.insert(0, os.path.normpath(os.path.join(THIS_DIR_PARENT_ROOT, '../')))
    # logging.basicConfig(level=logging.DEBUG)

from vimdown.lexer import Lexer
import vimdown.parser

class TestVimdownLexer(unittest.TestCase):

    def setUp(self):
        """@todo: Docstring for setUp
        :returns: @todo
        """
        self.lexer = Lexer(vimdown.parser.vim_rules,
                           case_sensitive=True,
                           omit_whitespace=False,
                           )
    #setUp()

    def test_simple_token_comment(self):
        """@todo: Docstring for simple_token_comment
        :returns: @todo
        """

        in_str = ("\"comment line 1\n"
                  " \"comment line 2")
        res = []

        for token in self.lexer.scan(in_str):
            self.assertEqual(vimdown.parser.Parser.COMMENT, token[0])
            res.append(token) 

    #test_simple_token_comment()

    def test_simple_token_code(self):
        """@todo: Docstring for simple_token_code
        :returns: @todo
        """
    
        pass
    #test_simple_token_code()

#TestVimdownLexer
