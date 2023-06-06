from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
from os import path
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
    def validate(self, value: any) -> None | ValidatorErrorBag:
        """
        Contains code to validate value.
        @param value: to validate.
        @return: Nothing or error bag.
        """
        pass


class NotEmptyRule(AbstractValidatorRule):
    """
    Validation rule for checking if value is empty.
    """
    error_message = 'validation.field_empty'

    def validate(self, value: any) -> None | ValidatorErrorBag:
        """
        Very simple check to see if value is empty.
        @param value: to validate.
        @return: Nothing or error bag.
        """
        if isinstance(value, str):
            value.strip()

        if not value:
            return ValidatorErrorBag(self.error_message)


class PathExistsRule(AbstractValidatorRule):
    """
    Validation rule to see if value is path (that exists) in the system.
    """
    error_message = 'validation.path_does_not_exists'

    def validate(self, value) -> None | ValidatorErrorBag:
        """
        Simple check if value is path (that exists) in the system.
        @param value: path to validate
        @return: Nothing or error bag.
        """
        if not path.exists(value):
            return ValidatorErrorBag(self.error_message)


def validate(value: any, rules: List[AbstractValidatorRule], return_bag: bool = True) -> None | str | ValidatorErrorBag:
    """
    Validates value against given set of rules.
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
    """
    Validates input against given set of rules and sets (or clears) an error to (or from) a label.
    @param entry_input: input to validate.
    @param error_label: set error text to in case there is an error.
    @param rules: array of AbstractValidatorRule objects that will validate the value.
    @return: True or False depending on if there is any errors or not.
    """
    result = validate(entry_input.get(), rules)

    # if there is no validation problems, hide the label and return positive result
    if result is None:
        qe.hide(error_label)
        return True

    # otherwise show the label, and change the text.
    error_label.config(text=result.error)
    qe.show(error_label, {})

    return False
