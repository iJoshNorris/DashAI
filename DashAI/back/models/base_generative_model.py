from abc import ABCMeta, abstractmethod
from typing import Any, Final

from DashAI.back.config_object import ConfigObject


class BaseGenerativeModel(ConfigObject, metaclass=ABCMeta):

    TYPE: Final[str] = "Model"

    @abstractmethod
    def generate(self, input: Any) -> Any:
        """Generate output from a generative model.

        input (Any): Input to the generative model.
        """
        raise NotImplementedError

    @abstractmethod
    def process_output(self, out: Any, file_name: str, path: str) -> str:
        """Process the output of a generative model.

        file_name (Str): Indicates the name of the file.
        path (Str): Indicates the path where the output will be stored.
        """
        raise NotImplementedError
