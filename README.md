## GoSolar: accurately predicting photovoltaic installation power generation using machine learning and weather information 

<p class="aligncenter">
<img src="./figures/solar-city-Japan.jpg" align="middle" width="100%" height="300">
</p>


**Author** Ivan Borozan 

About
=====

Developed a machine learning based model to accurately predict the energy output for residential solar panel installations in Ontario. 

**Data**

The model is trained using real data obtained from two sources:

* a dataset collected from [photovoltaic (PV) installations](https://openpv.nrel.gov/) on the ground by the National Renewable Energy Project (NREL) a national laboratory of the US Department of Energy

* a dataset from the [National Solar Radiation Database (NSRDB)](https://nsrdb.nrel.gov/) that includes hourly measures of weather patterns such as radiation, position of the sun, temperature and wind speed

Variables such as Global Horizontal Irradiance (GHI), Direct Horizontal Irradiance (DHI), Direct Normal Irradiance (DNI), Wind Speed, Temperature and Solar Zenith Angle obtained from NSRDB were averaged over a year. 

**EDA short summary**

Due to a significant difference in solar irradiance along the four cardinal directions North/South and East/West as shown in the figures below  

<p float="left">
  <img src="./figures/Solargis-North-America-DNI-solar-resource-map-en.png"" width="40%" height="30%">
  <img src="./figures/DNI_irradiance_gimp.png" width="470" height="360"> 
</p>


only solar installations within the US located within a rectangular region in blue ('Direct Normal Irradiance' figure above) are used for further analysis.  

In figure below we show the same US installations and their proximity to communities in Ontario.

<p float="left">
   <img src="./figures/Ontaro_communities2.png" width="400" height="400"> 
</p>

After data processing and feature selection 8 numerical features

- Size (kW)
- array tilt
- Temperature
- Wind Speed
- Azimuth
- Direct Normal Irradiance
- Direct Horizontal Irradiance 
- Global Horizontal Irradiance 

and 76859 data points were used for training, validation, model selection and evaluation on the test set (for more detail about the analysis see the [technical report](./notebooks/solar_eda_and_technical_report.ipynb)).  

**Web app**

The final product is a user friendly [webb app](http://hbaranalytics.com:5000) developed to help Ontario residents predict their solar installation annual energy output and other key characteristics with improved accuracy.

Based on geographical location, panel size, roof pitch and its orientation GoSolar web app provides predictions for:

* Annual Energy Output (kWh/year)
* Annual Return (CAD)
* Installation cost (CAD)
* Break Even Time (Years)
