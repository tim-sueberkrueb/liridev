# -*- coding: utf-8

import typing


class Formatting:
    Purple = '\033[95m'
    Blue = '\033[94m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Red = '\033[91m'
    Bold = '\033[1m'
    Underline = '\033[4m'
    End = '\033[0m'


def heading(*text):
    log(*text, formatting=(Formatting.Purple, Formatting.Bold))


def info(*text):
    log(*text, formatting=(Formatting.Blue,))


def success(*text):
    log(*text, formatting=(Formatting.Green,))


def warning(*text):
    log(*text, formatting=(Formatting.Yellow,))


def error(*text):
    log(*text, formatting=(Formatting.Red,))


def log(*text, formatting: typing.Iterable[str] = None):
    formatting = formatting or tuple()
    print(*formatting, *text, Formatting.End, sep='')
