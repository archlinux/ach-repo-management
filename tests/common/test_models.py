from contextlib import nullcontext as does_not_raise
from typing import ContextManager, List, Optional, Union

from pydantic import ValidationError
from pytest import mark, raises

from repod.common import models
from tests.conftest import (
    create_default_full_version,
    create_default_invalid_full_version,
)


@mark.parametrize(
    "value, expectation",
    [
        ("1", does_not_raise()),
        (1, does_not_raise()),
        ("0", raises(ValidationError)),
        ("-1", raises(ValidationError)),
        ("1.1", raises(ValidationError)),
    ],
)
def test_epoch(value: Union[str, int], expectation: ContextManager[str]) -> None:
    with expectation:
        assert isinstance(models.Epoch(epoch=value), models.Epoch)


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1", "1", 0),
        ("1", "2", -1),
        ("2", "1", 1),
        (1, 1, 0),
        (1, 2, -1),
        (2, 1, 1),
    ],
)
def test_epoch_vercmp(subj: Union[int, str], obj: Union[int, str], expectation: int) -> None:
    assert models.Epoch(epoch=subj).vercmp(epoch=models.Epoch(epoch=obj)) == expectation


@mark.parametrize(
    "value, expectation",
    [
        ("1", does_not_raise()),
        ("1.1", does_not_raise()),
        (1, does_not_raise()),
        (1.1, does_not_raise()),
        ("0", raises(ValidationError)),
        ("-1", raises(ValidationError)),
        ("1.a", raises(ValidationError)),
    ],
)
def test_pkgrel(value: str, expectation: ContextManager[str]) -> None:
    with expectation:
        assert isinstance(models.PkgRel(pkgrel=value), models.PkgRel)


@mark.parametrize(
    "value, expectation",
    [
        ("1", ["1"]),
        ("1.1", ["1", "1"]),
        (1, ["1"]),
        (1.1, ["1", "1"]),
    ],
)
def test_pkgrel_as_list(value: str, expectation: List[str]) -> None:
    assert models.PkgRel(pkgrel=value).as_list() == expectation


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1", "1", 0),
        ("2", "1", 1),
        ("1", "2", -1),
        ("1", "1.1", -1),
        ("1.1", "1", 1),
        ("1.1", "1.1", 0),
        ("1.2", "1.1", 1),
        ("1.1", "1.2", -1),
    ],
)
def test_pkgrel_vercmp(subj: str, obj: str, expectation: int) -> None:
    assert models.PkgRel(pkgrel=subj).vercmp(pkgrel=models.PkgRel(pkgrel=obj)) == expectation


@mark.parametrize(
    "value, expectation",
    [
        ("1", does_not_raise()),
        ("1.1", does_not_raise()),
        ("1.a", does_not_raise()),
        (1, does_not_raise()),
        (1.1, does_not_raise()),
        ("0", does_not_raise()),
        ("foo", does_not_raise()),
        ("-1", raises(ValidationError)),
        (".1", raises(ValidationError)),
    ],
)
def test_pkgver(value: str, expectation: ContextManager[str]) -> None:
    with expectation:
        assert isinstance(models.PkgVer(pkgver=value), models.PkgVer)


@mark.parametrize(
    "value, expectation",
    [
        ("1", ["1"]),
        ("1.1", ["1", "1"]),
        ("1.a", ["1", "a"]),
        ("1.1a", ["1", "1a"]),
        ("foo", ["foo"]),
        ("1_1", ["1", "1"]),
        ("1.1_1", ["1", "1", "1"]),
        (1, ["1"]),
        (1.1, ["1", "1"]),
    ],
)
def test_pkgver_as_list(value: str, expectation: List[str]) -> None:
    assert models.PkgVer(pkgver=value).as_list() == expectation


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1", "1", 0),
        ("2", "1", 1),
        ("1", "2", -1),
        ("1", "1.1", -1),
        ("1.1", "1", 1),
        ("1.1", "1.1", 0),
        ("1.2", "1.1", 1),
        ("1.1", "1.2", -1),
        ("1+2", "1+1", 1),
        ("1+1", "1+2", -1),
        ("1.1", "1.1a", 1),
        ("1.1a", "1.1", -1),
        ("1.1", "1.1a1", 1),
        ("1.1a1", "1.1", -1),
        ("1.1", "1.11a", -1),
        ("1.11a", "1.1", 1),
        ("1.1_a", "1.1", 1),
        ("1.1", "1.1_a", -1),
        ("1.a", "1.1", -1),
        ("1.1", "1.a", 1),
        ("1.a1", "1.1", -1),
        ("1.1", "1.a1", 1),
        ("1.a11", "1.1", -1),
        ("1.1", "1.a11", 1),
        ("a.1", "1.1", -1),
        ("1.1", "a.1", 1),
        ("foo", "1.1", -1),
        ("1.1", "foo", 1),
        ("a1a", "a1b", -1),
        ("a1b", "a1a", 1),
        ("20220102", "20220202", -1),
        ("20220202", "20220102", 1),
    ],
)
def test_pkgver_vercmp(subj: str, obj: str, expectation: int) -> None:
    assert models.PkgVer(pkgver=subj).vercmp(pkgver=models.PkgVer(pkgver=obj)) == expectation


