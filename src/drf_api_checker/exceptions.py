# -*- coding: utf-8 -*-
import os


class ContractError(AssertionError):
    pass


class DictKeyMissed(ContractError):
    def __init__(self, keys):
        self.keys = keys

    def __str__(self) -> str:
        return f"Missing fields: `{self.keys}` "


class DictKeyAdded(ContractError):
    def __init__(self, keys):
        self.keys = keys


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
        return rf"""View '{self.view}' returned more field than expected.
Action needed: {os.path.basename(self.filename)} need rebuild.
New fields are: `{self.field_names}`"""


class FieldValueError(ContractError):
    def __init__(self, view, field_name, expected, received, filename,
                 message="Field `{0.field_name}` does not match."):
        self.view = view
        self.field_name = field_name
        self.expected = expected
        self.received = received
        self.filename = filename
        self.message = message.format(self)

    def __str__(self) -> str:
        return rf"""View `{self.view}` breaks the contract.        
Datadir: {self.filename}
{self.message}
- expected: `{self.expected}`
- received: `{self.received}`"""


class HeaderError(ContractError):
    def __init__(self, view, header, expected, received, filename, extra=""):
        self.view = view
        self.field_name = header
        self.expected = expected
        self.received = received
        self.filename = filename
        self.extra = extra

    def __str__(self) -> str:
        return rf"""View `{self.view}` breaks the contract.
Datadir: {self.filename}
Field `{self.field_name}` does not match.
- expected: `{self.expected}`
- received: `{self.received}`
{self.extra}
"""


class StatusCodeError(ContractError):
    def __init__(self, view, received, expected):
        self.view = view
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return f"View `{self.view}` breaks the contract. Expected status {self.expected}, received {self.received}"
