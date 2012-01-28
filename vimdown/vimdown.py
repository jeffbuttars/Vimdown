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

	def __init__(self, fl, m2code=False, pyg=False):

		logging.debug("Parser(fl:%s, m2code:%s)" % (fl, m2code))
		self.fd = open(fl)

		self.m2code = m2code
		self.pyg = pyg
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
					
				if self.m2code:
					cb = "\n    :::vim\n    %s\n" % (cont)
				else:
					cb = "\n    %s\n" % (cont)
				logging.debug("code block : %s" % cb)
				res.append(cb)
					
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
		import markdown2
		blocks = self.parse()
		mkd = self.blocks_to_markdown(blocks)
		if self.pyg:
			logging.debug("Parser.gen_html() codehilite")
			return markdown2.markdown(mkd, extras=['codehilite'])
		else:
			logging.debug("Parser.gen_html()")
			return markdown2.markdown(mkd)
	#gen_html()
#Parser

def main():
	usage = ("%prog, Convert .vimrc and vimscript into markdown")

	parser = OptionParser(usage=usage)
	parser.add_option("-o", "--outfile", dest='outfile', default=False,
			help=("Write the output to the given filename"))
	parser.add_option("-t", "--html", dest='html', action='store_true', default=False,
			help=("If markdown2 is present then vimdown will"
		 		" will process the markdown using markdown2 and"
		 		" and output the resulting HTML"
			))
	parser.add_option("-c", "--codeblock", dest='codeblock', action='store_true', default=False,
			help=("If set, the code blocks in the generated markdown will be"
		 		" the markdown2 extended syntax."
			))
	parser.add_option("-p", "--pygmentize", dest='pygmentize', action='store_true', default=False,
			help=("If markdown2 is present then vimdown will"
		 		" will output html using markdown2's pygments"
		 		" code coloring. If this option is present the --html and --codeblock"
		 		" options are implied."
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
		parser = Parser(fl, m2code=options.codeblock, pyg=options.pygmentize)
		res = ""
		if options.html or options.pygmentize:
			res = parser.gen_html().encode('utf-8')
		else:
			res = parser.gen_markdown()
			
		outfile.write(res)
#main()

if __name__ == '__main__':
	main()