@mark.parametrize(
    "value, expectation",
    [
        (f"{create_default_full_version()}", does_not_raise()),
        (f"{create_default_invalid_full_version()}", raises(ValidationError)),
    ],
)
def test_version(value: str, expectation: ContextManager[str]) -> None:
    with expectation:
        assert isinstance(models.Version(version=value), models.Version)


@mark.parametrize(
    "value, expectation",
    [
        ("1:1.0.0-1", models.Epoch(epoch=1)),
        ("1.0.0-1", None),
    ],
)
def test_version_get_epoch(value: str, expectation: Optional[models.Epoch]) -> None:
    assert models.Version(version=value).get_epoch() == expectation


@mark.parametrize(
    "value, expectation",
    [
        ("1:1.0.0-1", models.PkgVer(pkgver="1.0.0")),
        ("1:1_0_0-1", models.PkgVer(pkgver="1_0_0")),
        ("1.0.0-1", models.PkgVer(pkgver="1.0.0")),
        ("1_0_0-1", models.PkgVer(pkgver="1_0_0")),
    ],
)
def test_version_get_pkgver(value: str, expectation: Optional[models.PkgVer]) -> None:
    assert models.Version(version=value).get_pkgver() == expectation


@mark.parametrize(
    "value, expectation",
    [
        ("1:1.0.0-1", models.PkgRel(pkgrel="1")),
        ("1:1_0_0-1", models.PkgRel(pkgrel="1")),
        ("1.0.0-1", models.PkgRel(pkgrel="1")),
        ("1_0_0-1", models.PkgRel(pkgrel="1")),
        ("1:1.0.0-1.1", models.PkgRel(pkgrel="1.1")),
        ("1:1_0_0-1.1", models.PkgRel(pkgrel="1.1")),
        ("1.0.0-1.1", models.PkgRel(pkgrel="1.1")),
        ("1_0_0-1.1", models.PkgRel(pkgrel="1.1")),
    ],
)
def test_version_get_pkgrel(value: str, expectation: Optional[models.PkgRel]) -> None:
    assert models.Version(version=value).get_pkgrel() == expectation


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1.0.0-1", "1.0.0-1", 0),
        ("1.0.0-1", "1.0.0-2", -1),
        ("1.0.0-2", "1.0.0-1", 1),
        ("1.0.1-1", "1.0.0-1", 1),
        ("1.0.0-1", "1.0.1-1", -1),
        ("1:1.0.0-1", "1:1.0.0-1", 0),
        ("1:1.0.0-1", "1:1.0.0-2", -1),
        ("1:1.0.0-2", "1:1.0.0-1", 1),
        ("1:1.0.1-1", "1:1.0.0-1", 1),
        ("1:1.0.0-1", "1:1.0.1-1", -1),
        ("2:1.0.0-1", "1:1.0.0-1", 1),
        ("1:1.0.0-1", "2:1.0.1-1", -1),
        ("1:1.0.0-1", "1.0.0-1", 1),
        ("1.0.0-1", "1:1.0.0-1", -1),
    ],
)
def test_version_vercmp(subj: str, obj: str, expectation: int) -> None:
    assert models.Version(version=subj).vercmp(version=models.Version(version=obj)) == expectation


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1.2.3-1", "1.2.3-2", True),
        ("1.2.3-2", "1.2.3-1", False),
    ],
)
def test_version_is_older_than(subj: str, obj: str, expectation: bool) -> None:
    assert models.Version(version=subj).is_older_than(version=models.Version(version=obj)) is expectation


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1.2.3-1", "1.2.3-2", False),
        ("1.2.3-2", "1.2.3-1", True),
    ],
)
def test_version_is_newer_than(subj: str, obj: str, expectation: bool) -> None:
    assert models.Version(version=subj).is_newer_than(version=models.Version(version=obj)) is expectation