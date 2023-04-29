# -*- coding: utf-8 -*-
import abc
import hashlib
import json
from typing import Dict, List, Union, Type


class AbstractNginxObject:
    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Union[str, int, List[str]]]:
        """
        This method should return a dictionary which mirrors the crossplane JSON
        structure.
        """
        pass

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def hash(self) -> str:
        return hashlib.md5(
            self.to_json().encode("utf-8")
        ).hexdigest()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.hash() == other.hash()
        else:
            return False
