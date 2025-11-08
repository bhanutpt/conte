"""Configuration helpers for Conte."""

from __future__ import annotations

from copy import deepcopy

from .defaults import DEFAULT_CONFIG


def get_default_config() -> dict:
    """Return a deep copy of the built-in default config."""
    return deepcopy(DEFAULT_CONFIG)


__all__ = ["get_default_config", "DEFAULT_CONFIG"]
