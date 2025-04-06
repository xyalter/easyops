#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-02 00:02
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

import json
import unittest

from easyops import Config
from easyops.linux.apt2 import SourceConfigSet
from easyops.netboot import get_args, Netboot


class TestNetBoot(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(path='tests/invoke.yml')
        self.invoke = self.config.context

        with open('./sources.json', 'r') as f:
            self.mirror_set = SourceConfigSet(json.load(f))

    def test_args(self) -> None:
        args = get_args(['debian', '-H', 'vm-tmp-dstd'])
        self.assertEqual('debian', args.os)
        self.assertEqual('vm-tmp-dstd', args.H)
        self.assertFalse(args.manual)
        netboot = Netboot(args.os, args.H)
        # with patch.object(netboot, 'config', self.config), \
        #      patch.object(netboot, 'src_list', self.src_list):
        netboot.config = self.config
        netboot.mirror_set = self.mirror_set
        host = netboot.get_config()
        mirror = netboot.mirror
        # netboot.download()

    def test_preseed(self) -> None:
        args = get_args(['ubuntu', '-H', 'test2'])
        netboot = Netboot(args.os, args.H)
        netboot.config = self.config
        netboot.src_list = self.mirror_set

        config = netboot.get_preseed_cfg()
        with open('tests/ubuntu/preseed-test2.cfg', 'r') as f:
            example = f.read()
        self.assertEqual(example, config)
