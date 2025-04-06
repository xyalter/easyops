#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:49
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from jinja2 import Template

from .. import path_join, TEMPLATES_PATH
from ..config.host import BootType
from ..util import read_text


class NetbootMixin:
    """
    A mixin class providing methods to generate GRUB configuration
    and preseed files for different boot types and systems.

    Methods:
        gen_grub: Generates a GRUB configuration based on the boot type.
        gen_preseed2: Generates a preseed configuration for a given system
                      and version code, tailored to the specified boot type.
    """

    @classmethod
    def gen_grub(cls, boot_type: BootType) -> str:
        """
        Generates a GRUB configuration for the specified boot type.

        Args:
            boot_type (BootType): The boot type, either EFI or BIOS.

        Returns:
            str: The rendered GRUB configuration as a string.
        """
        if boot_type == BootType.EFI:
            src_path = path_join(TEMPLATES_PATH, "boot", "grub.gpt.cfg.j2")
        else:
            src_path = path_join(TEMPLATES_PATH, "boot", "grub.msdos.cfg.j2")
        cfg_src = read_text(src_path)

        os_name = cls.__name__.lower()
        return Template(cfg_src).render(os=os_name)

    @staticmethod
    def gen_preseed2(sys, values, ver_code=None) -> str:
        """
        Generates a preseed configuration for a given system and version code,
        tailored to the specified boot type.

        Args:
            sys (str): System name, used to determine the template file name.
            values (dict): Dictionary containing values to be replaced in the
                template.
            ver_code (str): Version code to be used in the template file name.
                If not specified, the default template for the system is used.

        Returns:
            str: The rendered preseed configuration.
        """
        src_path = path_join(TEMPLATES_PATH, "boot")
        if ver_code is None:
            src_path = path_join(src_path, "preseed." + sys)
        else:
            src_path = path_join(src_path, "preseed." + sys + "-" + ver_code)
        if values["boot_type"] == BootType.EFI:
            src_path += ".gpt.cfg.j2"
        else:
            src_path += ".msdos.cfg.j2"
        cfg_src = read_text(src_path)
        cfg_dst = Template(cfg_src).render(values)
        return cfg_dst
