=================
 ebookgenerators
=================

This module is useful as an example of real world generators. They
have been used to some degree of success to help my mother. She's an
avid reader and kindle owner. She enjoys that she can up the font on
her kindle. She obtained some pdf's that were quite painful to read in
dead tree and on the kindle. Being the kind son I am I translated them
to the mobi format and emailed them to her kindle.

I've used these generators on about a dozen pdfs. Some tweaking is
required because the output of each pdf seems a bit different. YMMV

pdf to mobi
===========

My process went like this:

* use ``pdf2txt.py`` to get text of pdf files.
* inspect txt files and tweak to get them to rst if possible
* create a python generator pipeline to clean up text (using ``ebookgen``)
* use ``rst2epub2`` or ``rst2html`` to create mobi file
* email mobi file to someone@kindle.com

For normal people
=================

If you don't care about ebooks that much (or making your own), then
this library might be interesting as examples of real-world
generators. Of particular interest might be the ``Peeker`` class which
allows looking ahead in iterators. (This comes in often when tweaking
text).

There are also a few examples of basic generators and some fancier
ones that use ``Peeker``.

These generators aren't necessarily written in a functional style
using *map*, *reduce* and *filter*, though they probably could
be. Sorry.

Creating a generator chain
==========================

My script to clean the ``pdf2txt.py`` output looks something like this::


  import sys

  import ebookgen


  def run():
      data = sys.stdin
      data = ebookgen.remove_leading_space(data)
      data = ebookgen.remove_dash_page(data)
      data = ebookgen.remove_carot_l(data)
      data = ebookgen.remove_two_spaces(data)
      data = ebookgen.remove_double_returns(data)
      data = ebookgen.insert_extra_paragraph_line(data)
      data = ebookgen.insert_rst_sections(data)

      for line in data:
          print line,

  if __name__ == '__main__':
      run()


License
=======

MIT

Copyright
=========

Matt Harrison, 2012

