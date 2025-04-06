#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-26 21:52
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

import json
import logging
from os import path
from typing import List

import requests
from invoke import Context, run

from easyops import SCRIPTS_PATH, Config, Host
from easyops.linux import Debian, Ubuntu
from easyops.linux.apt2 import SourceConfigItem, SourceConfigSet
from easyops.util import write_text

CFG_URI = "https://files.lesscode.dev/easyops"


class Netboot:
    """
    A class representing the netboot installer for Linux.

    This class provides methods to download the specified version of the
    operating system from the specified mirror, update the GRUB
    configuration, generate a preseed configuration, and attach data files
    to the netboot image.

    Attributes:
        os (str): The operating system identifier.
        mirror (str): The mirror URI.
        host (Host): The host configuration.
        mirror_set (SourceConfigSet): The set of mirror configurations.
        script_path (str): The path to the netboot script.
    """

    def __init__(self, os: str, host: str):
        """
        Initializes a new Netboot instance.

        Args:
            os (str): The operating system identifier.
            host (str): The host configuration identifier.
        """
        self.os = os
        self.__host = host
        self.script_path = path.join(SCRIPTS_PATH, "netboot.sh")

        self.__config = Config(path="invoke.yml")
        if self.os is None:
            if self.get_config().os is not None:
                self.os = self.get_config().os
            else:
                raise RuntimeError("OS must be specified!")

        json_text = requests.get(f"{CFG_URI}/sources.json", timeout=10).text
        self.__mirror_set = SourceConfigSet(json.loads(json_text))

    @property
    def config(self) -> Config:
        """Get the configuration."""
        return self.__config

    @config.setter
    def config(self, value: Config) -> None:
        """Set the configuration."""
        self.__config = value

    @property
    def mirror_set(self) -> SourceConfigSet:
        """Get the set of mirror configurations."""
        return self.__mirror_set

    @mirror_set.setter
    def mirror_set(self, value: SourceConfigSet) -> None:
        """Sets the set of mirror configurations."""
        self.__mirror_set = value

    @property
    def host(self) -> Host:
        """Get the host configuration."""
        return self.get_config()

    @property
    def executor(self) -> Context:
        """Get the executor."""
        return self.config.context

    @property
    def mirror(self) -> SourceConfigItem:
        """
        Get the mirror configuration for the current host.

        If the host's mirror configuration contains a '.', it is assumed to be
        a complete mirror URI and is returned as is. Otherwise, the host's
        mirror name is used to search for a matching mirror configuration in
        the global set of mirrors.

        The search criteria are as follows:

        1. Operating system: The host's operating system identifier.
        2. Name: The host's mirror name.
        3. Scheme: The mirror's URI scheme must be 'http' or 'https'.

        The search order is:

        1. Search for a mirror with the given name and operating system
           identifier.
        2. If not found, search for a mirror with the given name and the
           global set of mirrors.
        3. If not found, return None.

        Returns:
            SourceConfigItem or None: The mirror configuration, or None if
                not found.
        """
        host = self.host
        if "." in host.mirror:
            return SourceConfigItem(self.os, dict(host=host.mirror))
        else:

            def scheme(schemes: List[str]):
                return "mirror" not in schemes

            return self.mirror_set.get_mirror(
                os=self.os, name=host.mirror, scheme=scheme
            )

    @property
    def mirror_uri(self) -> str:
        """Get the mirror URI."""
        return f"{self.mirror.scheme[0]}://{self.mirror.host}"

    def get_config(self) -> Host:
        """
        Get the host configuration.

        If the host is not found, returns None.
        """
        if self.__host is not None and self.__host in self.config.hosts:
            return self.config.hosts[self.__host]
        elif self.os in self.config.hosts:
            return self.config.hosts[self.os]

    def download(self, ver_code=None):
        """
        Downloads the operating system from the specified mirror.

        Downloads the specified version of the operating system from the
        specified mirror.

        Args:
            ver_code (str, optional): The version code of the operating system
                to download (e.g. "bookworm" for Debian or "noble" for Ubuntu).
                Defaults to None.

        Raises:
            subprocess.CalledProcessError: If the command to download the
                operating system fails.
        """
        if ver_code is None:
            if self.os == "debian":
                ver_code = Debian.VERSIONS[12]
            elif self.os == "ubuntu":
                ver_code = Ubuntu.VERSIONS[20]
        run(
            " ".join(
                [
                    "bash",
                    self.script_path,
                    "netboot_download",
                    self.mirror_uri,
                    self.os,
                    ver_code,
                ]
            )
        )

    def update_grub(self):
        """
        Updates the GRUB configuration for the current operating system.

        This method generates a GRUB configuration based on the operating system
        type (either Debian or Ubuntu) and writes it to a file. It then executes
        a shell script to apply the GRUB configuration.

        Raises:
            Exception: If the operating system type is not supported.
        """
        grub_cfg = None
        if self.os == "debian":
            grub_cfg = Debian.gen_grub(self.host.boot_type)
        elif self.os == "ubuntu":
            grub_cfg = Ubuntu.gen_grub(self.host.boot_type)
        if grub_cfg is not None:
            file_path = path.abspath("grub-msdos.cfg")
            write_text(grub_cfg, file_path)
            run(" ".join(["bash", self.script_path, "netboot_grub", file_path]))

    def get_preseed_cfg(self, hostname: str):
        """
        Generates a preseed configuration for the given hostname.

        This method retrieves the host configuration, constructs a set of
        values required for generating the preseed configuration, and
        invokes the appropriate method based on the operating system
        (Debian or Ubuntu) to generate the configuration.

        Args:
            hostname (str): The hostname to be used in the preseed configuration.

        Returns:
            str: The generated preseed configuration content.
        """
        host = self.get_config()
        proxy = host.proxy
        if proxy is None:
            proxy = ""
        values = {
            "boot_type": host.boot_type,
            "fqdn": host.fqdn,
            "host": host.host,
            "domain": host.domain,
            "root_password": host.users["root"]["password"],
            "root_key": host.users["root"]["key"],
            "username": host.username,
            "fullname": host.fullname,
            "user_password": host.users[host.username]["password"],
            "user_key": host.users[host.username]["key"],
            "proxy": proxy,
            "mirror": self.mirror.host,
            "features": host.features,
            "packages": host.packages,
        }
        if "network" in host.data:
            values["network_ipv4"] = host.network["ipv4"]
            values["network_gateway"] = host.network["gateway"]
            values["network_dns"] = host.network["dns"]
        if "post_scripts" in host.data:
            values["post_scripts"] = host.post_scripts
        if hostname:
            values["fqdn"] = ".".join([hostname, host.domain])
        preseed_cfg = None
        if self.os == "debian":
            preseed_cfg = Debian.gen_preseed_conf(values)
        elif self.os == "ubuntu":
            preseed_cfg = Ubuntu.gen_preseed_conf(values)
        return preseed_cfg

    def generate_preseed(self, hostname: str = None):
        """
        Generates a preseed configuration for the given hostname and writes it
        to a file.

        Args:
            hostname (str, optional): The hostname to be used in the preseed
                configuration. Defaults to None.

        Returns:
            None
        """
        preseed_cfg = self.get_preseed_cfg(hostname)
        if preseed_cfg is not None:
            file_path = path.abspath("pressed.cfg")
            write_text(preseed_cfg, file_path)

    def gen_preseed(self, hostname: str = None):
        """
        Generates a preseed configuration for the given hostname and applies it
        to the netboot image.

        Args:
            hostname (str, optional): The hostname to be used in the preseed
                configuration. Defaults to None.

        Returns:
            None
        """
        preseed_cfg = self.get_preseed_cfg(hostname)
        if preseed_cfg is not None:
            file_path = path.abspath("pressed.cfg")
            write_text(preseed_cfg, file_path)
            run(
                " ".join(
                    ["bash", self.script_path, "netboot_preseed", self.os, file_path]
                )
            )

    def attach_data(self):
        """
        Attaches data files to the netboot image.

        This method iterates over the files specified in the host configuration
        and attempts to attach each file to the netboot image by executing a
        shell script. If a file's source path does not exist, a warning is logged.

        Returns:
            None
        """
        if self.host.files is None:
            return
        files = self.host.files
        for file in files:
            if path.exists(file["src"]):
                run(
                    " ".join(
                        [
                            "bash",
                            self.script_path,
                            "netboot_attach",
                            self.os,
                            path.relpath(file["src"]),
                            file["dest"],
                            path.abspath(path.curdir),
                        ]
                    )
                )
            else:
                logging.warning("File: %s is not found!", path.abspath(file["src"]))
