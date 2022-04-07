from importlib import import_module

from sanic import Sanic

def setup_modules(app: Sanic, *module_names: str) -> None:
    """
    Load some modules
    """
    for module_name in module_names:
        print(module_name)
        module = import_module(module_name)
        if bp := getattr(module, "bp", None):
            app.blueprint(bp)