import time
import pandas as pd
from sqlitedict import SqliteDict
from datetime import datetime, date, timedelta

class Covid19Nor:
    def __init__(self):
        self.urls = {
            'admissions_nat': 'https://raw.githubusercontent.com/frefrik/covid19-nor-admissions/master/data/admissions_nat.csv',
            'national_tests': 'https://raw.githubusercontent.com/thohan88/covid19-nor-data/master/data/03_covid_tests/national_tests.csv'
        }

        self.db = SqliteDict('./data/database.sqlite', 'cocvid19nor', autocommit=True)

        self.rows = ['admissions', 'respiratory', 'tested']

        if 'tested' not in self.db:
            print('Table not found, creating')
            self._initiate()
            self._fetch_newdata()

    def _initiate(self):
        for row in self.rows:
            self.db[row] = {}

    def _check_data_age(self, name):
        data = self.db[name]['updated_ts']

        if data >= datetime.now() + timedelta(seconds = -60):
            return True
        else:
            return False

    def _fetch_newdata(self):
        db = self.db
        today = date.today()
        yesterday = today - timedelta(days=1)

        tested_df = pd.read_csv(self.urls['national_tests'])
        admissions_df = pd.read_csv(self.urls['admissions_nat'])

        """ tested """
        tested_last_date = tested_df.date.max()
        tested_newToday, tested_newYesterday, tested_newToday_pctChg, tested_newYesterday_pctChg = 0, 0, 0, 0
        tested_current = tested_df[tested_df.date == tested_df.date.max()]
        tested_total = tested_current.n_tests_cumulative.values[0].astype(int)

        if tested_last_date == str(today):
            tested_newToday = tested_current.n_tests.values[0].astype(int)
            tested_newToday_pctChg = round(tested_newToday / (tested_total - tested_newToday)*100,2)

        if tested_last_date == str(yesterday):
            tested_newYesterday = tested_df[tested_df.date == str(yesterday)].n_tests.values[0].astype(int)
            tested_newYesterday_pctChg = round(tested_newYesterday / (tested_total - tested_newToday - tested_newYesterday)*100,2)

        tested = db['tested']
        tested['updated_ts'] = datetime.now()
        tested['total'] = tested_total
        tested['newToday'] = tested_newToday
        tested['newToday_pctChg'] = tested_newToday_pctChg
        tested['newYesterday'] = tested_newYesterday
        tested['newYesterday_pctChg'] = tested_newYesterday_pctChg
        db['tested'] = tested

        """ admissions """
        admissions_current = admissions_df[admissions_df.date == admissions_df.date.max()]
        admissions_total = admissions_current.admissions.values[0].astype(int)

        admissions = db['admissions']
        admissions['updated_ts'] = datetime.now()
        admissions['total'] = admissions_total
        db['admissions'] = admissions

        """ respiratory """
        respiratory_current = admissions_df[admissions_df.date == admissions_df.date.max()]
        respiratory_total = respiratory_current.respiratory.values[0].astype(int)

        respiratory = db['respiratory']
        respiratory['updated_ts'] = datetime.now()
        respiratory['total'] = respiratory_total
        db['respiratory'] = respiratory

    def select_all(self):
        data =  self.db

        for i in data.items():
            print(i)

    def get_data(self, name, column):
        data_age = self._check_data_age(name)

        retries = 0
        while not data_age:
            retries += 1
            try:
                print('Fetching new data, #', retries)
                self._fetch_newdata()
                time.sleep(0.5)
                data_age = self._check_data_age(name)
            except:
                print('get_data: Error!')
        
            if retries == 3:
                break

        data = self.db[name][column]

        return data
    
    def get_timeseries(self, name):
        if name == 'tested':
            df = pd.read_csv(self.urls['national_tests'])

            idx = pd.date_range(df['date'].min(), date.today())
            df.index = pd.DatetimeIndex(df['date'])
            df = df.reindex(idx)
            df['date'] = df.index
            df = df.reset_index(drop=True)

            df['n_tests'] = df['n_tests'].fillna(0).astype(int)
            df['n_tests_cumulative'] = df['n_tests_cumulative'].fillna(method='ffill').astype(int)

        elif name in ('admissions', 'respiratory'):
            df = pd.read_csv(self.urls['admissions_nat'], usecols=['date', name])
        else:
            df = None

        return df

if __name__ == "__main__":
    c19 = Covid19Nor()


    respiratory = c19.get_data('respiratory', 'total')
    admissions = c19.get_data('admissions', 'total')
    tested = c19.get_data('tested', 'total')
    print(respiratory)
    print(admissions)
    print(tested)
    ts = c19.get_timeseries('respiratory')
    print(ts)
