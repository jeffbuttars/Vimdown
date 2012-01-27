#!/usr/bin/env python

import sys, re, logging
from optparse import OptionParser

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class Parser(object):

	# States
	NON = 0
	COMMENT = 1
	NONCOMMENT = 2
	state_map = {
			NON:"NON",
			COMMENT:"COMMENT",
			NONCOMMENT:"NONCOMMENT",
	}

	def __init__(self, fl):

		logging.debug("Parser(fl:%s)" % (fl,))
		self.fd = open(fl)

		self.iscomment = re.compile('^\s?"')
		#isspacey = re.compile('^\s*$')
	#__init__()

	def parse(self):

		state = Parser.NON
		nstate = None 
		blocks = []
		block = {Parser.NON:[]}

		line = self.fd.readline()
		while line:


			if self.iscomment.match(line):
				nstate = Parser.COMMENT
			else:
				nstate = Parser.NONCOMMENT

			if state != nstate:
				blocks.append(block)
				state = nstate
				block = {state:[]}

			block[state].append(line)
			line = self.fd.readline()

		blocks.append(block)

		return blocks
	#parse()

	#def print_blocks(self, blocks, annotate=True):

	#	res = ""
	#	for block in blocks:
	#		k,v = block.items()[0]
	#		if annotate:
	#			res = "%s\n%s++++++++++++++++++++++++++++\n%s" % (
	#					res, state_map[k], "".join(v)) 
	#		else:
	#			res = "%s%s" % (res, "".join(v)) 

	#	return res
	##print_blocks()

	def blocks_to_markdown(self, blocks):

		# remove the Vim comment character
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
			#return res.replace("\n", "  \n")
		#strip_vcomment()

		res = [] 
		for block in blocks:
			k,v = block.items()[0]
			if k == Parser.NONCOMMENT:
				#if cont == '\n' or isspacey.match(cont):
				if v == '\n':
					continue
				cont = "    ".join(v)
				logging.debug("cont : '%s'" % cont)
					
				#res.append("\n\n\n<div class=\"vimdown_vim\">\n%s</div>\n\n\n" % (pygmentize(cont)))
				#res.append("\n    :::vim\n%s\n" % (cont))
				logging.debug("code block : \n'    %s'\n" % cont)
				res.append("\n    %s\n" % (cont))
			if k == Parser.COMMENT:
				res.extend(map(strip_vcomment, v))
			if k == Parser.NON:
				continue
				
		return "".join(res)
	#blocks_to_markdown()

	def gen_markdown(self):
		blocks = self.parse()
		return self.blocks_to_markdown(blocks)
	#gen_markdown()

	def gen_html(self):
		pass
	#gen_html()
#Parser

def main():
	usage = ("%prog, Convert .vimrc and vimscript into markdown")

	parser = OptionParser(usage=usage)
	parser.add_option("-o", "--outfile", dest='outfile', default=False,
			help=("Write the output to the given filename"))
	parser.add_option("-t", "--html", dest='html', default=False,
			help=("If markdown2 is present then vimdown will"
		 		" will process the markdown using markdown2 and"
		 		" and output the resulting HTML"
			))
	parser.add_option("-p", "--pygmentize", dest='pygmentize', default=False,
			help=("If markdown2 is present then vimdown will"
		 		" will output html using markdown2's pygments"
		 		" code coloring. If this option is present the --html"
		 		" option is implied."
			))
	parser.add_option("-c", "--codeblock", dest='codeblock', default=False,
			help=("If set, the code blocks in the generated markdown will be"
		 		" the markdown2 extended syntax."
			))

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

	for fl in infiles:
		#logging.debug(parser.print_blocks(blocks, annotate=True))
		parser = Parser(fl)
		outfile.write(parser.gen_markdown())
#main()

if __name__ == '__main__':
	main()
