"""Backward-compatible conversion API.

The original notebook combined parsing and folder conversion. The actual parsing
implementation lives in `parser.py`; this module exposes the conversion functions
under their own concern for a cleaner project structure.
"""
from .parser import convert_folder, file_to_record

__all__ = ["convert_folder", "file_to_record"]
