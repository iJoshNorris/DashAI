from abc import abstractmethod
from typing import Any

from DashAI.back.models.base_model import BaseModel


class GenerativeModel(BaseModel):
    @abstractmethod
    def process_output(self, out: Any, file_name: str, path: str) -> str:
        """Process the output of a generative model.

        file_name (Str): Indicates the name of the file.
        path (Str): Indicates the path where the output will be stored.
        """
        raise NotImplementedError
