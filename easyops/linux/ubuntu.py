#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from .deblike import DebianCore
from .apt import AptMixin
from .netboot import NetbootMixin


class Ubuntu(DebianCore, AptMixin, NetbootMixin):
    """
    A class representing the Ubuntu operating system, providing methods
    for generating preseed and APT source configurations.

    Inherits from:
        - DebianCore: Core functionalities for Debian-based systems.
        - AptMixin: A mixin for handling APT source list generation.
        - NetbootMixin: A mixin for generating GRUB and preseed configurations.

    Methods:
        gen_preseed_conf: Generates a preseed configuration for Ubuntu.
        gen_apt_src: Generates an APT source list for Ubuntu.
    """

    @staticmethod
    def gen_preseed_conf(values, ver_code=None):
        """Generates Ubuntu preseed configuration file.

        Args:
            values (dict): Configuration values for package installation
            ver_code (str, optional): Ubuntu version codename (e.g. 'focal')

        Returns:
            str: Path to generated preseed configuration file
        """
        cfg_dst = Ubuntu.gen_preseed2("ubuntu", values, ver_code)
        return cfg_dst

    @staticmethod
    def gen_apt_src(
        mirror=None,
        dir_main="ubuntu",
        dir_sec="ubuntu-security",
        version=None,
        universe=True,
        restricted=True,
        backports=False,
        src=True,
        write=False,
        dst_path=None,
    ):
        """Generates apt source list configuration for Ubuntu repositories.

        Args:
            mirror (str): Base mirror URL
            dir_main (str): Main repository directory
            dir_sec (str): Security updates directory
            version (int): Ubuntu version number (e.g. 22)
            universe (bool): Include universe repository
            restricted (bool): Include restricted repository
            backports (bool): Include backports repository
            src (bool): Include source repository
            write (bool): Write configuration to file
            dst_path (str): Destination path for written configuration

        Returns:
            str: Generated apt source list contents
        """
        if mirror is None:
            mirror = Ubuntu.MIRRORS["auto"]
        elif "." not in mirror:
            mirror = Ubuntu.MIRRORS[mirror]
        if version is None:
            version = 20
        repo_type = Ubuntu.REPO_TYPES
        if not universe:
            repo_type.remove("universe")
        if not restricted:
            repo_type.remove("restricted")
        values = dict(
            mirror=mirror,
            dir_main=dir_main,
            dir_sec=dir_sec,
            version=Ubuntu.VERSIONS[version],
            repotype=" ".join(repo_type),
        )
        return Ubuntu.gen_src_list(values, backports, src, write, dst_path)


Ubuntu.VERSIONS = {
    20: "focal",
    18: "bionic",
}

Ubuntu.MIRRORS.update(
    {
        "cn": "cn.archive.ubuntu.com",
        "hk": "hk.archive.ubuntu.com",
        "sg": "sg.archive.ubuntu.com",
        "kr": "kr.archive.ubuntu.com",
        "jp": "jp.archive.ubuntu.com",
        "tw": "tw.archive.ubuntu.com",
        "us": "us.archive.ubuntu.com",
        "sec": "security.ubuntu.com",
        "auto": "archive.ubuntu.com",
    }
)

Ubuntu.REPO_TYPES = ["main", "universe", "restricted", "multiverse"]
