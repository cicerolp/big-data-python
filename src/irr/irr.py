import numpy as np


class IRR:
    """Class that implements the calculation of IRR for 'a series of cash flows that occur at 
    irregular intervals'. 
    
    It uses a binary search approach to speed up the computation. Based on NPV value,
    the algorithm tries to narrow both the upper and lower limits of an initial IRR
    value until it converges.
    """
    MAX_LOG = 1e05
    YEAR_LENGTH = 365.2425

    @staticmethod
    def compute(due_dates: list, cash_flow: list, max_iterations: int = 1000, tol: float = 1e-10):
        """Computes the IRR for a series of cash flows on specific dates.

        Args:
            due_dates: List of datetime64[ns] items.
            cash_flow: Cash flow list. The first element must be negative.
            max_iterations: Maximum number of iterations to run the binary search.
            tol: Tolerance for stopping criteria.

        Returns:
            xirr: The IRR value.
        """
        if len(due_dates) != len(cash_flow):
            raise ValueError('Arguments with different lengths.')

        if not len(due_dates):
            raise ValueError('Empty input arrays.')

        if cash_flow[0] > 0:
            raise ValueError('Invalid initial investiment value.')

        # compute years fraction from start_date
        years_fraction = IRR.get_years_fraction(due_dates)

        # set initial values
        xirr = 1
        xirr_lo, xirr_hi = - IRR.MAX_LOG, + IRR.MAX_LOG

        for _ in range(max_iterations):
            prev_xirr = xirr
            xirr = (xirr_lo + xirr_hi) / 2.0

            # test against TOL
            if abs(prev_xirr - xirr) < tol:
                return xirr

            # instead of iterating NPV until it reachs 0, we use it to
            # calculate IRR using a binary approach (faster than the naive alternative)
            npv = np.sum(cash_flow / np.power(1 + xirr, years_fraction))
            
            if np.sign(npv) < 0:
                # decrease upper limit
                xirr_hi = xirr
            else:
                # increase lower limit
                xirr_lo = xirr
        return xirr

    @staticmethod
    def get_years_fraction(dates: list):
        """Computes the year fractions related to a start date.

        Args:
            dates: List of datetime64[ns] items.

        Returns:
            array: List of year fractions.
        """
        if len(dates) < 2:
            raise ValueError(f'Invalid array length [{len(dates)}].')

        # compute years fraction from start_date
        return np.array(dates - dates[0], dtype='timedelta64[D]').astype(int) / IRR.YEAR_LENGTH