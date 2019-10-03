GoSolar: Accurately predicting photovoltaic installation power generation using machine learning and weather information 
================================================================================================

**Author** Ivan Borozan 

About
=====

Developed a machine learning based model to accurately predict the energy output for residential solar panel installations in Ontario. The model is trained using real data obtained from two sources:

**Data**

* a dataset collected from [photovoltaic (PV) installations](https://openpv.nrel.gov/) on the ground by the National Renewable Energy Project (NREL) a national laboratory of the US Department of Energy

* a dataset from the [National Solar Radiation Database (NSRDB)](https://nsrdb.nrel.gov/) that includes hourly measures of weather patterns such as radiation, position of the sun, temperature and wind speed

The final product is a user friendly [webb app](http://hbaranalytics.com:5000) developed to help Ontario residents predict their solar installation annual energy output and other key characteristics with improved accuracy.

Based on geographical location, panel size, roof pitch and its orientation GoSolar web app provides predictions for:

* Annual Energy Output (kWh/year)
* Annual Return (CAD)
* Installation cost (CAD)
* Break Even Time (Years)
