#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:35
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

import unittest

from easyops import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(path='tests/invoke.yml')
        self.invoke = self.config.context

    def test_host(self) -> None:
        config = self.config
        for key in config.hosts:
            host = config.hosts[key]
            # print(host)
