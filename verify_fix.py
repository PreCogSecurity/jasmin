#!/usr/bin/env python
import re

content = open('misc/scripts/sms_logger.py').read()
print('=== sms_logger.py ===')
print('has_os: import os in content:', 'import os' in content)
print('has_environ: os.environ.get in content:', 'os.environ.get' in content)
has_guest_literal = bool(re.search(r"password\s*=\s*'guest'", content))
print('has_guest_literal:', has_guest_literal)
if has_guest_literal:
    print('WARNING: literal guest password still present in source!')
else:
    print('OK: no literal guest password in source - replaced with env var')

content2 = open('misc/doc/sources/faq/consume_MT_messages.py').read()
print()
print('=== consume_MT_messages.py ===')
print('has_os: import os in content:', 'import os' in content2)
print('has_environ: os.environ.get in content:', 'os.environ.get' in content2)
has_guest_literal2 = bool(re.search(r"password\s*=\s*'guest'", content2))
print('has_guest_literal:', has_guest_literal2)
if has_guest_literal2:
    print('WARNING: literal guest password still present in source!')
else:
    print('OK: no literal guest password in source - replaced with env var')