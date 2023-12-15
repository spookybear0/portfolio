import os
import sys
import importlib.util
from sanic import Sanic
from sanic.log import logger

def import_from_dir(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

path = os.path.dirname(os.path.abspath(__file__)) + "/../"
routes = []

def add_all_routes(app: Sanic):
    def import_dir(directory):
        sys.path.append(directory)
        for f in os.listdir(directory):
            if os.path.isdir(directory + f) and f not in ["__pycache__"]:
                import_dir(directory + f + "/")
            elif os.path.isfile(directory + f) and f not in ["__init__.py"]:
                logger.info(f"Importing {directory}{f}")
                mod = import_from_dir(f.rstrip(".py"), directory + f)
                routes.append(mod)

    import_dir(path + "handlers/")

async def render_template(r, template, *args, **kwargs) -> str:
    app = Sanic.get_app("Portfolio")
    additional_kwargs = {
        
    }

    kwargs = {**kwargs, **additional_kwargs}

    text = await app.ctx.jinja.render_async(template, r, *args, **kwargs)
    return text