from sanic import Request
from helpers.routinghelper import render_template
from sanic.log import logger
from sanic import Sanic

app = Sanic.get_app("Portfolio")

@app.get("/")
async def about(request: Request) -> str:
    logger.info("Loading index page")
    return await render_template(request, "index.html")