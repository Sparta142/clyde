import logging
import os

import clyde
from clyde.models.locale import Locale

logging.basicConfig(level=logging.DEBUG)

app = clyde.ClydeApp(os.environ['CLYDE_BOT_TOKEN'])


@app.chat_input(
    description='Show a random color',
    description_localizations={
        'en-GB': 'Show a random colour',
        Locale.SPANISH: 'Mostrar un color aleatorio',
        Locale.TR: 'Rastgele renk göster',
    }
)
async def color(
    ctx: clyde.Context,  # Required for all commands
    name: str,  # Variable length string
    integral: int,  # Any integer between -2^53 and 2^53
    is_cool: bool,  # True/false
):
    pass

app.run(port=80)
