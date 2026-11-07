"""Shared exceptions for Prove's public interfaces."""

from __future__ import annotations


class ProveError(Exception):
    """An expected validation failure from a Prove primitive."""

    def __init__(self, message: str, code: int = 2) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
