# -*- coding: utf-8

"""
    This file contains modified code adopted from Python's "platform" module
    to detect Linux distributions. This "platform" module functionality
    was deprecated with Python 3.6.

    Original code: https://github.com/python/cpython/blob/master/Lib/platform.py

    platform module copyright notice:

    Copyright (c) 1999-2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2010, eGenix.com Software GmbH; mailto:info@egenix.com

    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose and without fee or royalty is hereby granted,
    provided that the above copyright notice appear in all copies and that
    both that copyright notice and this permission notice appear in
    supporting documentation or portions thereof, including modifications,
    that you make.

    EGENIX.COM SOFTWARE GMBH DISCLAIMS ALL WARRANTIES WITH REGARD TO
    THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
    INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
    FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
    WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

"""

import os
import re


_UNIXCONFDIR = '/etc'

_distributor_id_file_re = re.compile("(?:DISTRIB_ID\s*=)\s*(.*)", re.I)
_release_file_re = re.compile("(?:DISTRIB_RELEASE\s*=)\s*(.*)", re.I)
_codename_file_re = re.compile("(?:DISTRIB_CODENAME\s*=)\s*(.*)", re.I)
_release_filename = re.compile(r'(\w+)[-_](release|version)', re.ASCII)
_lsb_release_version = re.compile(
    r'(.+)'
    ' release '
    '([\d.]+)'
    '[^(]*(?:\((.+)\))?',
    re.ASCII
)
_release_version = re.compile(
    r'([^0-9]+)'
    '(?: release )?'
    '([\d.]+)'
    '[^(]*(?:\((.+)\))?', re.ASCII
)

_supported_dists = (
    'SuSE', 'debian', 'fedora', 'redhat', 'centos',
    'mandrake', 'mandriva', 'rocks', 'slackware', 'yellowdog', 'gentoo',
    'UnitedLinux', 'turbolinux', 'arch', 'mageia', 'Ubuntu')


def _parse_release_file(firstline):
    # Default to empty 'version' and 'id' strings.  Both defaults are used
    # when 'firstline' is empty.  'id' defaults to empty when an id can not
    # be deduced.
    version = ''
    id = ''

    # Parse the first line
    m = _lsb_release_version.match(firstline)
    if m is not None:
        # LSB format: "distro release x.x (codename)"
        return tuple(m.groups())

    # Pre-LSB format: "distro x.x (codename)"
    m = _release_version.match(firstline)
    if m is not None:
        return tuple(m.groups())

    # Unknown format... take the first two words
    line = firstline.strip().split()
    if line:
        version = line[0]
        if len(line) > 1:
            id = line[1]
    return '', version, id


def linux_distribution(distname='', version='', id='',
                       supported_dists=_supported_dists,
                       full_distribution_name=1):
    """ Tries to determine the name of the Linux OS distribution name.

        The function first looks for a distribution release file in
        /etc and then reverts to _dist_try_harder() in case no
        suitable files are found.

        supported_dists may be given to define the set of Linux
        distributions to look for. It defaults to a list of currently
        supported Linux distributions identified by their release file
        name.

        If full_distribution_name is true (default), the full
        distribution read from the OS is returned. Otherwise the short
        name taken from supported_dists is used.

        Returns a tuple (distname, version, id) which default to the
        args given as parameters.

    """
    # check for the Debian/Ubuntu /etc/lsb-release file first, needed so
    # that the distribution doesn't get identified as Debian.
    try:
        with open("/etc/lsb-release", "r") as etclsbrel:
            for line in etclsbrel:
                m = _distributor_id_file_re.search(line)
                if m:
                    _u_distname = m.group(1).strip()
                m = _release_file_re.search(line)
                if m:
                    _u_version = m.group(1).strip()
                m = _codename_file_re.search(line)
                if m:
                    _u_id = m.group(1).strip()
            if _u_distname and _u_version:
                return (_u_distname, _u_version, _u_id)
    except (EnvironmentError, UnboundLocalError):
            pass

    try:
        etc = os.listdir(_UNIXCONFDIR)
    except OSError:
        # Probably not a Unix system
        return distname, version, id
    etc.sort()
    for file in etc:
        m = _release_filename.match(file)
        if m is not None:
            _distname, dummy = m.groups()
            if _distname in supported_dists:
                distname = _distname
                break
    else:
        return distname, version, id

    # Read the first line
    with open(os.path.join(_UNIXCONFDIR, file), 'r',
              encoding='utf-8', errors='surrogateescape') as f:
        firstline = f.readline()
    _distname, _version, _id = _parse_release_file(firstline)

    if _distname and full_distribution_name:
        distname = _distname
    if _version:
        version = _version
    if _id:
        id = _id
    return distname, version, id
