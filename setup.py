from distutils.core import setup

setup(name='vimdown',
	  version='1.1.0',
	  description="Convert Vim files to Markdown",
	  author="Jeff Buttars",
	  author_email="jeffbuttars@gmail.com",
	  url="http://github.com/jeffbuttars/vimdown",
      download_url="https://github.com/downloads/jeffbuttars/Vimdown/vimdown-1.1.0.tar.gz",
	  requires=["markdown2",],
	  provides=["vimdown"],
	  scripts=["vimdown/vimdown"],
	  license="BSD",
	)
