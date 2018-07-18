# coding=utf-8

import sys

# compatible with Python 3.7
if sys.version_info.major == 3 and sys.version_info.minor >= 7:
    import re
    re._pattern_type = re.Pattern

broker_url = "redis://127.0.0.1:6379/11"
result_backend = ""

task_default_queue = "haha"
