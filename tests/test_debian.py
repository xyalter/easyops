#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:35
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

import unittest

from easyops.linux import Debian


class TestDebian(unittest.TestCase):
    def setUp(self) -> None:
        # with open('./sources.json', 'r') as f:
        #     self.src_list = json.load(f)
        pass

    def test_gen_grub(self) -> None:
        config = Debian.gen_grub()
        with open('tests/debian/grub-msdos.cfg', 'r') as f:
            example = f.read()
        self.assertEqual(example, config)
