# -*- coding: utf-8 -*-
import os


class ContractError(AssertionError):
    pass


class FieldMissedError(ContractError):
    def __init__(self, view, field_name):
        self.view = view
        self.field_name = field_name

    def __str__(self) -> str:
        return f"View `{self.view}` breaks the contract. Missing fields: `{self.field_name}` "


class FieldAddedError(ContractError):
    def __init__(self, view, field_names, filename):
        self.view = view
        self.field_names = field_names
        self.filename = filename

    def __str__(self) -> str:
        return rf"""View `{self.view}` returned more field than expected.
Action needed: {os.path.basename(self.filename)} need rebuild.
New fields are: `{self.field_names}`"""


class FieldValueError(ContractError):
    def __init__(self, view, field_name, expected, receiced, filename):
        self.view = view
        self.field_name = field_name
        self.expected = expected
        self.receiced = receiced
        self.filename = filename

    def __str__(self) -> str:
        return rf"""View `{self.view}` breaks the contract.
Datadir: {self.filename}
Field `{self.field_name}` does not match.
- expected: `{self.expected}`
- received: `{self.receiced}`"""
