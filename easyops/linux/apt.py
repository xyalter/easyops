#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from string import Template

from .. import path_join, path_sep, CONF_APT_PATH, BUILD_TMP_PATH
from ..util import write_text, read_text


class AptMixin:
    """
    A mixin class for handling APT source list generation.

    This class provides a static method to generate APT source lists by substituting values
    into a template, with options to include or exclude backports and source packages.
    It also supports writing the generated source list to a specified destination path.

    Attributes:
        MIRRORS (dict): A dictionary of available mirror URLs by name.
        repo_types (list): A list of repository types.
    """
    MIRRORS = {
        "163": "mirrors.163.com",
        "aly": "mirrors.aliyun.com",
        "aly-vpc": "mirrors.cloud.aliyuncs.com",
        "xtom": "mirror.xtom.com.hk",
        "sggs": "mirror.sg.gs",
        # kr
        "harukasan": "ftp.harukasan.org",
        # us
        "steadfast": "mirror.steadfast.net",
    }
    repo_types = []

    @staticmethod
    def gen_src_list(values, backports, src, write=False, dst_path=None):
        """
        Generate APT source list by substituting values into a template.

        Args:
            values (dict): A dictionary of values to be substituted into the template.
            backports (bool): Whether to include backports in the generated source list.
            src (bool): Whether to include source packages in the generated source list.
            write (bool): Whether to write the generated source list to a file.
            dst_path (str): The destination path to write the generated source list to.
                If not specified, the default path is under
                ``<BUILD_TMP_PATH>/apt/sources.list.<dir_main>``.

        Returns:
            str: The generated source list.
        """
        src_path = path_join(CONF_APT_PATH, "sources.list")
        cfg_src = read_text(src_path)
        cfg_dst = Template(cfg_src).safe_substitute(values)
        lines = cfg_dst.splitlines()
        dst = list(lines)
        for line in lines:
            if not backports and line.find("backports") != -1:
                dst.remove(line)
            if not src and line.find("deb-src") != -1:
                dst.remove(line)
        cfg_dst = "\n".join(dst) + "\n"
        if write:
            base_path = path_join(BUILD_TMP_PATH, "apt", "sources.list.")
            if dst_path is None:
                dst_path = path_join(base_path + values["dir_main"])
            elif path_sep not in dst_path:
                dst_path = path_join(base_path + dst_path)
            write_text(cfg_dst, dst_path)
        return cfg_dst
