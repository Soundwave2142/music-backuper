from os import path
from abc import ABC, abstractmethod
from typing import List
from tkinter import Entry, Label

from src.providers.language import LanguageProvider


class ValidatorErrorBag:
    def __init__(self, error: str):
        self.error = error


class AbstractValidatorRule(ABC):
    @abstractmethod
    def validate(self, value) -> None | ValidatorErrorBag:
        pass


class NotEmptyRule(AbstractValidatorRule):
    error_message = 'validation.field_empty'

    def validate(self, value) -> None | ValidatorErrorBag:
        if isinstance(value, str):
            value.strip()

        if not value:
            return ValidatorErrorBag(self.error_message)


class PathDoNotExistsRule(AbstractValidatorRule):
    error_message = 'validation.path_does_not_exists'

    def validate(self, value) -> None | ValidatorErrorBag:
        if not path.exists(value):
            return ValidatorErrorBag(self.error_message)


class ValidatorComponent:
    def __init__(self, language_provider: LanguageProvider):
        self.__ = language_provider

    def validate_input(self, entry_input: Entry, error_label: Label, rules: List[AbstractValidatorRule]) -> bool:
        result = self.validate(entry_input.get(), rules)

        # set error message or make label empty in any case
        error_message = ''
        if result is not None:
            error_message = self.__.t(result.error)

        error_label.config(text=error_message, fg="red")  # TODO: set color from theme

        # let the father parent know if validate failed
        return result is None

    def validate(self, value, rules: List[AbstractValidatorRule],
                 return_bag: bool = True) -> None | str | ValidatorErrorBag:
        for rule in rules:
            error_bag = rule.validate(value)
            if error_bag is None:
                continue

            if return_bag is True:
                return error_bag

            return self.__.t(error_bag.error)
