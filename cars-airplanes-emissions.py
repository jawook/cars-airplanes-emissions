# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

clrs = px.colors.qualitative.D3
mbOff = {'displayModeBar': False}

#%% loading relevant frames
#@st.cache
def loaddata():
    global dfSrcCar, dfSrcPln
    dfSrcCar = pd.read_csv('cars.csv')
    dfSrcPln = pd.read_csv('planes.csv')
    
loaddata()

#%% configuration settings
st.set_page_config(page_title='Emissions: Planes vs. Automobiles', page_icon='favicon.png')

st.markdown('# Planes, (no trains), and automobiles: which is worse for emissions?')
st.markdown('#### Configuration Settings')

colA1, colABlnk, colA2 = st.columns((10, 2, 10))
with colA1:    
    inAirLoad = st.slider('Assumed airplane passenger load:', 
                          min_value=1,
                          max_value=100,
                          value=100,
                          format='%g%%')
with colA2:    
    inCarPx = st.slider('Assumed number of passengers in automobile:',
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
dfSrcCarMod = dfSrcCarMod.groupby('Label').agg({'Cat': 'first',
                                                'SCat': 'first',
                                                'Eff': 'mean'})

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
dfSrcPlnMod = dfSrcPlnMod.groupby('Label').agg({'Cat': 'first',
                                                'SCat': 'first',
                                                'Eff': 'mean',
                                                'Sector': 'mean'})

#%% top chart
st.markdown('#### Fuel economy per passenger for airplanes and automobiles')

carCats = st.multiselect(label=('Types of vehicles to include in chart (click ' +
                                'in grey box to add additional types)'),
                      options=dfSrcCarMod['SCat'].unique(),
                      default=['SUV: Small'])
plnCats = st.multiselect(label=('Types flights to include in chart (click ' +
                                'in grey box to add additional types)'),
                      options=dfSrcPlnMod['SCat'].unique(),
                      default=[dfSrcPlnMod['SCat'].unique()[1]])
st.markdown(('*liters per 100km per passenger based on airplane passenger load of ' + 
             str(inAirLoad) + '% and ' + str(inCarPx) + ' passengers per ' +
             'automobile, hover for details*'))                          

ch1CarDf = dfSrcCarMod.copy()
ch1CarDf = ch1CarDf[ch1CarDf['SCat'].isin(set(carCats))]
ch1PlnDf = dfSrcPlnMod.copy()
ch1PlnDf = ch1PlnDf[ch1PlnDf['SCat'].isin(set(plnCats))]

chr1 = go.Figure()
chr1.add_trace(go.Bar(x=ch1PlnDf.index, y=ch1PlnDf['Eff'], 
                        name='Airplanes', marker=dict(line=dict(width=0),
                                                      color=clrs[0])))
chr1.add_trace(go.Bar(x=ch1CarDf.index, y=ch1CarDf['Eff'], 
                        name='Automobiles', marker=dict(line=dict(width=0),
                                                        color=clrs[1])))
chr1.update_xaxes(showticklabels=False, categoryorder='total descending')
chr1.update_yaxes(ticksuffix='  ', tickformat='.1f')
chr1.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                     plot_bgcolor='rgba(0,0,0,0)',
                     bargap=0, bargroupgap=0, barmode='stack',
                     margin=dict(l=0, r=0, t=0, b=0),
                     legend=dict(orientation='h', xanchor='right', x=.99, 
                                 yanchor='top', y=.99),
                     height=300)

st.plotly_chart(chr1, use_container_width=True)
with st.expander('See data sources'):
    st.markdown('* *All airline fuel economy metrics from various sources via ' + 
                '[wikipedia](https://en.m.wikipedia.org/wiki/Fuel_economy_in_aircraft)' +
                ', assumes that fuel use per flight is constant regardless of '+
                'passenger load;*')
    st.markdown('* *All car fuel economy metrics from the Government ' + 
                'of Canada 2022 [fuel economy database](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64)' +
                ', assumes that fuel use per trip is constant regardless of number ' +
                'of passengers, based on highway mileage ratings*')
    st.markdown('* *When there are multiple configurations of a automobile or ' + 
                'airplane model, the average fuel economy is used*')
    
