# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st

#%% loading relevant frames
@st.cache
def loaddata():
    global dfSrcCars, dfSrcPlanes
    dfSrcCars = pd.read_csv('cars.csv')
    dfSrcPlanes = pd.read_csv('planes.csv')
    
loaddata()

#%% sidebar setup
st.sidebar.markdown('## Configuration Settings')
st.sidebar.slider('Assumed airplane passenger load:', 
                  min_value=0,
                  max_value=100,
                  value=100,
                  format='%g%%')