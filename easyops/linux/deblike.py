#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from jinja2 import Template


from .. import path_join, path_sep, CONF_PRESEED_PATH, BUILD_TMP_PATH
from ..util import write_text, read_text


class DebianCore:
    """Base class for Debian-like distribution configuration management.
    
    Attributes:
        VERSIONS (dict): Mapping of version codenames to release numbers
    """
    VERSIONS = {}

    @staticmethod
    def gen_preseed(sys, values, write=False, dst_path=None):
        """Generates preseed configuration for Debian-based systems.
        
        Args:
            sys (str): System identifier (e.g. 'debian', 'ubuntu')
            values (dict): Template variables for preseed configuration
            write (bool): Persist configuration to disk (default: False)
            dst_path (str): Custom output path (default: system-specific)
        
        Returns:
            str: Rendered preseed configuration content
        """
        src_path = path_join(CONF_PRESEED_PATH, "preseed-" + sys + ".cfg.j2")
        cfg_src = read_text(src_path)
        cfg_dst = Template(cfg_src).render(values)
        if write:
            base_path = path_join(BUILD_TMP_PATH, "boot", "preseed-")
            if dst_path is None:
                dst_path = path_join(base_path + sys + ".cfg")
            elif path_sep not in dst_path:
                dst_path = path_join(base_path + dst_path + ".cfg")
            write_text(cfg_dst, dst_path)
        return cfg_dst
