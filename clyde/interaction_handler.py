from .models.interactions import (
    Interaction,
    InteractionCallbackData,
    InteractionCallbackType,
    InteractionResponse,
)
from .models.messages import MessageFlags


class InteractionHandler:
    async def handle_ping(
        self,
        interaction: Interaction,
    ) -> InteractionResponse:
        return InteractionResponse(type=InteractionCallbackType.PONG)

    async def handle_application_command(
        self,
        interaction: Interaction,
    ) -> InteractionResponse:
        return InteractionResponse(
            type=InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            data=InteractionCallbackData(
                content='It works!',
                flags=MessageFlags.EPHEMERAL,
            ),
        )

    async def handle_message_component(
        self,
        interaction: Interaction,
    ) -> InteractionResponse:
        raise NotImplementedError()
