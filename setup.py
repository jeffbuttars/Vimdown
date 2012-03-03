from distutils.core import setup, Command
from unittest2 import TextTestRunner, TestLoader
import vimdown.tests

cmdclasses = dict()

class TestCommand(Command):
    """Runs the unit tests for vimdown"""

    user_options = []

    def initialize_options(self):
        """@todo: Docstring for initialize_options
        :returns: @todo
        """
    
        pass
    #initialize_options()

    def finalize_options(self, arg1):
        """@todo: Docstring for finalize_options
        
        :arg1: @todo
        :returns: @todo
        """
    
        pass
    #finalize_options()

    def run(self):
        """@todo: Docstring for run
        :returns: @todo
        """
    
        loader = TestLoader()
        t = TextTestRunner()
        t.run(loader.loadTestsFromModule(vimdown.tests))
    #run()
#TestCommand

# 'test' is the parameter as it gets added to setup.py
cmdclasses['test'] = TestCommand

setup(cmdclass = cmdclasses,
    name='vimdown',
    version='1.2.0',
    description="Convert Vim files to Markdown",
    author="Jeff Buttars",
    author_email="jeffbuttars@gmail.com",
    url="http://github.com/jeffbuttars/vimdown",
    download_url="https://github.com/downloads/jeffbuttars/Vimdown/vimdown-1.1.1.tar.gz",
    requires=["markdown2","unittest2"],
    provides=["vimdown"],
    scripts=["vimdown/vimdown"],
    py_modules=["vimdown.lexer", "vimdown.parser", "vimdown.tests.run_tests"],
    license="BSD",
)
