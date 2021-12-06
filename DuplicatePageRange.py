#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
VERSION: 1.0 of 2021-11-06
AUTHOR: BASTIAN ILSØ HOUGAARD. 
LICENSE: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY.

Parts of this script are based on the MonthlyCalendar script by Rafferty River.
"""
######################################################
# imports
from __future__ import division # overrules Python 2 integer division
import sys
import locale
import platform

try:
    from scribus import *
except ImportError:
    print("This Python script is written for the Scribus \
      scripting interface.")
    print("It can only be run from within Scribus.")
    sys.exit(1)

python_version = platform.python_version()
if python_version[0:1] != "3":
    print("This script runs only with Python 3.")
    messageBox("Script failed",
        "This script runs only with Python 3.",
        ICON_CRITICAL)	
    sys.exit(1)

######################################################
def main():
    """ Application/Dialog loop with Scribus sauce around """
    try:
        statusMessage('Running script...')
        progressReset()
        
        page_range = valueDialog('Specify page range', 'Specify Page Range (fx. 1-5)','1-' + str(currentPage()))
        page_range = page_range.split('-')
        page_range = (int(page_range[0]), int(page_range[1]))
        import_range = range(page_range[0],page_range[1]+1)
        
        pcount = range(0, page_range[1] - page_range[0]+1)
                                              
        dup_amount = valueDialog('Copies', 'Specify Number of Copies','1')
        dup_amount = int(dup_amount)                                              
        
        docname = getDocName()
        
        # Collect Master Pages
        m = []
        for p in pcount:
            m.append(getMasterPage(page_range[0]+p))
        
        # Duplicate pages and apply master pages
        anchor = page_range[1]+1
        for d in range(dup_amount):
            importPage(docname, tuple(import_range))
            for p in pcount:
                if (len(m[p]) > 0):
                    applyMasterPage(m[p], anchor+p)
            anchor = pageCount()+1
        

    finally:
        if haveDoc() > 0:
            redrawAll()
        statusMessage('Done.')
        progressReset()

if __name__ == '__main__':
    main()

