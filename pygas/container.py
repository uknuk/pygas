from dependency_injector import providers, containers
from .player import Player
from .artists import Artists
from .tracks import Tracks
from .albums import Albums


class Components(containers.DeclarativeContainer):
    tracks = providers.Singleton(Tracks)
    albums = providers.Singleton(Albums)
    player = providers.Singleton(Player, tracks)
    artists = providers.Singleton(Artists, albums, tracks)
