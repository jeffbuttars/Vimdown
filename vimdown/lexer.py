#!/usr/bin/env python

import re

iscomment = re.compile('^\s*"')

def lex(input):

	line = input.readline()
	while line:
		line = input.readline()
		if iscomment.match(line):
			print("COMMENT : %s" % (line,))
		else:
			print("NONCOMMENT : %s" % (line,))
#lex()
