import site, sys, os, logging
site.addsitedir(os.path.dirname(__file__))

logging.basicConfig(stream = sys.stderr)

import filtering_site as application