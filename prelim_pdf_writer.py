#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

header = """

Created on Sat Nov 5 2022

@author: Victor Prieto

"""


# %% start runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% insert code below

def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')


if __name__ == '__main__':
    # Basic document
    doc = Document('basic')
    fill_document(doc)

    # doc.generate_pdf(clean_tex=False)  # FIXME why doesn't latexmk work??
    doc.generate_tex()

    # Document with `\maketitle` command activated
    doc = Document()

    doc.preamble.append(Command('title', 'Awesome Title'))
    doc.preamble.append(Command('author', 'Anonymous author'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    fill_document(doc)

    doc.generate_pdf('basic_maketitle', clean_tex=False)

    # Add stuff to the document
    with doc.create(Section('A second section')):
        doc.append('Some text.')

    doc.generate_pdf('basic_maketitle2', clean_tex=False)
    tex = doc.dumps()  # The document as string in LaTeX syntax
    
    filename_input = 'test'
    file_path = r'./output/'
    filename = file_path + filename_input
    doc.generate_tex()
    # doc.generate_pdf()


# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
