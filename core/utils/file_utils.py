#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 12:36:45 2025

@author: shayneufeld
"""

# core/utils/file_utils.py

"""
Utility functions for extracting text or data from supported file types:
- .txt: Plain text
- .pdf: Portable Document Format (using PyMuPDF)
- .csv: Comma-separated values
- .json: JavaScript Object Notation

Used by the agent to analyze user-uploaded documents.
"""

import os
import json
import csv

import fitz  # PyMuPDF
from typing import Optional


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_csv(file_path: str) -> str:
    output = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(", ".join(row))
    return "\n".join(output)


def extract_text_from_json(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)


def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Generic file reader that auto-selects the appropriate method
    based on file extension.

    Args:
        file_path (str): Path to the file to extract from.

    Returns:
        str or None: Extracted text content or None if unsupported type.
    """
    _, ext = os.path.splitext(file_path.lower())
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".csv":
        return extract_text_from_csv(file_path)
    elif ext == ".json":
        return extract_text_from_json(file_path)
    else:
        return None
