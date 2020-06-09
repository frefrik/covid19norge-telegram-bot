import requests
import json
import yaml
import time
from datetime import datetime, date, timedelta
from sqlitedict import SqliteDict

class VG():
    def __init__(self):
        self.urls = {
            'region': 'https://redutv-api.vg.no/corona/v1/sheets/norway-region-data',
            'fhi': 'https://redutv-api.vg.no/corona/v1/sheets/fhi',
            'reports': 'https://redutv-api.vg.no/corona/v1/areas/country/reports',
            'world_ts': 'https://redutv-api.vg.no/corona/v1/world/timeseries',
            'nordic_ts': 'https://redutv-api.vg.no/corona/v1/nordic/timeseries'
        }

        self.db = SqliteDict('./data/database.sqlite', 'vg', autocommit=True)

        self.rows = ['population',
                     'confirmed',
                     'dead',
                     'tested',
                     'hospitalized',
                     'intensiveCare',
                     'respiratory',
                     'quarantineEmployees',
                     'infectedEmployees']

        if 'confirmed' not in self.db:
            print('Table not found, creating')
            self.initiate()
            self.fetch_newdata()
            self.update_last_diff('all')

    def initiate(self):
        for row in self.rows:
            self.db[row] = {}

    def select_all(self):
        data =  self.db

        for i in data.items():
            print(i)

    def check_data_age(self, name, datatype):
        if datatype == 'current':
            data = self.db[name]['updated_ts']
            
        elif datatype == 'last':
            data = self.db[name]['last_updated_ts']

        if data >= datetime.now() + timedelta(seconds = -60):
            return True
        else:
            return False

    def get_last_diff(self, name):
        if name == 'all':
            for item in self.db.items():
                total = item[1]['total']
                last_total = item[1]['last_total']

                last_diff = total - last_total

                print(item[0], last_diff)

        else:
            db = self.db[name]
            total = db['total']
            last_total = db['last_total']

            last_diff = total - last_total

            return last_diff

    def update_last_diff(self, name):
        if name == 'all':
            for item in self.db.items():
                db = self.db[item[0]]
                db['last_updated_ts'] = datetime.now()
                db['last_total'] = db['total']
                
                self.db[item[0]] = db

        else:
            db = self.db[name]
            db['last_updated_ts'] = datetime.now()
            db['last_total'] = self.db[name]['total']

            self.db[name] = db

    def get_data(self, name, column):
        data_age = self.check_data_age(name, 'current')

        retries = 0
        while not data_age:
            retries += 1
            try:
                self.fetch_newdata()
                time.sleep(0.5)
                data_age = self.check_data_age(name, 'current')
            except:
                print('get_data: Error!')
        
            if retries == 3:
                break

        data = self.db[name][column]

        return data

    def get_all_data(self, name):
        data = self.db[name]
        
        return data
    
    def get_json(self, name):
        ret_str = requests.get(self.urls[name]).json()

        return ret_str

    def fetch_newdata(self):
        db = self.db

        fhi = requests.get(self.urls['fhi']).json()
        reports = requests.get(self.urls['reports']).json()['hospitals']['total']
        region = requests.get(self.urls['region']).json()['metadata']

        """ population """
        population_total = region['population']

        population = db['population']
        population['updated_ts'] = datetime.now()
        population['total'] = population_total

        db['population'] = population

        """ confirmed """
        confirmed_total = region['confirmed']['total']
        confirmed_newToday = region['confirmed']['newToday']
        confirmed_newToday_pctChg = round(confirmed_newToday / (confirmed_total - confirmed_newToday) * 100, 2)
        confirmed_newYesterday = region['confirmed']['newYesterday']
        confirmed_newYesterday_pctChg = round(confirmed_newYesterday / (confirmed_total - confirmed_newToday - confirmed_newYesterday) * 100, 2)
        confirmed_male = fhi['gender']['current']['male']
        confirmed_female = fhi['gender']['current']['female']

        confirmed = db['confirmed']
        confirmed['updated_ts'] = datetime.now()
        confirmed['total'] = confirmed_total
        confirmed['newToday'] = confirmed_newToday
        confirmed['newToday_pctChg'] = confirmed_newToday_pctChg
        confirmed['newYesterday'] = confirmed_newYesterday
        confirmed['newYesterday_pctChg'] = confirmed_newYesterday_pctChg
        confirmed['male'] = confirmed_male
        confirmed['female'] = confirmed_female

        db['confirmed'] = confirmed

        """ dead """
        dead_total = region['dead']['total']
        dead_newToday = region['dead']['newToday']
        dead_newToday_pctChg = round(dead_newToday / (dead_total - dead_newToday) * 100, 2)
        dead_newYesterday = region['dead']['newYesterday']
        dead_newYesterday_pctChg = round(dead_newYesterday / (dead_total - dead_newToday - dead_newYesterday) * 100, 2)
        dead_male = fhi['deathAges']['current']['gender']['male']
        dead_female = fhi['deathAges']['current']['gender']['female']
        dead_totalcases = fhi['deathAges']['current']['count']
        dead_age = fhi['deathAges']['current']['mean']

        dead = db['dead']
        dead['updated_ts'] = datetime.now()
        dead['total'] = dead_total
        dead['newToday'] = dead_newToday
        dead['newToday_pctChg'] = dead_newToday_pctChg
        dead['newYesterday'] = dead_newYesterday
        dead['newYesterday_pctChg'] = dead_newYesterday_pctChg
        dead['male'] = dead_male
        dead['female'] = dead_female
        dead['totalcases'] = dead_totalcases
        dead['age_mean'] = dead_age

        db['dead'] = dead

        """ tested """
        tested_total = fhi['tested']['current']['count']
        tested_newToday, tested_newYesterday, tested_newToday_pctChg, tested_newYesterday_pctChg = 0, 0, 0, 0

        for i in fhi['tested']['timeseries']:
            test_date = str(i['date'])
            if test_date == str(date.today()):
                tested_newToday = i['new']
                tested_newToday_pctChg = i['percentChange']
            if test_date == str(date.today() - timedelta(days=1)):
                tested_newYesterday = i['new']
                tested_newYesterday_pctChg = i['percentChange']

        tested = db['tested']
        tested['updated_ts'] = datetime.now()
        tested['total'] = tested_total
        tested['newToday'] = tested_newToday
        tested['newToday_pctChg'] = tested_newToday_pctChg
        tested['newYesterday'] = tested_newYesterday
        tested['newYesterday_pctChg'] = tested_newYesterday_pctChg

        db['tested'] = tested

        """ hospitalized """
        hospitalized_total = reports['hospitalized']
        hospitalized_male = fhi['hospitalization']['current']['gender']['male']
        hospitalized_female = fhi['hospitalization']['current']['gender']['female']
        hospitalized_totalcases = fhi['hospitalization']['current']['causedByCorona']
        hospitalized_age = fhi['hospitalization']['current']['age']['mean']

        hospitalized = db['hospitalized']
        hospitalized['updated_ts'] = datetime.now()
        hospitalized['total'] = hospitalized_total
        hospitalized['male'] = hospitalized_male
        hospitalized['female'] = hospitalized_female
        hospitalized['totalcases'] = hospitalized_totalcases
        hospitalized['age_mean'] = hospitalized_age

        db['hospitalized'] = hospitalized

        """ intensiveCare """
        icu_total = reports['intensiveCare']
        icu_male = fhi['intensiveCare']['current']['gender']['male']
        icu_female = fhi['intensiveCare']['current']['gender']['female']
        icu_totalcases = fhi['intensiveCare']['current']['total']
        icu_age = fhi['intensiveCare']['current']['age']['mean']

        intensiveCare = db['intensiveCare']
        intensiveCare['updated_ts'] = datetime.now()
        intensiveCare['total'] = icu_total
        intensiveCare['male'] = icu_male
        intensiveCare['female'] = icu_female
        intensiveCare['totalcases'] = icu_totalcases
        intensiveCare['age_mean'] = icu_age

        db['intensiveCare'] = intensiveCare

        """ respiratory """
        respiratory_total = reports['respiratory']

        respiratory = db['respiratory']
        respiratory['updated_ts'] = datetime.now()
        respiratory['total'] = respiratory_total

        db['respiratory'] = respiratory

        """ quarantineEmployees """
        quarantineEmployees_total = reports['quarantineEmployees']

        quarantineEmployees = db['quarantineEmployees']
        quarantineEmployees['updated_ts'] = datetime.now()
        quarantineEmployees['total'] = quarantineEmployees_total

        db['quarantineEmployees'] = quarantineEmployees

        """ infectedEmployees """
        infectedEmployees_total = reports['infectedEmployees']

        infectedEmployees = db['infectedEmployees']
        infectedEmployees['updated_ts'] = datetime.now()
        infectedEmployees['total'] = infectedEmployees_total

        db['infectedEmployees'] = infectedEmployees

if __name__ == "__main__":
    vg = VG()

    vg.select_all()
    #vg.get_last_diff('all')
    #vg.get_data('confirmed','total')