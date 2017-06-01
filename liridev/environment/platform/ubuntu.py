# -*- coding: utf-8 -*-

import typing
import click

from ...utils import console
from ...utils import execution

from ..dependency import BuildDependency
from ..configuration import Configuration


class Ubuntu(Configuration):
    platform_name = 'Ubuntu'
    supported_platform_versions = ('17.04',)

    options = Configuration.options + [
        click.option(
            '--qt-cmake-path',
            type=click.Path(exists=True, writable=True, file_okay=False),
            required=True, help='Path to Qt CMake files. Usually located at $QTDIR/lib/cmake/'
        )
    ]

    def __init__(self):
        super().__init__()
        self.apt_packages = tuple()

    def _configure(self, options: typing.Dict):
        qt_build_options = {'CMAKE_PREFIX_PATH': options['qt_cmake_path']}

        self.apt_packages = (
            'git',
            'build-essential',
            'cmake',
            'repo',
            'mesa-common-dev',
            'libxfixes-dev',
            'libxcb-xfixes0-dev',
            'libxcb-keysyms1-dev',
            'libx11-xcb-dev',
            'libxrender-dev',
            'gperf',
            'zlib1g-dev',
            'libxml2-dev',
            'libxslt1-dev',
            'docbook-xml',
            'docbook-xsl',
            'flex',
            'bison',
            'libgcrypt20-dev',
            'network-manager-dev',
            'libnm-dev',
            'libpulse-dev',
            'libpolkit-agent-1-dev',
            'libpolkit-backend-1-dev',
            'libgbm-dev',
            'libinput-dev',
            'libflatpak-dev',
            'libxkbcommon-dev',
            'libboost-all-dev',
            'freeglut3-dev',
            'gstreamer1.0*',
            'libgstreamer1.0*',
            'libgstreamer-plugins-base1.0-dev',
            'libgles2-mesa-dev',
            'libxcb-cursor-dev',
            'libxcb-composite0-dev',
            'xorg-dev',
            'modemmanager-dev'
        )

        self.build_dependencies = (
            BuildDependency('https://github.com/KDE/extra-cmake-modules'),
            BuildDependency('https://github.com/KDE/ki18n', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kconfig', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kcoreaddons', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kwindowsystem', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kauth', build_options=qt_build_options),
            BuildDependency('https://github.com/kde/kcodecs', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kguiaddons', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kwidgetsaddons', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kconfigwidgets', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kdbusaddons', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/karchive', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kitemviews', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kiconthemes', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/phonon', use_latest_source_tag=False, build_options={
                **qt_build_options,
                **{'PHONON_BUILD_PHONON4QT5': 'ON'}
            }),
            BuildDependency('https://github.com/KDE/knotifications', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kcrash', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kdoctools', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kservice', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/polkit-qt-1', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/polkit-qt-1', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/kwallet', build_options=qt_build_options),
            BuildDependency('https://github.com/lxde/libqtxdg', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/networkmanager-qt', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/modemmanager-qt', build_options=qt_build_options),
            BuildDependency('https://github.com/KDE/solid', build_options=qt_build_options),
            BuildDependency('https://anongit.freedesktop.org/git/gstreamer/qt-gstreamer.git', build_options={
                **qt_build_options,
                **{'QT_VERSION': '5'}
            })
        )

    def install_packages(self, *packages):
        self.assert_configured()
        console.heading('Installing required packages ...')
        # Cannot be silenced in case a password
        # prompt comes up. Using apt's -q (quiet)
        # parameter instead.
        execution.run(
            'sudo', 'apt-get', 'install', *self.apt_packages,
            '-y', '-qq' if not self.verbose else ''
        )
        console.success('Finished installing required packages.')
