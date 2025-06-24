#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 16:37:07 2025

@author: shayneufeld
"""

from typing import List, AsyncGenerator
from langchain_core.callbacks.base import AsyncCallbackHandler
import asyncio

class StreamingHandler(AsyncCallbackHandler):
    def __init__(self):
        self.tokens: List[str] = []
        self.done = False

    async def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)

    async def stream(self) -> AsyncGenerator[str, None]:
        current = 0
        while not self.done or current < len(self.tokens):
            while current < len(self.tokens):
                yield self.tokens[current]
                current += 1
            await asyncio.sleep(0.05)  # adjust as needed

    async def on_llm_end(self, *args, **kwargs):
        self.done = True
