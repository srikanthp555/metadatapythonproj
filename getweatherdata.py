"""
imports modules json, datetime, requests and pandas
"""
import json
import datetime
import os
import requests
import pandas as pd

class GetWeatherData:
    """
    Represents GetWeatherData Class which generates data from openweathermap
    and transforms data based o given requirement

    ...

    Methods
    -------
    geturl(lat, lon, unix_time):
        Generates URL to send get request to openweathermap API
    getFlattenJSON():
        Transforms JSON dtaa to Flatten structure
    getFirstDataset():
        Generate first dataset requirement to get highest temp
    getSecondDataset():
        Generate second dataset requirement to get max,min,avg temp
    getData():
        Send API requests to openweathermap API
    """

    def geturl(self, lat, lon, unix_time, api_key):
        """
        To get URL with location and date
        """
        try:
            base_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
            #api_key = "b6f5221855dd7432fcbb52b170b5f172"
            url = base_url + "lat=" + lat + "&lon=" + lon + \
                "&dt=" + unix_time + "&appid=" + api_key
            return url

        except Exception as e:
            print(f"Exception in geturl: {str(e)}")

    def getflattenjson(self):
        """
        Method to extract flatten JSON from nested JSON
        """
        try:
            print("Read JSON data. Flatten the data and deduplicate process - Start")
            with open('data.json', 'r', encoding='utf-8') as jsonfile:
                data_list = json.load(jsonfile)
            datadf = pd.json_normalize(
                    data_list, meta=['lat', 'lon', 'timezone', 'timezone_offset'], record_path='hourly')
            datadf.drop_duplicates(subset=['lat', 'lon', 'dt'], keep='first', inplace=True)
            print("Write Flatten data into text file: original_data.txt")
            datadf.to_csv(r'original_data.txt', header=True, index=None, sep='|', mode='w')
            print(f"Read JSON Data. Flatten the data and deduplicate process - End")
            self.getfirstdataset()

        except Exception as e:
            print(f"Exception in getflattenjson: {str(e)}")

    def getfirstdataset(self):
        """
        Method to retrieve step-3 first datasets
        """
        try:
            print("Build First Dataset containing location, date and highest temperature - Start")
            print("getfirstdataset - Read whole 5 days deduplicated data")
            datadf = pd.read_csv('original_data.txt', sep='|')
            datadf['date'] = pd.to_datetime(datadf['dt'],unit='s')
            datadf['month'] = datadf['date'].dt.month
            datadf.drop('dt', axis=1, inplace=True)
            print("getfirstdataset - record highest temperatures by location and month")
            datadf = datadf[datadf.groupby(
                ['timezone', 'month'])['temp'].transform('max') == datadf['temp']]
            datadf1 = datadf[['date', 'timezone', 'temp']]
            datadf1.columns.values[[0, 1, 2]] = ['date', 'location', 'highest_temp']
            print("getfirstdataset - write first dataset into csv file")
            datadf1.to_csv(r'firstdataset.txt', header=True, index=None, sep='|', mode='w')
            print("Build First Dataset containing location, date and highest Temperature - End")
            print(f"First Dataset: {datadf1}")
            self.getseconddataset()

        except Exception as e:
            print(f"Exception in getfirstdataset: {str(e)}")

    def getseconddataset(self):
        """
        Method to retrieve step-3 second dataset
        """
        try:
            print("Build Second Dataset containing avg temp, min temp, loc of min temp, max temp - Start")
            print("getseconddataset - Read whole 5 days deduplicated data")
            datadf = pd.read_csv('original_data.txt', sep='|')
            datadf['date'] = pd.to_datetime(datadf['dt'],unit='s')
            datadf['day'] = datadf['date'].dt.day
            datadf['date'] = datadf['date'].dt.date
            datadf.drop('dt', axis=1, inplace=True)
            print("getseconddataset - get max temp, loc of max temp - per day")
            datadf_max = datadf[datadf.groupby(['day'])['temp'].transform('max') == datadf['temp']]
            datadf_max = datadf_max[['date', 'timezone', 'temp', 'day']]
            datadf_max.columns.values[[0, 1, 2, 3]] = [
                    'date', 'location_of_max_temp', 'max_temperature', 'day']
            datadf_max = datadf_max.drop_duplicates(
                    subset=['date', 'location_of_max_temp', 'max_temperature', 'day'], keep='first')
            #print(f"{datadf_max}")
            print("getseconddataset - get min temp, loc of min temp - per day")
            datadf_min = datadf[datadf.groupby(['day'])['temp'].transform('min') == datadf['temp']]
            datadf_min = datadf_min[['timezone', 'temp', 'day']]
            datadf_min.columns.values[[0, 1, 2]] = ['location_of_min_temp', 'min_temperature', 'day']
            datadf_min = datadf_min.drop_duplicates(
                    subset=['location_of_min_temp', 'min_temperature', 'day'], keep='first')
            #print(f"{datadf_min}")
            print("getseconddataset - get avg temp per day")
            datadf_mean = datadf.groupby(['day'], as_index=False)['temp'].mean()
            datadf_mean.columns.values[[0, 1]] = ['day', 'avg_temperature']
            #print(f"{datadf_mean}")
            datadf_merge = pd.merge(datadf_max, datadf_min, on='day')
            datadf_fin_merge = pd.merge(datadf_merge, datadf_mean, on='day')
            #print(f"{datadf_fin_merge}")
            datadf_fin_merge.drop('day', axis=1, inplace=True)
            datadf_fin_merge.to_csv(r'seconddataset.txt', header=True, index=None, sep='|', mode='w')
            print("Build Second Dataset containing avg temp, min temp, loc of min temp, max temp - End")
            print(f"Second Dataset: {datadf_fin_merge}")

        except Exception as e:
            print(f"Exception in getseconddataset: {str(e)}")

    def getdata(self):
        """
        To get Data with URL submission on OpenWeatherMapAPI call
        """
        try:
            lat = ['48.208174','26.228516', '50.85034', '27.472792', '4.903052',
                    '42.697708', '11.544873', '28.613939', '51.507351', '38.907192']
            lon = ['16.373819', '50.58605', '4.35171', '89.639286', '114.939821',
                    '23.321868', '104.892167', '77.209021', '-0.127758', '-77.036871']
            data_list = []
            api_key = os.environ["API_KEY"]
            #api_key = "b6f5221855dd7432fcbb52b170b5f172"
            response_success = None
            response_err_code = ''
            print(f"API KEY from docker-compose file: {api_key}")
            print("Connect openweathermap API and retrieve last 5 days data - START")
            for i in range(10):
                #print(f"lat is:{lat[i]}")
                #print(f"lon is:{lon[i]}")
                for day_cnt in range(1, 6):
                    yesterday = datetime.date.today() - datetime.timedelta(day_cnt)
                    url = self.geturl(lat[i], lon[i], yesterday.strftime("%s"), api_key)
                    #print(f"URL in getData:{url}")
                    # HTTP request
                    response = requests.get(url)
                    #print(response)
                    # checking the status code of the request
                    if response.status_code == 200:
                        # getting data in the json format
                        data = response.json()
                        data_list.append(data)
                        response_success = 'YES'
                        #print(f"data is {type(data_list)}")
                    else:
                        # showing the error message
                        print(f"Error in the HTTP request:{response.status_code}")
                        response_success = 'NO'
                        response_err_code = response.status_code
            #print(f"Data for one loc:{type(data_list)}")
            if response_success == 'YES':
                print("Connect openweathermap API and retrieve last 5 days data - END")
                print("Write JSON data into file data.json - Start")
                with open('data.json', 'w', encoding='utf-8') as jsonfile:
                    json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)
                print("Write JSON data into file data.json - End")
                self.getflattenjson()
            else:
                print("Connect openweathermap API Failed with error:{response_err_code}")

        except Exception as e:
            print(f"Exception in getdata: {str(e)}")

if __name__ == '__main__':

    try:
        getweatherdata = GetWeatherData()
        print("in getweatherdata main")
        getweatherdata.getdata()
        print("End")

    except Exception as e:
        print(f"Exception in main: {str(e)}")
