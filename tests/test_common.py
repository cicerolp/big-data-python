import pytest
import numpy as np


@pytest.fixture
def dextra_asset():
    from dextra import Dextra
    instance = Dextra()
    instance.run('./resources/Ativos.csv')
    return instance


def test_xirr(dextra_asset):
    assert dextra_asset.xirr == pytest.approx(0.72, 0.1)