# coding: utf-8

import os
from tempfile import mkdtemp
from shutil import rmtree

from six import u
import pytest

from pydarts import PyDarts, PyDartsError


@pytest.fixture(scope='function')
def tmpdir(request):
    path = mkdtemp()
    request.addfinalizer(lambda: rmtree(path))
    return path


def test_pydarts_load_unexists_file():
    with pytest.raises(PyDartsError):
        PyDarts.load(os.path.join('unknown.dict'))


def test_pydarts_build_from_empty(tmpdir):
    with pytest.raises(PyDartsError):
        PyDarts([])


def test_pydarts_search00(tmpdir):
    da = PyDarts([u("a"), u("ab"), u("abcd"), u("あい"), u("あいう"), u("あいうえ"), u("あいうえお")])

    assert len(da.search(u("abcdefg"), longest=False)) == 3
    assert len(da.search(u("あいうえおお"), longest=False)) == 4


def test_pydarts_search01(tmpdir):
    da = PyDarts([u(""), u("a"), u("abcd")])

    assert len(da.search(u("abcdefg"), longest=False)) == 3
    assert len(da.search(u("ありがとう"), longest=False)) == 1


def test_pydarts_search02(tmpdir):
    da = PyDarts([u("あり"), u("ありがと"), u("ありがとう"), u("さ"), u("ささ"), u("さようなら")])

    assert len(da.search(u("あありがとうと君にさようなら"), longest=False)) == 5
    assert len(da.search(u("さようなiらさささ,ああああと"), longest=False)) == 2
    assert len(da.search(u(""), longest=False)) == 0


def test_pydarts_longest_search00(tmpdir):
    da = PyDarts([u("あり"), u("ありがと"), u("ありがとう"), u("さ"), u("さよう"), u("さようなら")])

    assert len(da.search(u("あありがとうと君にさようなら"))) == 2
    assert len(da.search(u("さよう、あり"))) == 2
    assert len(da.search(u(""))) == 0


def test_pydarts_longest_search01(tmpdir):
    da = PyDarts([u("生命"), u("生命保険"), u("生命保険を考える会")])

    assert len(da.search(u("あありがとうと君にさようなら"))) == 0
    assert len(da.search(u("生命の躍動"))) == 1
    assert len(da.search(u("昨日未明、生命保険を考える会の会長が発言した"))) == 1


def test_pydarts_longest_search02(tmpdir):
    da = PyDarts([u(""), u("生命"), u("生命保険"), u("生命保険を考える会")])

    assert len(da.search(u("あありがとうと君にさようなら"))) == 1
    assert len(da.search(u("生命の躍動"))) == 2
    assert len(da.search(u("昨日未明、生命保険を考える会生命保険"))) == 3


def test_pydarts_longest_search03(tmpdir):
    da = PyDarts([u("生命"), u("生命保険"), u("生命保険を考える会")])

    assert len(da.search(u("生命保険生命保険生命保険を考える会生命"))) == 3


def test_pydarts_longest_search04():
    da = PyDarts([u("竹内"), u("竹内結子"), u("竹内結子問題"), u("竹内結子問題の記事")])

    assert len(da.search(u("竹内結子竹内結子問題の記事竹内"))) == 3
