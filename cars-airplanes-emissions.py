# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st

#%% loading relevant frames
#@st.cache
def loaddata():
    global dfSrcCar, dfSrcPln
    dfSrcCar = pd.read_csv('cars.csv')
    dfSrcPln = pd.read_csv('planes.csv')
    
loaddata()

#%% sidebar setup
st.sidebar.markdown('## Configuration Settings')
inAirLoad = st.sidebar.slider('Assumed airplane passenger load:', 
                              min_value=1,
                              max_value=100,
                              value=100,
                              format='%g%%')
inCarPx = st.sidebar.slider('Assumed number of passengers in automobile:',
                            min_value=1,
                            max_value=6,
                            value=1,
                            format='%g')

#%% transform data

dfSrcCarMod = dfSrcCar.copy()
dfSrcCarMod['Cat'] = 'Automobile'
dfSrcCarMod['SCat'] = dfSrcCarMod['Vehicle Class']
dfSrcCarMod['Eff'] = (dfSrcCarMod['Fuel Consumption: Highway (L/100km)'] / 
                                inCarPx)
dfSrcCarMod['Label'] = (dfSrcCarMod['Make'] + ' ' + dfSrcCarMod['Model'] +
                           ' (' + dfSrcCarMod['Cylinders'].astype(int).astype(str) + 
                           ' Cylinder - ' + 
                           dfSrcCarMod['Engine Size (L)'].astype(str) + 'L)')
dfSrcCarMod = dfSrcCarMod[['Cat', 'SCat', 'Eff', 'Label']]

dfSrcPlnMod = dfSrcPln.copy()
dfSrcPlnMod['Cat'] = 'Airplane'
dfSrcPlnMod['SCat'] = dfSrcPlnMod['Class']
dfSrcPlnMod['Eff'] = ((dfSrcPlnMod['Fuel Efficiency (L/100km)'] * 
                       dfSrcPlnMod['Seats']) / 
                      (dfSrcPlnMod['Seats'] * (inAirLoad / 100)))
dfSrcPlnMod['Label'] = (dfSrcPlnMod['Model'] + ' - (' +
                        dfSrcPlnMod['Class'] + ' - ' +
                        dfSrcPlnMod['Sector'].astype(str) + 'km Trip)')
dfSrcPlnMod = dfSrcPlnMod[['Cat', 'SCat', 'Eff', 'Label', 'Sector']]