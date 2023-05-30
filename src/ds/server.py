from __future__ import annotations

from aiohttp import hdrs


class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST
