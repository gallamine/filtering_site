import site
import sys
import os
import logging

site.addsitedir(os.path.dirname(__file__) + "/app")

logging.basicConfig(stream = sys.stderr)

