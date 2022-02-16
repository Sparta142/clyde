from typing import Awaitable, Callable

from aiohttp.web import HTTPUnauthorized, Request, StreamResponse, middleware
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def validate_signature(key: VerifyKey):
    """
    Create a middleware that validates inbound Discord interactions
    against the provided ``key`` using the request's
    ``X-Signature-Ed25519`` and ``X-Signature-Timestamp`` headers.
    """

    @middleware
    async def _impl(
        request: Request,
        handler: Callable[[Request], Awaitable[StreamResponse]],
    ) -> StreamResponse:
        try:
            signature = request.headers['X-Signature-Ed25519']
            timestamp = request.headers['X-Signature-Timestamp']
        except KeyError as e:
            raise HTTPUnauthorized(text='Missing request signature') from e

        # The signed message is the decoded body prefixed with the timestamp
        body = await request.text()
        smessage = (timestamp + body).encode()

        try:
            key.verify(smessage, bytes.fromhex(signature))
        except BadSignatureError as e:
            raise HTTPUnauthorized(text='Invalid request signature') from e

        # Everything looks good, continue as normal
        return await handler(request)

    return _impl
