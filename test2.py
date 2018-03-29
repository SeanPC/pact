#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib import Misc
misc = Misc()
subject = 'Pact Notice'
sender = 'pact@veritas.com'
to = 'bentley.xu@veritas.com'
cc = 'bentley.xu@veritas.com'
content = '''
    Dear User,please contact bentley.
                                            bentely
                                                bentley
'''
print misc.sendMail(subject,content,sender,to,cc)
 