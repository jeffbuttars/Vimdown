#!/usr/bin/env python

import sys
from optparse import OptionParser

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

from pygments import  highlight
from pygments.lexers import VimLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

import lexer

def colorize(code, outfile):
	hf = HtmlFormatter(style='colorful')
	return "<style>%s</style>\n%s" % (hf.get_style_defs(),
					highlight(code, VimLexer(), hf))
#colorize()

def main():
	usage = ("%prog, Convert .vimrc and vimscript into markdown")

	parser = OptionParser(usage=usage)
	#parser.add_option("-f", "--configfile", dest='cfg_path', default="/etc/wpc/wpc.ini",
	#		help=("The path to the config file to read. If this is the only option"
	#	 	" given the entire config file will be printed to stdout"))

	#parser.add_option("-s", "--configsection", dest='cfg_section', default="",
	#		help=("The section in the config file to read. If this option is given but "
	#	 	"the --configoption is NOT, then the config section specified will be printed"
	#		" to stdout. NOTE: Specify the DEFAULT section to print out default section. "))

	parser.add_option("-o", "--outfile", dest='outfile', default=False,
			help=("Write the output to the given filename"))

	(options, args) = parser.parse_args()
	logging.debug("options:%s"%options)
	logging.debug("args:%s"%args)

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

	hf = HtmlFormatter(style='colorful')
	style_section = ("<style>\n%s\ndiv.vimdown_vim "
				  "{display:block;border:1px solid #888;"
				  "background-color:#E0E0E0;"
				  "padding:.5em 1em .5em 1em;"
				  "-webkit-border-radius: 5px;"
				  "-moz-border-radius: 5px;"
				  "border-radius: 5px;"
				  "}"
				  "\n</style>\n") % (hf.get_style_defs(),)
	#style_section = "<style>\n%s\n</style>\n" % (hf.get_style_defs(),)
	style_section = style_section.replace('*', '\*')

	for fl in infiles:
		logging.debug("opening file %s" % (fl,))
		fd = open(fl)
		blocks = lexer.lex(fd)
		#logging.debug(lexer.print_blocks(blocks, annotate=True))
		#outfile.write(lexer.print_blocks(blocks, annotate=True))
		#outfile.write(style_section)
		outfile.write(lexer.blocks_to_markdown(blocks))
		#hl = colorize(fd.read(), outfile)
		#logging.debug(hl)
		#outfile.write(hl.encode('utf-8'))
#main()

if __name__ == '__main__':
	main()
