from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the provider scanner."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the CLI tool is installed in the system PATH."""
        pass

    @abstractmethod
    def scan(self, target_url: str) -> List[Dict[str, Any]]:
        """Executes the scanner and returns a list of raw signals to be created."""
        pass
