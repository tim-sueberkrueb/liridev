## Liri Development Tool

`liridev` is a tool to setup development requirements for [Liri][liri-gh].

### Dependencies
* `Python >= 3.5`
    * [click](http://click.pocoo.org)
* git
* repo

### Install
From the root of the repository, run:
```
python3 setup.py install
```

### Usage

Setup dependencies. This option may require build steps depending on your platform:
```sh
liridev deps setup \
                   --qt-cmake-path <path-to-qt>/lib/cmake
                   --path ~/dev/lirios/deps  # for example
```
Setting up a repository clone for [superbuild][lirios-superbuild-gh]:
```sh
liridev repo setup --path ~/dev/lirios/repo  # for example
```
Synchronize and update repository
```sh
liridev repo update --path ~/dev/lirios/repo  # for example
```

For a list of all commands, run:
```
liridev --help
```

### License
Licensed under the terms of the MIT license

[liri-gh]: https://github.com/lirios
[click-website]: http://click.pocoo.org
[lirios-superbuild-gh]: https://github.com/lirios/lirios
