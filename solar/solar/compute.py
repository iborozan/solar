#conda activate py_demo
import pandas as pd
import numpy as np
import os
import sqlite3
import pickle
from numpy import *
import copy

def get_prediction(postal_code, size_kw, tilt, azimuth, latitude):
    """ Function that fits the best regression model and calculates predictions for the solar webapp"""
    size_kw = float(size_kw)
    tilt = float(tilt)
    # cost of electricity in Ontario at peak time 
    el_cost_on = 0.134
    # peak electricity rate = 71% incerase (over 10 years) + 18% inflation rate
    rate = 8.9
    time = 10
    # transform azimuth to degrees
    if azimuth == 'S':
        azimuth1 = 180
    elif azimuth == 'SW':
        azimuth1 = 180 + 45
    elif azimuth == 'W':
        azimuth1 = 180 + 90
    elif azimuth == 'NW':
        azimuth1 = 180 + 90 + 45
    elif azimuth == 'N':
        azimuth1 = 1
    elif azimuth == 'NE':
        azimuth1 = 45
    elif azimuth == 'E':
        azimuth1 = 90
    elif azimuth == 'SE':
        azimuth1 = 90 + 45
    print(azimuth1)
    conn = sqlite3.Connection("./models/nrel_data.db")
    nrel_data_point = pd.read_sql("SELECT * FROM nrel_data WHERE Zipcode = " + postal_code, con=conn)
    # calculate the tilt difference
    tilt_difference = abs(tilt - latitude)
    optimum_tilt = latitude
    # get the model prediction for irradinace 
    grid_search_gbrt = pickle.load( open( "./models/finalized_gbrt_model.sav", "rb" ) )
    # load the cost model 
    lin_reg_cost = pickle.load( open( "./models/finalized_lin_model_cost.sav", "rb" ) )
    # load the data processing pipeline 
    full_pipeline = pickle.load( open( "./models/full_pipeline.sav", "rb" ) )
    data =  array([size_kw, azimuth1, tilt_difference, nrel_data_point['DHI'].values[0], nrel_data_point['DNI'].values[0], nrel_data_point['GHI'].values[0], nrel_data_point['Temperature'].values[0], nrel_data_point['Wind Speed'].values[0]]).reshape(1,-1)
    df = pd.DataFrame(data, columns = ['size_kw', 'azimuth1', 'tilt_difference', 'DHI', 'DNI', 'GHI', 'Temperature', 'Wind Speed']) 
    test_data_point_tr = full_pipeline.transform(df)
    gbrt_ml = grid_search_gbrt.best_estimator_
    # output the predicted data 
    solar_energy_output_yr = gbrt_ml.predict(test_data_point_tr)
    cost_prediction = lin_reg_cost.predict(array(size_kw).reshape(1,-1))
    # taking into account an increase of 8.9% in elec cost over a year 
    total_annual_savings = solar_energy_output_yr * el_cost_on * pow((1 + rate / 100), 1)
    total_annual_savings_cum = solar_energy_output_yr * el_cost_on * (pow((1 + rate / 100), time))
    # estimated 15% error : is the average median error on the cost (see solar_eda_and_technical_report)
    error_cost = 0.1527
    break_even_time_low = (cost_prediction - cost_prediction*error_cost)/total_annual_savings_cum
    break_even_time_max = (cost_prediction + cost_prediction*error_cost)/total_annual_savings_cum
    return solar_energy_output_yr, cost_prediction, total_annual_savings, break_even_time_low, break_even_time_max, optimum_tilt


def process_postal_code(postal_code1):
    # take the first two letters of the postal code
    sub_str = '"' + postal_code1[0:3] + '"'
    return sub_str



