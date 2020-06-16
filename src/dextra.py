from __future__ import annotations

import requests
import pandas as pd

from irr import IRR
from in_memory_db import InMemoryDBLite
from datetime import datetime, timedelta

import threading
from typing import Optional


class DextraMeta(type):
    """Thread-safe singleton factory.
    """
    _instance: Optional[Dextra] = None
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Dextra(metaclass=DextraMeta):
    """Class that implements all steps from Dextra's programming challenge.
    """
    INITIAL_INVESTMENT = 300000
    SELIC_ENDPOINT = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json'

    def __init__(self):
        self.xirr, self.selic_rate, self.selic_date = 0, 0, None

    def run(self, csv_file: str, initial_investiment=INITIAL_INVESTMENT, d_day: str = ''):
        """Implements the logic to resolve Dextra's challange.

        Args:
            csv_file: CSV file path. Should follow Dextra's structure.
            initial_investiment: Initial investiment amount. Positive float.
            d_day: Date of 'D' day. Format '%d/%m/%Y'. If empty,  'D' is defined as the previous day from first cash flow.
        """
        # 1. Read an CSV file with the assets
        df = self.read_and_transform_csv(csv_file, initial_investiment, d_day)

        # 2. Calculate the IRR
        # Calculate IRR for irregular intervals using a binary search approach
        self.xirr = IRR.compute(cash_flow=df['cash_flow'].to_numpy(
        ), due_dates=df['due_date'].to_numpy())

        # 3. Consume a public web service that return the Selic rate of the day
        self.selic_date, self.selic_rate = self.retrieve_current_selic()

        # 4. Show the IRR calculated and the Selic rate in console
        print(f'Internal Rate of Return:')
        print(f'\tInitial Date: {df["due_date"][0]}')
        print(f'\tInitial Investiment: {initial_investiment}')
        print(f'\tValue: {self.xirr:.2%}')

        print(f'Selic Rate:')
        print(f'\tDate: {self.selic_date}')
        print(f'\tValue: {self.selic_rate:.2%}')

        # 5. Store the information of the CSV file, the calculated IRR and Selic rate in a in memory database
        self.save_to_db(df)

    def read_and_transform_csv(self, csv_file: str, initial_investiment: float, d_day: str = '') -> pd.DataFrame:
        """Applies data transformations to the CSV to correcly load the assets.

        Args:
            csv_file: CSV file path. Should follow Dextra's structure.
            initial_investiment: Initial investiment amount. Positive float.
            d_day: Date of 'D' day. Format '%d/%m/%Y'. If empty,  'D' is defined as the previous day from first cash flow.

        Returns:
            df: Transformed CSV data in pd.DataFrame type.
        """
        # Read an CSV file with the assets
        df = pd.read_csv(csv_file, sep=';',
                         names=['asset', 'cash_flow', 'due_date'], usecols=[0, 1, 2], skiprows=1)

        df['cash_flow'] = df['cash_flow'].str.replace(
            r'(R\$|\.)', '').str.replace(',', '.').astype(float)
        df['due_date'] = pd.to_datetime(df['due_date'],  format='%d/%m/%Y')

        # Filter data based on 'D' day
        if not d_day:
            d_day = df['due_date'][0] - timedelta(days=1)
        else:
            d_day = pd.to_datetime(d_day, format='%d/%m/%Y', errors='ignore')

        df = df[df['due_date'] >= d_day]

        # Add initial investiment
        initial_df = pd.DataFrame.from_dict(
            {'due_date': [d_day], 'cash_flow': [-initial_investiment]})
        df = pd.concat([initial_df, df], ignore_index=True).sort_values(
            by='due_date')

        return df

    def retrieve_current_selic(self):
        """Consumes a public web service that returns the Selic rate of the day.

        Returns:
            date: Lastest valid Selic date.
            rate: Lastest valid Selic rate.
        """
        r = requests.get(Dextra.SELIC_ENDPOINT)

        if r.status_code == 200:
            # convert data
            data = r.json()[0]
            date = datetime.strptime(data['data'], '%d/%m/%Y')            
            rate = float(data['valor'])
        else:
            # invalid response from endpoint. using default values
            date = datetime.now()
            rate = 0.0

        return date, rate

    def save_to_db(self, df: pd.DataFrame):
        """Uses an in-memory database to save the CSV information, IRR and current Selic rates.

        Args:
            df: pd.DataFrame containing the transformed CSV data.
        """
        # create db_rate and saves the rate data
        db_rate = InMemoryDBLite(name='db_rate')
        db_rate.connect()
        db_rate.create_schema('rate', 'value')

        db_rate.insert({'rate': 'irr', 'value': self.xirr})
        db_rate.insert({'rate': 'selic', 'value': self.selic_rate})
        db_rate.disconnect()

        # create db_csv and saves the CSV data
        db_csv = InMemoryDBLite(name='db_csv')
        db_csv.connect()
        db_csv.create_schema('asset', 'cash_flow', 'due_date')

        db_csv.insert_multiple(df.to_dict('records'))
        db_csv.disconnect()
