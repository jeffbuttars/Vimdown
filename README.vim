" # Vimdown
"
"
" # Vimdown
" 
" ## TOC
" * [Overview](#overview)
" * [Usage](#usage)
" 	* [Basic](#usage_basic)
" 	* [Advanced](#usage_advanced)
" * [Examples](#examples)
" #### Vim comment lines as a code block
"
" 
" <a name="overview"></a>
" ## Overview
" Vimdown transforms .vim files into markdown documents.  
" Vimdown was born out of an itch to make my .vimrc look nice as the README.mkd file for my GitHub 
" repository that holds my .vim directory.  
" This README was written as a vim file and rendered to markdown with vimdown.  
" 
" Vimdown is a very simple parser. All it does is seperate a Vim file
" into blocks of text that either contiguous comments or contiguous
" non-comments. Blocks of comments are stripped of their comment 
" marks, '"', from the begining of the line and considered
" to be in markdown syntax. Non-comment blocks are considered 
" code blocks and are inserted into the resulting markdown document
" as explicit vim codeblocks. Only lines with the comment mark,
" '"', as the first or second character of the line are considered 
" comments. If the comment mark starts later in the line it will be
" considered code with a comment in the code block.
" 
" 
" <a name="usage" /></a>
" ## Usage
" Vimdown has built in help output
" <pre>
" > vimdown --help 
" </pre>
" 
"
" <a name="usage_basic" /></a>
" ### Basic
"
" Simply give the vimdown command a file or files to process and it will
" print out the result to stdout:
" <pre>
" > vimdown infile > outfile
" </pre>
"
" You can specify an output file:
" <pre>
" > vimdown  -o outfile infile
" </pre>
" 
" Using multiple input files:
" <pre>
" > vimdown infile infile2 infile3 -o outfile
" </pre>
" 
" 
" 
" 
" <a name="usage_advanced" /></a>
" ### Advanced
"
" #### Markdown2 code blocks
" You can have markdown2 style code blocks with -c :
" <pre>
" > vimdown -c -o outfile infile
" </pre>
"
" That will create code blocks in the markdown in the style of:
" <pre>
"     :::vim
"     code is here
" </pre>
" 
" 
" #### Render to HTML
" If you have markdown2 installed you can ask vimdown to render
" the markdown to HTML for you with the -t option.
"
" This will render a basic markdown document as HTML into
" the outfile
" <pre>
" > vimdown -t -o outfile infile
" </pre>
" 
" This will render a markdown document with markdown2 codeblocks as HTML into
" the outfile
" <pre>
" > vimdown -c -t -o outfile infile
" </pre>
"
" #### Pygments Styles
" If you have both Markdown2 and Pygments installed you can have 
" vimdown render the output as an HTML document with the code
" markup styled for Pygments. Use the -p option:
" <pre>
" > vimdown -p -o outfile infile
" </pre>
" 
" <a name="examples" /></a>
" ## Examples
" Everything you've seen in the document so far is an example of how vimdown
" renders comments in a vim file. 
"
" Comment blocks must have the '"' comment mark in the first or second character
" position of the line.  
"
" The comment block:
" <pre>
"" comment 
"" comment 
"" comment 
" </pre>
" will render as:  
" comment   
" comment   
" comment   
"
" Another comment block, the comment starts in an extra space:
" <pre>
"  " comment 
"  " comment 
"  " comment 
" </pre>
" renders as:  
 " comment   
 " comment   
 " comment  
"
" This will be considered a code block:  
" <pre>
"     " comment 
"     " comment 
"     " comment 
" </pre>
" rendered as:
"
  "  comment
  "  comment
  "  comment
"
" The following examples are how it will render 
" code blocks.  

if variable < 10
    let g:variable = 0
endif

" A code block with comments

if filereadable( tstr )
    " make sure our big ass bsd tags file
    " is used in subdirs as well.
    set tags+=tstr " comment at end of line
endif
