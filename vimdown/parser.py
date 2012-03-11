import re
import logging

from lexer import Lexer

logger = logging.getLogger('vimdown.parser')

_parser_instance = None


class Parser(object):

    COMMENT = 'COMMENT'
    CODE = 'CODE'

    def __init__(self, fl, m2code=False, ghubf=False,
                 pyg=False, nofolds=False, foldmarker='{{{,}}}'):

        logger.debug(("Parser(fl:%s, m2code:%s, pyg:%s, "
                      "nofolds:%s, foldmarker:%s)")
                     % (fl, m2code, pyg, nofolds, foldmarker))
        self.fd = open(fl)

        self.ghubf = ghubf
        self.m2code = m2code or pyg
        self.pyg = pyg
        self.nofolds = nofolds
        self.foldmarker = foldmarker

        # GitHub code fences take precedence
        if self.ghubf:
            self.m2code = False
            self.pyg = False

        self.isspacey = re.compile('^\s*$')

        self.lexer = Lexer(vim_rules,
                           case_sensitive=True,
                           omit_whitespace=False,
                           )

        global _parser_instance
        _parser_instance = self
    #__init__()

    def block_to_markdown(self, state, block):
        logger.debug("\nblock_to_markdown %s:%s" % (state, block))
        if not (state and block):
            return ""

        res = []
        if state == Parser.CODE:

            # A super dirty and crapy way to remove
            # leading and trailing empty lines.
            while block and self.isspacey.match(block[0]):
                block.pop(0)
            while block and self.isspacey.match(block[-1:][0]):
                block.pop()

            # We ignore empty code blocks
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
            logger.debug("code block : '%s'" % cb)
            res.append(cb)

        if state == Parser.COMMENT:
            res.extend(block)

        return "".join(res)
    #block_to_markdown()

    def parse(self):
        """
            A Very simple parser. Simply groups contiguous types of tokens
            together.

        TODO: Get rid of the inner for loop. Need to be able to feed the lexer
        the file object or an iterable wrapper around it so we can simplifiy
        the line reading into the scanner/lexer.
        """

        state = ""
        nstate = None
        block = []
        mkd_res = ""

        lineno = 1
        while 1:
            line = self.fd.readline()
            logger.debug("\nscanning lineno %s:'%s'" % (lineno, line,))

            if not line:
                break
            lineno += 1

            for token in self.lexer.scan(line):
                logger.debug(token)

                nstate = token[0]
                tok = token[1]

                if state != nstate:
                    # logger.debug("\n new state %s" % (nstate))
                    mkd_res += self.block_to_markdown(state, block)
                    block = []
                    state = nstate

                block.append(tok)

            # logger.debug("\n parse bottom" )
        mkd_res += self.block_to_markdown(state, block)
        return mkd_res
    #parse()

    gen_markdown = parse

    def gen_html(self):
        import markdown2
        mkd = self.parse()
        if self.pyg:
            logger.debug("Parser.gen_html() codehilite\n mkd:%s" % (mkd,))
            return markdown2.markdown(mkd, extras={'code-color': None})
        else:
            logger.debug("Parser.gen_html()\n mkd:%s" % (mkd,))
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

    # logger.debug("strip_vcomment %s" % (str,))
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

    if _parser_instance and _parser_instance.nofolds:
        # Strip any fold markers
        markers = _parser_instance.foldmarker.split(',')
        fold_start_marker = markers[0]
        fold_end_marker = markers[1]

        fold_start_re = '%s\d*' % (fold_start_marker,)
        res = re.sub(fold_start_re, '', res, count=1)

        fold_end_re = '%s\d*' % (fold_end_marker,)
        res = re.sub(fold_end_re, '', res, count=1)

    # logger.debug("strip_vim_comment() res : '%s'" % (res,))
    return res
    # return Parser.strip_nl(scanner, res)
#strip_vim_comment()


vim_rules = [
    (Parser.CODE, '^(?!\s?").*\n?'),
    (Parser.COMMENT, ('^\s?".*\n?', strip_vim_comment)),

]
