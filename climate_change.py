import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()

#! data manipulation

country = pd.read_csv('Climate_Change_Dash/Data_climate/GlobalLandTemperaturesByCountry.csv')
majorcity = pd.read_csv('Climate_Change_Dash/Data_climate/GlobalLandTemperaturesByMajorCity.csv')
state = pd.read_csv('Climate_Change_Dash/Data_climate/GlobalLandTemperaturesByState.csv')
globe = pd.read_csv('Climate_Change_Dash/Data_climate/GlobalTemperatures.csv')
CO2 = pd.read_csv('Climate_Change_Dash/Data_climate/global_co2_emissions_per_capita.csv')

#* unique country name to for dropdown loop
country_name = country.Country.unique().tolist()
majorcity_name = majorcity.City.unique().tolist()
state_name = state.State.unique().tolist()

#* it doesn't make sense to visualize temp throughout all the time. The seasonality is confusing and making my graphs not straightforward
# this is global years
years = np.unique(globe['dt'].apply(lambda x: x[:4])) # the first four characters 

mean_temp_globe = []
for year in years: 
    mean_temp_globe.append(globe[globe['dt'].apply(lambda x: x[:4]) == year]['LandAverageTemperature'].mean()) # average all temperatures in the same year 

# prepare data for plotly graph of global average temperature

data_global = go.Scatter(x = years, 
                        y = mean_temp_globe,
                        name='Average Temperature',
                        line=dict(color='rgb(199, 121, 093)')
                        )
# prepare co2 emission data for future visualization
years_co2 = CO2['date'].tolist()
Emission = CO2['Global CO2 Emissions per Capita'].tolist()
data_co2 = go.Scatter(x = years_co2, 
                        y = Emission,
                        name='Global CO2 Emission per capita',
                        line=dict(color='rgb(199, 121, 093)')
                        )

#! layout
app.layout = html.Div([
    # Main title
    html.H1('Climate Change Data Analysis', style = {'textAlign': 'center'}), #css
    # dividing into tabs
    dcc.Tabs(id = 'tabs', children = [
        # Defining the layout of the first Tab
        dcc.Tab(label = 'Local', children = [
            html.Div([
                dcc.Markdown(''' This is my CS 106 Project at Calvin University, proving the global warming trend.'''),
                  
                #! Country
                html.H1('Temperature VS Country', style = {'textAlign': 'center'}),
                #FIRST dropdown. Country
                dcc.Dropdown(id = 'my-dropdown1', # used to connect with callback
                            options=[{'label': i, 'value': i} for i in country_name],     # label is what user sees; value is what I work with inside dash code
                            multi=True,value=['China'], #value is default value
                            style = {"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id = 'Temp_country'),
                #! State
                html.H1('Temperature VS State', style = {'textAlign': 'center'}),
                #Second dropdown. State
                dcc.Dropdown(id = 'my-dropdown2', # used to connect with callback
                            options=[{'label': i, 'value': i} for i in state_name],     # label is what user sees; value is what I work with inside dash code
                            multi=True,value=['Acre'], #value is default value
                            style = {"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id = 'Temp_state'),
                #! Major City 
                html.H1('Temperature VS Major City', style = {'textAlign': 'center'}),
                #Third dropdown. City
                dcc.Dropdown(id = 'my-dropdown3', # used to connect with callback
                            options=[{'label': i, 'value': i} for i in majorcity_name],     # label is what user sees; value is what I work with inside dash code
                            multi=True,value=['Abidjan'], #value is default value
                            style = {"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id = 'Temp_City'),
            ]) # html.div 
        ]), # dcc.tab1
        #! Second tab for CO2 emission
        #* this one does not have to be interactive. Simple two ploty graphs
        dcc.Tab(label = "Global", children = [
            html.Div([
                html.H1("Climate Change on a Global Perspective", style={"textAlign": "center"}),
                dcc.Graph(id = "Temp_globe",
                        figure = {'data': [data_global],
                                'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                                                    '#FF7400', '#FFF400', '#FF0056'],
                                                    height=600,
                                                    title=f"Global Temperature Over Time",
                                                    xaxis={"title":"Year"},
                                                    yaxis={"title":"Temperature(Celsius)"}
                                                    )
                                }
                        ),
                dcc.Graph(id = 'CO2_Emission',
                        figure = {'data': [data_co2],
                                'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                                                    '#FF7400', '#FFF400', '#FF0056'],
                                                    height=600,
                                                    title=f"Global CO2 Emission Over Time",
                                                    xaxis={"title":"Year"},
                                                    yaxis={"title":"Global CO2 Emission per capita"}
                                                    )
                        }
                )
            ])# html.Div for dcc.tab2
        ]) # dcc.tab2
    ]) # dcc.tabs
]) #html.div

#! Interactive part


@app.callback(Output('Temp_country', 'figure'),
              [Input('my-dropdown1', 'value')])  
#! Country
def update_graph(selected_dropdown):
    dropdown = dict(zip(country_name, country_name))
    trace_1 = []

    for c in selected_dropdown:
        trace_1.append(
            go.Scatter(
                x = country[country['Country'] == c]['dt'],
                y = country[country['Country'] == c]['AverageTemperature'],  
                mode = 'lines', opacity = 0.7,
                name = f'Temperature of {dropdown[c]}',
                textposition = 'bottom center'
            )
        )
    traces = [trace_1]
    data = [val for sublist in traces for val in sublist] # flattening. Cited from https://towardsdatascience.com/interactive-dashboards-for-data-science-51aa038279e5
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"Temperature of {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
            yaxis={"title":"Temperature(Celsius)"})}
    return figure

#! State
@app.callback(Output('Temp_state', 'figure'),
              [Input('my-dropdown2', 'value')]) 
def update_graph(selected_dropdown):
    dropdown = dict(zip(state_name, state_name))
    trace_1 = [] # simply a randomly named list for to contain future data

    for c in selected_dropdown:
        trace_1.append(
            go.Scatter(
                x = state[state['State'] == c]['dt'],
                y = state[state['State'] == c]['AverageTemperature'],  # thinking if I should use autorange
                mode = 'lines', opacity = 0.7,
                name = f'Temperature of {dropdown[c]}', # so that title would change as I add more countries
                textposition = 'bottom center'
            )
        )
    traces = [trace_1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"Temperature of {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Temperature(Celsius)"})}
    return figure

#! City
@app.callback(Output('Temp_City', 'figure'),
              [Input('my-dropdown3', 'value')]) 
def update_graph(selected_dropdown):
    dropdown = dict(zip(majorcity_name, majorcity_name))
    trace_1 = []

    for c in selected_dropdown:
        trace_1.append(
            go.Scatter(
                x = majorcity[majorcity['City'] == c]['dt'],
                y = majorcity[majorcity['City'] == c]['AverageTemperature'],  # thinking if I should use autorange
                mode = 'lines', opacity = 0.7,
                name = f'Temperature of {dropdown[c]}',
                textposition = 'bottom center'
            )
        )
    traces = [trace_1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"Temperature of {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   #'rangeslider': {'visible': True}, 'type': 'date'
                   },
             yaxis={"title":"Temperature(Celsius)"})}
    return figure




if __name__ == "__main__":
    app.run_server(debug=True)