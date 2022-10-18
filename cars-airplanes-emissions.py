# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

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

st.set_page_config(page_title='Emissions: Planes vs. Automobiles', 
                   page_icon='favicon.png',
                   layout='wide',
                   menu_items={'About': ('Emissions: Planes vs. Automobiles' +
                                         '\nApp Contact: [Jamie Wilkie](mailto:jamie.wilkie@marqueegroup.ca)')})

appDetails = """
Created by: [Jamie Wilkie](https://www.linkedin.com/in/jamiewilkiecfa/) \n
Date: October 17, 2022 \n
Purpose: Compare the fuel efficiency of automobiles & airplanes under various assumptions based on publicly available information
"""
with st.expander('See app info:'):
    st.write(appDetails)

st.markdown('# Planes and automobiles: which is worse for emissions?')
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
chr1.update_xaxes(showticklabels=False, categoryorder='total descending',
                  fixedrange=True)
chr1.update_yaxes(ticksuffix='  ', tickformat='.1f', fixedrange=True)
chr1.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                     plot_bgcolor='rgba(0,0,0,0)',
                     bargap=0, bargroupgap=0, barmode='stack',
                     margin=dict(l=0, r=0, t=0, b=0),
                     legend=dict(orientation='h', xanchor='right', x=.99, 
                                 yanchor='top', y=.99),
                     height=300)

st.plotly_chart(chr1, use_container_width=True, config=mbOff)

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
plnPic = Image.open('airplane.png')
carPic = Image.open('car.png')

# charts comparing distances travelled
chr2 = go.Figure()
chr2.add_trace(go.Bar(x=[distance + 0.0001],
                      y=['Plane'], orientation='h',
                      marker=dict(color=clrs[0]),
                      hovertemplate='%{x:,.0f} km',
                      texttemplate='%{x:,.0f} km',
                      cliponaxis=False,
                      textposition='outside',
                      name=inCarModelPick))
chr2.add_trace(go.Bar(x=[distance],
                      y=['Car'], orientation='h',
                      marker=dict(color=clrs[1]),
                      hovertemplate='%{x:,.0f} km',
                      texttemplate='%{x:,.0f} km',
                      cliponaxis=False,
                      textposition='outside',
                      name=inPlnModelPick))

# charts comparing fuel burned
chr3 = go.Figure()
chr3.add_trace(go.Bar(x=[(distance/100)*effPln],
                      y=['Plane'], orientation='h',
                      marker=dict(color=clrs[0]),
                      hovertemplate='%{x:,.0f} L',
                      texttemplate='%{x:,.0f} L',
                      cliponaxis=False,
                      textposition='outside',
                      name=inPlnModelPick))
chr3.add_trace(go.Bar(x=[(distance/100)*effCar],
                      y=['Car'], orientation='h',
                      marker=dict(color=clrs[1]),
                      hovertemplate='%{x:,.0f} L',
                      texttemplate='%{x:,.0f} L',
                      cliponaxis=False,
                      textposition='outside',
                      name=inCarModelPick))
    
# charts comparing GHG emissions
chr4 = go.Figure()
chr4.add_trace(go.Bar(x=[(distance/100)*effPln*2.5],
                      y=['Plane'], orientation='h',
                      marker=dict(color=clrs[0]),
                      hovertemplate='%{x:,.0f} kg',
                      texttemplate='%{x:,.0f} kg',
                      cliponaxis=False,
                      textposition='outside',
                      name=inPlnModelPick))
chr4.add_trace(go.Bar(x=[(distance/100)*effCar*2.3],
                      y=['Car'], orientation='h',
                      marker=dict(color=clrs[1]),
                      hovertemplate='%{x:,.0f} kg',
                      texttemplate='%{x:,.0f} kg',
                      cliponaxis=False,
                      textposition='outside',
                      name=inCarModelPick))

# charts comparing time spent
chr5 = go.Figure()
chr5.add_trace(go.Bar(x=[(distance/850)+2+1],
                      y=['Plane'], orientation='h',
                      marker=dict(color=clrs[0]),
                      hovertemplate='%{x:,.0f} hrs',
                      texttemplate='%{x:,.0f} hrs',
                      cliponaxis=False,
                      textposition='outside',
                      name=inPlnModelPick))
chr5.add_trace(go.Bar(x=[(distance/90)],
                      y=['Car'], orientation='h',
                      marker=dict(color=clrs[1]),
                      hovertemplate='%{x:,.0f} hrs',
                      texttemplate='%{x:,.0f} hrs',
                      cliponaxis=False,
                      textposition='outside',
                      name=inCarModelPick))

for j in [chr2, chr3, chr4, chr5]:
    j.add_layout_image(dict(source=plnPic, 
                            xref='paper', yref='y', sizing='contain',
                            y='Plane', x=-0.015, sizex=1.5, sizey=1.5, layer='below',
                            xanchor='center', yanchor='middle'))
    j.add_layout_image(dict(source=carPic, 
                            xref='paper', yref='y', sizing='contain',
                            y='Car', x=-0.015, sizex=1.5, sizey=1.5, layer='below',
                            xanchor='center', yanchor='middle'))
    j.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=40, t=0, b=0),
                    height=50, showlegend=False)
    j.update_xaxes(visible=False, fixedrange=True)
    j.update_yaxes(visible=False, fixedrange=True)
    

st.markdown('##### Distance travelled *(based on selected plane distance)*')
st.plotly_chart(chr2, use_container_width=True, config=mbOff)
st.markdown('##### Fuel consumed per passenger')
st.plotly_chart(chr3, use_container_width=True, config=mbOff)
st.markdown('##### CO<sub>2</sub> per passenger', unsafe_allow_html=True)
st.plotly_chart(chr4, use_container_width=True, config=mbOff)
st.markdown('##### Hours of travel time')
st.plotly_chart(chr5, use_container_width=True, config=mbOff)
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
    st.markdown('* *CO<sub>2</sub> emissions per liter of fuel based on ' +
                'estimates from [ghgprotocol.org](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjJxJbm7ef6AhX1GDQIHZcND3wQFnoECDsQAQ&url=https%3A%2F%2Fghgprotocol.org%2Fsites%2Fdefault%2Ffiles%2FEmission_Factors_from_Cross_Sector_Tools_March_2017.xlsx&usg=AOvVaw1MOb4QhLTjmQSLtpFXIxFO)*',
                unsafe_allow_html=True)
    st.markdown('* *Air travel time assumes a cruise speed of 850km/h with 120 ' +
                'minutes for check-in, taxi & takeoff and 60 minutes for ' + 
                'landing, taxi and de-planing*')
    st.markdown('* *Automobile travel time assumes an average travel speed of ' + 
                '90km/h (including refuelling time, but assuming continuous travel)*')
    st.markdown('* *Code for data gathering and dashboard construction is ' + 
                'available at: https://github.com/jawook/cars-airplanes-emissions*')