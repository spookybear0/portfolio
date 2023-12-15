from sanic_jinja2 import SanicJinja2
from helpers import routinghelper
import asyncio
import jinja2
import sanic

app = sanic.Sanic("Portfolio")
app.config.USE_UVLOOP = False
app.ctx.jinja = SanicJinja2(
    app,
    loader=jinja2.FileSystemLoader("./assets/html"),
    pkg_path="assets/html",
    extensions=["jinja2.ext.loopcontrols"],
    enable_async=True
)

routinghelper.add_all_routes(app)
app.static("assets", "assets", name="assets")

async def main() -> None:
    """
    Start the server in a development/nonprod environment.
    """

    server = await app.create_server(host="localhost", port=8500, debug=True, return_asyncio_server=True)

    await server.startup()
    await server.after_start()
    await server.serve_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Exiting...")