#!/usr/bin/env python

import sys
from optparse import OptionParser

import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

from pygments import  highlight
from pygments.lexers import VimLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles #, get_style_by_name

import lexer

def main():
	usage = ("%prog, Convert .vimrc and vimscript into markdown")

	parser = OptionParser(usage=usage)
	parser.add_option("-s", "--style", dest='style', default="friendly",
				   help=("Specify the pygments style to use. Default is friendly. Styles available:\n%s")
				   % (", ".join(get_all_styles()),)
				   )
	parser.add_option("-o", "--outfile", dest='outfile', default=False,
			help=("Write the output to the given filename"))

	(options, args) = parser.parse_args()
	logging.debug("options:%s"%options)
	logging.debug("args:%s"%args)

	style = options.style

	outfile = options.outfile
	if not outfile:
		outfile = sys.stdout
	else:
		outfile = open(outfile, 'w')

	infiles = []	
	if args:
		infiles += args
	else:
		infiles.append(sys.stdin)
		
	logging.debug("outfile : %s, infiles : %s" % (outfile, infiles))


	for fl in infiles:
		logging.debug("opening file %s" % (fl,))
		fd = open(fl)
		blocks = lexer.lex(fd)
		outfile.write(lexer.blocks_to_markdown(blocks, style))
#main()

if __name__ == '__main__':
	main()
