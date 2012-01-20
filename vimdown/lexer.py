#!/usr/bin/env python

import re
import logging

from pygments import  highlight
from pygments.lexers import VimLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

# Allow tabs
iscomment = re.compile('^[ ]?"')
isspacey = re.compile('^\s*$')

# States
NON = 0
COMMENT = 1
NONCOMMENT = 2
state_map = {
		NON:"NON",
		COMMENT:"COMMENT",
		NONCOMMENT:"NONCOMMENT",
}

div_style = " -webkit-border-radius: 5px; -moz-border-radius: 5px; border-radius: 5px ;padding: .5em;"

def pygmentize(code, style='default'):
	hf = HtmlFormatter(style=style, noclasses=True,
					encoding='ascii', cssstyles=div_style)
	return highlight(code, VimLexer(), hf)
#pygmentize()

def lex(input):

	state = NON
	nstate = None 
	blocks = []
	block = {NON:[]}

	line = input.readline()
	while line:


		if iscomment.match(line):
			nstate = COMMENT
		else:
			nstate = NONCOMMENT

		if state != nstate:
			blocks.append(block)
			state = nstate
			block = {state:[]}

		block[state].append(line)
		line = input.readline()

	blocks.append(block)

	return blocks
#lex()

def print_blocks(blocks, annotate=True):

	res = ""
	for block in blocks:
		k,v = block.items()[0]
		if annotate:
			res = "%s\n%s++++++++++++++++++++++++++++\n%s" % (
					res, state_map[k], "".join(v)) 
		else:
			res = "%s%s" % (res, "".join(v)) 

	return res
#print_blocks()

def blocks_to_markdown(blocks, style='vim'):

	def strip_vcomment(str):
		#logging.debug("strip_vcomment %s" % (str,))
		res = ""

		# check for hard rule
		if str[0:10] == '""""""""""':
			return '__________\n\n'

		# Trim the comment and first space if it's easy
		if str[0:2] == '" ':
			res = str[2:]
		elif str[0:1] == '"':
			res = str[1:]
		else:
			# If the begining of the line is not predictable, 
			# do a dumb search and crop
			res = ("%s" % (str.partition('"')[2],))

		return res
	#strip_vcomment()

	res = [] 
	for block in blocks:
		k,v = block.items()[0]
		if k == NONCOMMENT:
			cont = "".join(v)
			if cont == '\n' or isspacey.match(cont):
				continue
			logging.debug("cont : '%s'" % cont)
				
			res.append("\n\n\n<div class=\"vimdown_vim\">\n%s</div>\n\n\n" % (pygmentize(cont, style)))
		if k == COMMENT:
			res.extend(map(strip_vcomment, v))
		if k == NON:
			continue
			
	return "".join(res)
#blocks_to_markdown()
