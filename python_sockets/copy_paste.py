import sys
from AppKit import *
from pykeyboard import PyKeyboard
import time


print "you have 5 seconds to highlight text"
time.sleep(5)

k = PyKeyboard()
# k.press_keys(['Command', 'a'])
k.press_keys(['Command', 'c'])

time.sleep(1)

pb = NSPasteboard.generalPasteboard()
pbstring = pb.stringForType_(NSStringPboardType)
print u"Pastboard string: %s".encode("utf-8") % repr(pbstring)




