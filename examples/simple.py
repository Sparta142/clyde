import logging
import os

import clyde

logging.basicConfig(level=logging.DEBUG)

app = clyde.ClydeApp(os.environ['CLYDE_BOT_TOKEN'])
app.run(port=80)
