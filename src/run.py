"""Run Challange Resolution.
"""
import sys
import argparse
from datetime import datetime
from dextra import Dextra

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Dextra\'s Programming Challenge.')
    parser.add_argument('-d', dest='d_day', type=str,
                        help='D day (expected format: \'dd/mm/yyyy\', \
                              default: when empty, is defined as the \
                                  previous day from first cash flow)')

    args = parser.parse_args()

    try:
        if args.d_day:
            datetime.strptime(args.d_day, '%d/%m/%Y')
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)

    Dextra().run('./resources/Ativos.csv', d_day=args.d_day)
