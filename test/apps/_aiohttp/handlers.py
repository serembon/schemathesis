import asyncio

from aiohttp import web


async def success(request: web.Request) -> web.Response:
    return web.json_response({"success": True})


async def invalid_response(request: web.Request) -> web.Response:
    return web.json_response({"random": "key"})


async def custom_format(request: web.Request) -> web.Response:
    return web.json_response({"value": request.query["id"]})


async def teapot(request: web.Request) -> web.Response:
    return web.json_response({"success": True}, status=418)


async def text(request: web.Request) -> web.Response:
    return web.Response(body="Text response", content_type="text/plain")


async def malformed_json(request: web.Request) -> web.Response:
    return web.Response(body="{malformed}", content_type="application/json")


async def failure(request: web.Request) -> web.Response:
    raise web.HTTPInternalServerError


async def slow(request: web.Request) -> web.Response:
    await asyncio.sleep(0.1)
    return web.json_response({"slow": True})


async def unsatisfiable(request: web.Request) -> web.Response:
    return web.json_response({"result": "IMPOSSIBLE!"})


async def flaky(request: web.Request) -> web.Response:
    config = request.app["config"]
    if config["should_fail"]:
        config["should_fail"] = False
        raise web.HTTPInternalServerError
    config["should_fail"] = True
    return web.json_response({"result": "flaky!"})


async def multipart(request: web.Request) -> web.Response:
    if not request.headers["Content-Type"].startswith("multipart/"):
        raise web.HTTPUnsupportedMediaType
    data = {field.name: (await field.read()).decode() async for field in await request.multipart()}
    return web.json_response(data)


path_variable = success
invalid = success
invalid_path_parameter = success
