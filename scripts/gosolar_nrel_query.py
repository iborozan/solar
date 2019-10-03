#!/usr/bin/python
# Filename: gosolar_nrel_query.py
# conda activate py_demo

import time
from datetime import datetime
import random
import pandas as pd
import numpy as np
import sqlite3
import requests
from sqlite3 import Error
import sys, os

# connect to the database 
def sql_connection():
    try:
        conn = sqlite3.connect('./gosolar.db')
        return conn
    except Error:
        print(Error)


# first initialize the table that tracks the donwloaded postal codes          
def sql_create_table(conn):
    '''create track_postal_codes table'''
    cursorObj = conn.cursor()
    try:
        cursorObj.execute("SELECT * FROM track_postal_codes")
        last_post_code_success = pd.read_sql("SELECT * FROM track_postal_codes", con=conn)["zipcode"][0]
        print('table track_postal_codes exists, last postal code downloaded is:', last_post_code_success)
    except Error:
        print('create table track_postal_codes in gosolar.db for tracking downloaded data from nrel.')
        initialize_pcode_df = pd.DataFrame({'zipcode': [0]})
        initialize_pcode_df.to_sql("track_postal_codes", con=conn)

        

def query_nrel(fails, last_post_code_success):
    """
    Main function to query NREL 
    """
    try:
        # see NSRDB download instructions using API: https://developer.nrel.gov.docs/solar/nsrdb/
        url = 'http://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
        # Return all but first 2 lines of csv to get data:
        info = pd.read_csv(url, nrows=2)
        df = pd.read_csv(url, skiprows=2)
        # creating a pivot table of our data with average values over a year 
        pivot = df.pivot_table(["GHI","DHI","DNI","Wind Speed","Temperature","Solar Zenith Angle"], index="Year")
        for c in pivot.columns:
            postal_code_values[c].append(pivot[c].values[0])
        postal_code_values["Zipcode"].append(all_postal_codes[floor_lower_iter:top_lower_iter][i])
        print('going to the next postal code')
        # only allowed to do 1000 requests per hour
        # see https://developer.nrel.gov/docs/rate-limits/
        # 3600/1000 = 3.6s set it up to 5s  
        wait_time = 5
        time.sleep(wait_time)
        # Updating last_post_code_success, it should be the top level iteration + lower level iteration.
        last_post_code_success = top_loop_iter + i
        # reset our successive_fails variable to 0, because we've had a success and want to stop counting them.
        fails = 0
    except:
        url = 'http://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
        # Add 1 to our successive_fails variable, which will iterate for every fail on the same zipcode.
        fails += 1
        resp = requests.get(url)
        response_code = resp.status_code
        print(response_code)
        if response_code == 429 and fails <= 6:
            wait_time = 5
            time.sleep(wait_time)
            fails, last_post_code_success = query_nrel(fails, last_post_code_success)
        else:
            print("postal code failed, going to the next postal code")
            failed_postal_codes.append(top_loop_iter + i)
            wait_time = 5
            time.sleep(wait_time)
    return fails, last_post_code_success



if __name__ == '__main__':
    print ('This script will query the NREL API if provided with a list of postal/zip codes')
    if (len(sys.argv)!=2):
        print ("Need to provide a file with postal codes, latitude, lognitude:")
        print ("Usage: python gosolar_nrel_query.py file_name_with_postal_codes.csv")
        exit(1)

    file_postal_codes = sys.argv[1]   

    postcode = pd.read_csv('./' + sys.argv[1])

    # loading in the csv file that has all the zipcodes with their corresponding lat/lon pairs
    start_date = datetime.now().time()
    
    # values for the api query
    # You must request an NSRDB api key from https://developer.nrel.gov/signup/
    api_key = '-------'
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle'
    year = '2015'
    leap_year = 'false'
    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '60'
    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'false'
    # Your full name, use '+' instead of spaces.
    your_name = '------'
    reason_for_use = 'model+testing'
    your_affiliation = 'Insight'
    your_email = '---------'
    mailing_list='true'

    # obtain series of the lats, lons, and postal codes 
    lats = postcode["Latitude"].values
    lons = postcode["Longitude"].values

    # us (zip) + canada postal codes
    all_postal_codes = postcode["zipcode"].values

    # connect to the database 
    conn = sql_connection()

    # this will initialize the table if it does not exist 
    sql_create_table(conn)

    # find the last postal code that was succefuly donwloaded 
    start_post_code = pd.read_sql("SELECT * FROM track_postal_codes", con=conn)["zipcode"][0]

    # set the last iteration for the top loop since you are only allowed to do 2k/day queries  
    # there is also a limit of 1000/hr queries  
    # https://developer.nrel.gov/docs/solar/nsrdb/guide/
    stop_iter_top_loop = start_post_code  + 2000

    # set iteration step 
    iteration_step = 500

    # change the iteration step if greater than the nimber of rows in the intial file woth postal codes 
    if stop_iter_top_loop > len(all_postal_codes):
        stop_iter_top_loop = len(all_postal_codes)
        # change iteration step if start_iter_top_loop . 
        iteration_step = stop_iter_top_loop - start_post_code


    # set this as a placeholder variable to be updated during the download process  
    last_post_code_success = pd.read_sql("SELECT * FROM track_postal_codes", con=conn)["zipcode"][0]

    # track postal codes that failed during the donwloaded 
    failed_postal_codes = []

    # top loop 
    for top_loop_iter in range(start_post_code, stop_iter_top_loop, iteration_step):

        print('starting from the position of the last postal code that was successfully downloaded:', last_post_code_success)

        postal_code_values = {
            "Zipcode": [],
            "DHI": [],
            "DNI": [],
            "GHI": [],
            "Solar Zenith Angle": [],
            "Temperature": [],
            "Wind Speed": []
        }

        floor_lower_iter = int(top_loop_iter)
        top_lower_iter = int(top_loop_iter) + iteration_step

        # setting our successive_fails variable, used by the query_nrel function.
        successive_fails = 0

        for i, (lat, lon) in enumerate(zip(lats[floor_lower_iter:top_lower_iter], lons[floor_lower_iter:top_lower_iter])):

            print(lat, lon, i)

            #if we get 15 successive 429 responses the query function will stop.
            if successive_fails <= 15:
                successive_fails, last_post_code_success = query_nrel(successive_fails, last_post_code_success)
                print("successive fails: ", successive_fails)
            else:
                #break
                print("Reached maximum request") 
                sys.exit()
                
        # only export to csv and to the db if data available  
        if len(postal_code_values['Zipcode']) > 0:
            postal_code_df = pd.DataFrame(postal_code_values)
            # exporting the data as a csv.
            postal_code_filepath = "./nrel_data_%s.csv" % str(floor_lower_iter)
            postal_code_df.to_csv(postal_code_filepath)
            # add this to our database as well.
            postal_code_df.to_sql("nrel_postal_code_data", con=conn, if_exists='append')
            print("exporting csv for iteration range: %s : %s" % (floor_lower_iter, top_lower_iter))


    # change last_success table in db
    last_success_df = pd.DataFrame({'zipcode': [last_post_code_success]})
    last_success_df.to_sql("track_post_code", con=conn, if_exists='replace')

    # adding the failed zips to the failed_zips table in our db
    failed_postal_codes_df = pd.DataFrame({'postal_code_index':failed_postal_codes})
    failed_postal_codes_df.to_sql("failed_postal_codes", if_exists='append', con=conn)

    finish_date = datetime.now().time()

    #print(datetime.now().time())
    print("Downloaded data for %s postal codes between %s and %s" % (last_post_code_success, start_date, finish_date))
    
