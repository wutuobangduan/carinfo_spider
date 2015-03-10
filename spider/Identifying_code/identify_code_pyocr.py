#!/usr/bin/env python
from PIL import Image

import sys
from pyocr import pyocr
from pyocr import builders
from pyocr import cuneiform
from pyocr import tesseract

tools = pyocr.get_available_tools()[:]
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
print("Using '%s'" % (tools[0].get_name()))
tools[0].image_to_string(Image.open('showphone4.gif')) 
