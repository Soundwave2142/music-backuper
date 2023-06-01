from os import path
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
from tkinter import Entry, Label

from src.providers.language import translate as __
from src.providers.element import quick_element as qe


@dataclass
class ValidatorErrorBag:
    """
    A bag containing all error related variables.
    """
    error: str
    _error: str = field(init=False, repr=False)

    @property
    def error(self) -> str:
        """
        Getter for error property, implemented in order to have translated value.
        @return: translated error.
        """
        return __(self._error)

    @error.setter
    def error(self, value: str) -> None:
        """
        Setter for error property, implemented in order to later have translated value.
        @param value: key of the message.
        @return: None.
        """
        self._error = value


class AbstractValidatorRule(ABC):
    """
    Abstract class for any validation rule.
    """

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


class PathExistsRule(AbstractValidatorRule):
    error_message = 'validation.path_does_not_exists'

    def validate(self, value) -> None | ValidatorErrorBag:
        if not path.exists(value):
            return ValidatorErrorBag(self.error_message)


def validate(value: any, rules: List[AbstractValidatorRule], return_bag: bool = True) -> None | str | ValidatorErrorBag:
    """
    @param value: value that will be validated in rules.
    @param rules: array of AbstractValidatorRule objects that will validate the value.
    @param return_bag: boolean to return entire bag or only error message.
    @return: Error bag with related variable, translated string, nothing.
    """
    for rule in rules:
        error_bag = rule.validate(value)
        if error_bag is None:
            continue

        if return_bag is True:
            return error_bag

        return error_bag.error


def validate_input(entry_input: Entry, error_label: Label, rules: List[AbstractValidatorRule]) -> bool:
    result = validate(entry_input.get(), rules)

    # if there is no validation problems, hide the label and return positive result
    if result is None:
        qe.hide(error_label)
        return True

    # otherwise show the label, and change the text.
    error_label.config(text=result.error)
    qe.show(error_label, {})

    return False
