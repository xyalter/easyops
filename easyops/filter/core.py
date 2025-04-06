#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections.abc import Sequence

text_type = str
binary_type = bytes


def is_string(seq):
    """Identify whether the input has a string-like type (inclding bytes)."""
    # AnsibleVaultEncryptedUnicode inherits from Sequence, but is expected to be a string like object
    return isinstance(seq, (text_type, binary_type)) or getattr(seq, '__ENCRYPTED__', False)


def is_sequence(seq, include_strings=False):
    """Identify whether the input is a sequence.
    Strings and bytes are not sequences here,
    unless ``include_string`` is ``True``.
    Non-indexable things are never of a sequence type.
    """
    if not include_strings and is_string(seq):
        return False

    return isinstance(seq, Sequence)


def flatten(mylist, levels=None, skip_nulls=True):
    ret = []
    for element in mylist:
        if skip_nulls and element in (None, 'None', 'null'):
            # ignore null items
            continue
        elif is_sequence(element):
            if levels is None:
                ret.extend(flatten(element, skip_nulls=skip_nulls))
            elif levels >= 1:
                # decrement as we go down the stack
                ret.extend(flatten(element, levels=(int(levels) - 1), skip_nulls=skip_nulls))
            else:
                ret.append(element)
        else:
            ret.append(element)

    return ret
