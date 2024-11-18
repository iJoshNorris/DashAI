from abc import abstractmethod
from typing import Any, Dict, Final, Optional


class GenerativeTask:
    """Base task for generative processes."""

    TYPE: Final[str] = "Task"

    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def prepare_for_task(
        self,
        input: Any,
    ) -> Any:
        """Prepare input data for the task.

        Parameters
        ----------
        input : Any
            Input data to be prepared

        Returns
        -------
        Any
            Prepared input data
        """
        raise NotImplementedError

    @abstractmethod
    def process_output(
        self,
        output: Any,
        path: Optional[str] = None,
    ) -> Any:
        """Process output data of the task.

        Parameters
        ----------
        output : Any
            Output data to be processed

        Returns
        -------
        Any
            Processed output data
        """
        raise NotImplementedError
