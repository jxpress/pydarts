import os
from tempfile import mkdtemp
from shutil import rmtree

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
    da = PyDarts(["a", "ab", "abcd", "あい", "あいう", "あいうえ", "あいうえお"])

    assert len(da.search("abcdefg", longest=False)) == 3
    assert len(da.search("あいうえおお", longest=False)) == 4


def test_pydarts_search01(tmpdir):
    da = PyDarts(["", "a", "abcd"])

    assert len(da.search("abcdefg", longest=False)) == 2
    assert len(da.search("ありがとう", longest=False)) == 0


def test_pydarts_search02(tmpdir):
    da = PyDarts(["あり", "ありがと", "ありがとう", "さ", "ささ", "さようなら"])

    assert len(da.search("あありがとうと君にさようなら", longest=False)) == 5
    assert len(da.search("さようなiらさささ,ああああと", longest=False)) == 2
    assert len(da.search("", longest=False)) == 0


def test_pydarts_longest_search00(tmpdir):
    da = PyDarts(["あり", "ありがと", "ありがとう", "さ", "さよう", "さようなら"])

    assert len(da.search("あありがとうと君にさようなら")) == 2
    assert len(da.search("さよう、あり")) == 2
    assert len(da.search("")) == 0


def test_pydarts_longest_search01(tmpdir):
    da = PyDarts(["生命", "生命保険", "生命保険を考える会"])

    assert len(da.search("あありがとうと君にさようなら")) == 0
    assert len(da.search("生命の躍動")) == 1
    assert len(da.search("昨日未明、生命保険を考える会の会長が発言した")) == 1


def test_pydarts_longest_search02(tmpdir):
    da = PyDarts(["", "生命", "生命保険", "生命保険を考える会"])

    assert len(da.search("あありがとうと君にさようなら")) == 0
    assert len(da.search("生命の躍動")) == 1
    assert len(da.search("昨日未明、生命保険を考える会生命保険")) == 2


def test_pydarts_longest_search03(tmpdir):
    da = PyDarts(["生命", "生命保険", "生命保険を考える会"])

    assert len(da.search("生命保険生命保険生命保険を考える会生命")) == 3


def test_pydarts_longest_search04():
    da = PyDarts(["竹内", "竹内結子", "竹内結子問題", "竹内結子問題の記事"])

    assert len(da.search("竹内結子竹内結子問題の記事竹内")) == 3


def test_pydarts_longest_search05():
    da = PyDarts(list(sorted(['アイドリッシュセブン', 'セブン', 'イド', 'リッシュ', 'シュ', 'ブン'])))

    assert len(da.search("アイドリッシュセブン")) == 1