st.markdown('#### Compare a flight with a road trip')

colB1, colB2 = st.columns(2)

with colB1:
    st.image('car.png')
    st.markdown('##### Car selection')
    inCarSCatPick = st.selectbox(label='Select the category of automobile',
                                 options=dfSrcCarMod['SCat'].unique(),
                                 index=1)
    inCarModelPick = st.selectbox(label='Select the specific automobile',
                                  options = dfSrcCarMod[dfSrcCarMod['SCat']==inCarSCatPick].index.unique(),
                                  index=0)
with colB2:
    st.image('airplane.png')
    st.markdown('##### Airplane selection')
    inPlnSCatPick = st.selectbox(label='Select the type of flight',
                                 options=dfSrcPlnMod['SCat'].unique(),
                                 index=2)
    inPlnModelPick = st.selectbox(label='Select the specific airplane',
                                  options = sorted(dfSrcPlnMod[dfSrcPlnMod['SCat']==inPlnSCatPick].index.unique()),
                                  index=0)

#%% build relavant charts
distance = dfSrcPlnMod[dfSrcPlnMod.index==inPlnModelPick]['Sector'].mean()
effPln = dfSrcPlnMod[dfSrcPlnMod.index==inPlnModelPick]['Eff'].mean()
effCar = dfSrcCarMod[dfSrcCarMod.index==inCarModelPick]['Eff'].mean()

# charts comparing distances travelled
chr2 = make_subplots(rows=1, cols=2)
chr2.add_trace(go.Bar(x=[distance],
                      marker=dict(color=clrs[1]),
                      hovertemplate='%{x:,.0f}km',
                      texttemplate='%{x:,.0f}km',
                      cliponaxis=False,
                      textposition='outside',
                      name=inCarModelPick), row=1, col=1,)
chr2.add_trace(go.Bar(x=[distance],
                      marker=dict(color=clrs[0]),
                      hovertemplate='%{x:,.0f}km',
                      texttemplate='%{x:,.0f}km',
                      cliponaxis=False,
                      textposition='outside',
                      name=inPlnModelPick), row=1, col=2)
chr2.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                   plot_bgcolor='rgba(0,0,0,0)',
                   margin=dict(l=0, r=40, t=0, b=0),
                   height=50, showlegend=False)
chr2.update_xaxes(visible=False)
chr2.update_yaxes(visible=False)

# charts comparing fuel burned
chr3 = make_subplots(rows=2, cols=1, shared_xaxes=True)
chr3.add_trace(go.Bar(x=[(distance/100)*effCar],
                      marker=dict(color=clrs[1]),
                      hovertemplate='%{x:,.0f}L',
                      texttemplate='%{x:,.0f}L',
                      cliponaxis=False,
                      textposition='outside',
                      name=inCarModelPick), row=1, col=1,)
chr3.add_trace(go.Bar(x=[(distance/100)*effPln],
                      marker=dict(color=clrs[0]),
                      hovertemplate='%{x:,.0f}L',
                      texttemplate='%{x:,.0f}L',
                      cliponaxis=False,
                      textposition='outside',
                      name=inPlnModelPick), row=2, col=1)
chr3.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                   plot_bgcolor='rgba(0,0,0,0)',
                   margin=dict(l=0, r=40, t=0, b=0),
                   height=50, showlegend=False)
chr3.update_xaxes(visible=False)
chr3.update_yaxes(visible=False)
    
st.markdown('##### Distance travelled *(based on selected plane distance)*')
st.plotly_chart(chr2, use_container_width=True, config=mbOff)
st.markdown('##### Fuel consumed per passenger')
st.plotly_chart(chr3, use_container_width=True, config=mbOff)