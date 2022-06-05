from re import Match, fullmatch

from repod.common import regex


def test_absolute_path(absolute_dir: str) -> None:
    assert isinstance(fullmatch(regex.ABSOLUTE_PATH, absolute_dir), Match)


def test_invalid_absolute_path(invalid_absolute_dir: str) -> None:
    assert not isinstance(fullmatch(regex.ABSOLUTE_PATH, invalid_absolute_dir), Match)


def test_architectures(arch: str) -> None:
    assert isinstance(fullmatch(regex.ARCHITECTURE, arch), Match)


def test_invalid_architectures(arch: str) -> None:
    assert not isinstance(fullmatch(regex.ARCHITECTURE, "foo"), Match)


def test_buildenvs(buildenv: str) -> None:
    assert isinstance(fullmatch(regex.BUILDENVS, buildenv), Match)


def test_invalid_buildenvs(invalid_buildenv: str) -> None:
    assert not isinstance(fullmatch(regex.BUILDENVS, invalid_buildenv), Match)


def test_epoch(epoch: str) -> None:
    assert isinstance(fullmatch(regex.EPOCH, epoch), Match)


def test_invalid_epoch(invalid_epoch: str) -> None:
    assert not isinstance(fullmatch(regex.EPOCH, invalid_epoch), Match)


def test_filename(
    arch: str,
    epoch: str,
    package_name: str,
    pkgrel: str,
    version: str,
) -> None:
    assert isinstance(fullmatch(regex.FILENAME, f"{package_name}-{epoch}{version}-{pkgrel}-{arch}.pkg.tar.zst"), Match)


def test_invalid_filename(
    invalid_epoch: str,
    invalid_package_name: str,
    invalid_pkgrel: str,
    invalid_version: str,
) -> None:
    assert not isinstance(
        fullmatch(
            regex.FILENAME, f"{invalid_package_name}-{invalid_epoch}{invalid_version}{invalid_pkgrel}-foo.pkg.tar.zst"
        ),
        Match,
    )


def test_md5(md5sum: str) -> None:
    assert isinstance(fullmatch(regex.MD5, md5sum), Match)
    assert not isinstance(fullmatch(regex.MD5, md5sum[0:-2]), Match)


def test_options(option: str) -> None:
    assert isinstance(fullmatch(regex.OPTIONS, option), Match)


def test_invalid_options(invalid_option: str) -> None:
    assert not isinstance(fullmatch(regex.OPTIONS, invalid_option), Match)


def test_package_name(package_name: str) -> None:
    assert isinstance(fullmatch(regex.PACKAGE_NAME, package_name), Match)


def test_invalid_package_name(invalid_package_name: str) -> None:
    assert not isinstance(fullmatch(regex.PACKAGE_NAME, invalid_package_name), Match)


def test_packager_name(packager_name: str) -> None:
    assert isinstance(fullmatch(regex.PACKAGER_NAME, packager_name), Match)


def test_invalid_packager_name(invalid_packager_name: str) -> None:
    assert not isinstance(fullmatch(regex.PACKAGER_NAME, invalid_packager_name), Match)


def test_pkgrel(pkgrel: str) -> None:
    assert isinstance(fullmatch(regex.PKGREL, pkgrel), Match)


def test_invalid_pkgrel(invalid_pkgrel: str) -> None:
    assert not isinstance(fullmatch(regex.PKGREL, invalid_pkgrel), Match)


def test_relative_path() -> None:
    assert isinstance(fullmatch(regex.RELATIVE_PATH, "foo"), Match)


def test_invalid_relative_path(absolute_dir: str) -> None:
    assert not isinstance(fullmatch(regex.RELATIVE_PATH, absolute_dir), Match)


def test_sha256(sha256sum: str) -> None:
    assert isinstance(fullmatch(regex.SHA256, sha256sum), Match)
    assert not isinstance(fullmatch(regex.SHA256, sha256sum[0:-2]), Match)


def test_version(version: str) -> None:
    assert isinstance(fullmatch(regex.VERSION, version), Match)


def test_invalid_version(invalid_version: str) -> None:
    assert not isinstance(fullmatch(regex.VERSION, invalid_version), Match)
