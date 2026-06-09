"""Banner beim Start des Servers."""

import sys
from collections import namedtuple
from getpass import getuser
from importlib.metadata import version
from locale import getlocale
from socket import gethostbyname, gethostname
from sysconfig import get_platform
from types import FunctionType
from typing import Final

import fastapi
import pydantic
import starlette
from loguru import logger
from pyfiglet import Figlet
from starlette.routing import BaseRoute, Route
from tabulate import tabulate

TableEntry = namedtuple("TableEntry", "pfad http_methoden funktion")


def _route_to_table_entry(route: Route) -> TableEntry:
    """Route als Tupel mit Pfad, HTTP-Methode, implementierende Funktion."""
    endpoint: Final = route.endpoint
    qualname: Final = (
        endpoint.__qualname__ if isinstance(endpoint, FunctionType) else "N/A"
    )
    methods_str = str(route.methods)[2:-2] if route.methods is not None else "-"
    methods_str = methods_str.replace("', '", ", ")

    return TableEntry(
        pfad=route.path,
        http_methoden=methods_str,
        funktion=f"{endpoint.__module__}.{qualname}",
    )


def _routes_to_str(routes: list[BaseRoute]) -> str:
    routes_str: Final = [
        _route_to_table_entry(route) for route in routes if isinstance(route, Route)
    ]

    return tabulate(
        sorted(routes_str),
        headers=["Pfad", "HTTP-Methoden", "Implementierung"],
    )


def banner(routes: list[BaseRoute]) -> None:
    """Banner für den Start des Servers."""
    figlet: Final = Figlet()

    print()
    print(figlet.renderText("patient"))

    rechnername: Final = gethostname()

    logger.info("Python      {}", sys.version_info)
    logger.info("Plattform   {}", get_platform())
    logger.info("FastAPI     {}", fastapi.__version__)
    logger.info("uvicorn     {}", version("uvicorn"))
    logger.info("Starlette   {}", starlette.__version__)
    logger.info("AnyIO       {}", version("anyio"))
    logger.info("Pydantic    {}", pydantic.__version__)
    logger.info("MockDB      aktiv")
    logger.info("Environment {}", sys.prefix)
    logger.info("User        {}", getuser())
    logger.info("Locale      {}", getlocale())
    logger.info("Rechnername {}", rechnername)
    logger.info("IP          {}", gethostbyname(rechnername))
    logger.info("{} Routes:", len(routes))

    print()
    print(_routes_to_str(routes))
    print()
