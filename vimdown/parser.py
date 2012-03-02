import re
import logging

from lexer import Lexer


class Parser(object):

    COMMENT = 'COMMENT'
    CODE = 'CODE'

    def __init__(self, fl, m2code=False, ghubf=False, pyg=False):

        logging.debug("Parser(fl:%s, m2code:%s, pyg:%s)" % (
            fl, m2code, pyg))
        self.fd = open(fl)

        self.ghubf = ghubf
        self.m2code = m2code or pyg
        self.pyg = pyg

        # GitHub code fences take precedence
        if self.ghubf:
            self.m2code = False
            self.pyg = False

        self.isspacey = re.compile('^\s*$')

        self.lexer = Lexer(vim_rules,
                           case_sensitive=True,
                           omit_whitespace=False,
                           )
    #__init__()

    def block_to_markdown(self, state, block):
        logging.debug("block_to_markdown %s:%s" % (state, block))
        if not (state and block):
            return ""

        res = []
        if state == Parser.CODE:

            # A super dirty and crapy way to remove
            # leading a trailing empty lines.
            while block and self.isspacey.match(block[0][0]):
                block.pop(0)
            while block and self.isspacey.match(block[-1:][0]):
                block.pop()

            # We look for and ignore empty code blocks
            if not block:
                return ""

            if self.ghubf:
                cont = "".join(block)
                cb = "\n```vim\n%s```\n" % (cont)
            else:
                cont = "    ".join(block)
                cb = "\n    %s" % (cont)
                if self.m2code:
                    cb = "\n    :::vim%s" % (cb)
            logging.debug("code block : '%s'" % cb)
            res.append(cb)

        if state == Parser.COMMENT:
            res.extend(block)

        return "".join(res)
    #block_to_markdown()

    def parse(self):
        """
            A Very simple parser. Simply groups contiguous types of tokens
            together.
        """

        state = ""
        nstate = None
        block = []
        mkd_res = ""

        lineno = 1
        while 1:
            line = self.fd.readline()
            logging.debug("scanning lineno %s:'%s'" % (lineno, line,))

            if not line:
                break
            lineno += 1

            for token in self.lexer.scan(line):
                logging.debug(token)

                nstate = token[0]
                tok = token[1]

                if state != nstate:
                    mkd_res += self.block_to_markdown(state, block)
                    state = nstate
                    block = []

                block.append(tok)

                mkd_res += self.block_to_markdown(state, block)

        return mkd_res
    #parse()

    def gen_markdown(self):
        return self.parse()
    #gen_markdown()

    def gen_html(self):
        import markdown2
        mkd = self.parse()
        if self.pyg:
            logging.debug("Parser.gen_html() codehilite\n mkd:%s" % (mkd,))
            return markdown2.markdown(mkd, extras={'code-color': None})
        else:
            logging.debug("Parser.gen_html()\n mkd:%s" % (mkd,))
            return markdown2.markdown(mkd)
    #gen_html()
#Parser


def strip_nl(scanner, token):
    """Strips the newline off the end of a token

    :scanner: @todo
    :token: @todo
    :returns: token
    """
    # print("strip_nl %s" % (token,))
    # return ""

    return token.rstrip("\n")
#strip_nl()


def strip_vim_comment(scanner, token):
    """@todo: Docstring for strip_vim_comment

    :arg1: @todo
    :returns: @todo
    """

    # logging.debug("strip_vcomment %s" % (str,))
    res = ""

    # check for hard rule
    if token[0:10] == '""""""""""':
        return '__________\n\n'

    # Trim the comment and first space if it's easy
    if token[0:2] == '" ':
        res = token[2:]
    elif token[0:1] == '"':
        res = token[1:]
    else:
        # If the begining of the line is not predictable,
        # do a dumb search and crop
        res = ("%s" % (token.partition('"')[2],))

    return res
    # return Parser.strip_nl(scanner, res)
#strip_vim_comment()

vim_rules = [
    (Parser.CODE, '^(?!\s?").*\n$'),
    (Parser.COMMENT, ('^\s?".*\n$', strip_vim_comment)),
]
