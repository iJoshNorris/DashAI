from abc import abstractmethod
from typing import Any

from DashAI.back.models.base_model import BaseModel


class GenerativeModel(BaseModel):
    @abstractmethod
    def process_output(self) -> Any:
        """Restores an instance of a model.

        filename (Str): Indicates where the model was stored.
        """
        raise NotImplementedError
