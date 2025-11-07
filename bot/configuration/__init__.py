"""Collect or build all requirements for startup bot."""

from bot.configuration.middleware import Middlewares
from bot.internal.services import Services
from bot.pkg.connectors import Connectors, PostgresSQL
from bot.pkg.models.core import Container, Containers
from bot.pkg.models.core.containers import Resource
from bot.internal.services.v1 import Services as V1Services


__all__ = ["__containers__"]

__containers__ = Containers(
    containers=[
        Container(container=Services),
        Resource(
            container=Connectors,
            depends_on=[
                Container(container=PostgresSQL),
            ],
        ),
        Container(container=Middlewares)
    ]
)

v1_container = V1Services()
v1_container.wire(
    modules=[
            "bot.internal.handlers.start",
            "bot.internal.handlers.test",
            "bot.internal.handlers.exam",
            "bot.internal.handlers.random_question",
        ]
)

