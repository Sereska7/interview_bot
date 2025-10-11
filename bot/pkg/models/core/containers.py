from dataclasses import dataclass, field
from typing import Type, List, Union, Callable
from dependency_injector import providers
from dependency_injector.containers import Container as _DIContainer
from aiogram import Dispatcher, BaseMiddleware
from aiogram.types import Message, TelegramObject
from bot.pkg.models.core.meta import SingletonMeta

@dataclass(frozen=True)
class Resource:
    container: Type[_DIContainer]
    depends_on: List[_DIContainer] = field(default_factory=list)
    packages: List[str] = field(default_factory=lambda: ["bot.pkg.models"])

@dataclass(frozen=True)
class Container:
    container: Union[Callable[..., _DIContainer]]
    packages: List[str] = field(default_factory=lambda: ["bot.pkg.models"])

class WiredContainer(dict, metaclass=SingletonMeta):
    """Singleton для хранения провайренных контейнеров."""
    def __getitem__(self, item: object) -> _DIContainer:
        return super().__getitem__(item.__name__)

@dataclass(frozen=True)
class Containers:
    containers: List[Union[Container, Resource]]
    __wired_containers__: WiredContainer = field(default_factory=WiredContainer, init=False)

    def wire(self) -> None:
        """Провайрим все контейнеры и их зависимости."""
        for container in self.containers:
            self.__wire(container)
            if isinstance(container, Resource):
                for dep in container.depends_on:
                    self.__wire(dep)

    def __wire(self, container: Union[Container, Resource]) -> _DIContainer:
        cont = container.container()
        cont.wire(packages=container.packages)
        name = container.container.__name__
        if name not in self.__wired_containers__:
            self.__wired_containers__[name] = cont
        return cont

    def attach_to_dispatcher(self, dp: Dispatcher):
        """Подключаем один middleware для всех контейнеров."""
        dp.update.middleware.register(ContainerMiddleware(self))


class ContainerMiddleware(BaseMiddleware):
    def __init__(self, containers: Containers):
        super().__init__()
        self.containers = containers

    async def __call__(self, handler, event: TelegramObject, data: dict, **kwargs):
        # кладём контейнеры в data
        data["containers"] = self.containers.__wired_containers__
        # прокидываем все аргументы через kwargs
        kwargs["data"] = data
        return await handler(event, **kwargs)
