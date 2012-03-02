from distutils.core import setup

setup(name='vimdown',
	  version='1.1.1',
	  description="Convert Vim files to Markdown",
	  author="Jeff Buttars",
	  author_email="jeffbuttars@gmail.com",
	  url="http://github.com/jeffbuttars/vimdown",
      download_url="https://github.com/downloads/jeffbuttars/Vimdown/vimdown-1.1.1.tar.gz",
	  requires=["markdown2",],
	  provides=["vimdown"],
	  scripts=["vimdown/vimdown"],
      py_modules=["vimdown.lexer", "vimdown.parser"],
	  license="BSD",
	)
