#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from .netboot import NetbootMixin
from .deblike import DebianCore
from .apt import AptMixin


class Debian(DebianCore, AptMixin, NetbootMixin):
    """
    A class representing the Debian operating system, providing methods
    for generating preseed and APT source configurations.

    This class inherits from:
        - DebianCore: Core functionalities for Debian-based systems.
        - AptMixin: A mixin for handling APT source list generation.
        - NetbootMixin: A mixin for generating GRUB and preseed configurations.

    Attributes:
        VERSIONS (dict): A dictionary of available version codes and their
            corresponding version names.
        MIRRORS (dict): A dictionary of available mirror URLs by name.
        repo_types (list): A list of repository types.

    Methods:
        gen_preseed_conf: Generates a preseed configuration for Debian.
        gen_apt_src: Generates an APT source list for Debian.
    """

    @staticmethod
    def gen_preseed_conf(values, ver_code=None):
        """Generates Debian preseed configuration file.
        
        Args:
            values (dict): Installation configuration parameters
            ver_code (str, optional): Debian version codename (e.g. 'bookworm')
        
        Returns:
            str: Path to generated preseed configuration file
        """
        cfg_dst = Debian.gen_preseed2("debian", values, ver_code)
        return cfg_dst

    @staticmethod
    def gen_apt_src(
        mirror=None,
        dir_main="debian",
        dir_sec="debian-security",
        version=None,
        contrib=True,
        non_free=True,
        backports=False,
        src=True,
        write=False,
        dst_path=None,
    ):
        """Generates apt source configuration for Debian repositories.
        
        Args:
            mirror (str): Mirror URL (default: auto-select)
            dir_main (str): Main repository directory (default: 'debian')
            dir_sec (str): Security updates directory (default: 'debian-security')
            version (str): Debian version codename (e.g. 'bookworm')
            contrib (bool): Include contrib repository (default: True)
            non_free (bool): Include non-free repository (default: True)
            backports (bool): Include backports repository (default: False)
            src (bool): Include source repositories (default: True)
            write (bool): Write to filesystem (default: False)
            dst_path (str): Custom output path
        
        Returns:
            str: Generated sources.list content
        """
        if mirror is None:
            mirror = Debian.MIRRORS["auto"]
        elif "." not in mirror:
            mirror = Debian.MIRRORS[mirror]
        if version is None:
            version = 12
        repo_type = Debian.REPO_TYPES
        if not contrib:
            repo_type.remove("contrib")
        if not non_free:
            repo_type.remove("non-free")
        values = dict(
            mirror=mirror,
            dir_main=dir_main,
            dir_sec=dir_sec,
            version=Debian.VERSIONS[version],
            repotype=" ".join(repo_type),
        )
        return Debian.gen_src_list(values, backports, src, write, dst_path)


Debian.VERSIONS = {
    12: "bookworm",
    11: "bullseye",
}

Debian.MIRRORS.update(
    {
        "cn": "ftp.cn.debian.org",
        "hk": "ftp.hk.debian.org",
        "sg": "ftp.sg.debian.org",
        "kr": "ftp.kr.debian.org",
        "jp": "ftp.jp.debian.org",
        "tw": "ftp.tw.debian.org",
        "us": "ftp.us.debian.org",
        "sec": "security.debian.org",
        "arc": "archive.debian.org",
        "auto": "deb.debian.org",
    }
)

Debian.REPO_TYPES = ["main", "contrib", "non-free"]
