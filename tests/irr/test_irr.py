import pytest
import numpy as np
from irr import IRR


@pytest.fixture
def irregular_cash_flow():
    due_date = np.arange(np.datetime64('2020-01-01'), np.datetime64(
        '2021-01-01'), np.timedelta64(30, 'D')).astype('datetime64[ns]')

    cash_flow = np.arange(1000, 1000 + (len(due_date) - 1) * 1000, 1000)
    cash_flow = np.insert(cash_flow, 0, -50000, axis=0)

    return {'due_date': due_date, 'cash_flow': cash_flow}


def test_positive(irregular_cash_flow):
    xirr = IRR.compute(due_dates=irregular_cash_flow['due_date'],
                       cash_flow=irregular_cash_flow['cash_flow'])
    assert(xirr >= 0)


def test_arrays_with_different_lengths():
    with pytest.raises(ValueError):
        IRR.compute(cash_flow=[-100], due_dates=[])


def test_empty_arrays():
    with pytest.raises(ValueError):
        IRR.compute(cash_flow=[], due_dates=[])


def test_invalid_initial_investiment():
    with pytest.raises(ValueError):
        IRR.compute(cash_flow=[100], due_dates=[
                    np.datetime64('2020-01-01').astype('datetime64[ns]')])
