from abc import ABC, abstractmethod

from murren.models import Murren


class Permission(ABC):
    @abstractmethod
    def is_banned(self, user: Murren) -> bool:
        raise NotImplementedError()


class MurrenPermission(Permission):

    def is_banned(self, user: Murren) -> bool:
        return user.is_banned
