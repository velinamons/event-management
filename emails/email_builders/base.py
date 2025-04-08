from typing import Any
from abc import ABC, abstractmethod


class BaseEmailBuilder(ABC):
    def __init__(self, registration: Any):
        self.registration = registration

    @abstractmethod
    def get_subject(self) -> str:
        pass

    @abstractmethod
    def get_html_content(self) -> str:
        pass

    @abstractmethod
    def get_text_content(self) -> str:
        pass
