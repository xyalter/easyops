#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2024-09-16 15:00
@Author  : xxy
@Email   : xxy@lesscode.dev

This script provides functionality to build OpenWRT images using a custom configuration.
It utilizes the OpenwrtImageBuilder to create and manage the build process.
"""


import argparse
import logging

from easyops.netboot import Netboot

from . import __version__


def get_parser():
    """
    Creates and returns an argument parser for the Linux netboot installer.

    Returns:
        argparse.ArgumentParser: Configured argument parser object.
    """
    parser = argparse.ArgumentParser(description="Linux netboot installer.")
    parser.add_argument(
        "--os", choices=["debian", "ubuntu"], help="the distribution's name"
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
        help="the distribution's major version",
    )
    parser.add_argument("-T", "--target", help="target name")
    parser.add_argument("-H", help="hostname")
    parser.add_argument("-M", "--manual", action="store_true", help="manual mode")
    parser.add_argument("--only-generate", action="store_true", help="only generate")

    return parser


def entry_func():
    """
    Main entry point of the script.

    This function parses command-line arguments, loads the configuration,
    and initiates the build process.
    """
    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    if not args.target and not args.os:
        raise RuntimeError("Target or OS is required!")
    netboot = Netboot(args.os, args.target)

    if not args.only_generate:
        logging.info("Start download netboot files...")
        netboot.download()
        logging.info("Netboot files had downloaded.")

        logging.info("Start download netboot files...")
        netboot.update_grub()
        logging.info("Grub config had updated.")

        if not args.manual:
            netboot.gen_preseed(args.H)
            netboot.attach_data()

    else:
        netboot.generate_preseed(args.H)
