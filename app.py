import dash
import dash_core_components as dcc
#from dash_core_components.Dropdown import Dropdown
#from dash_core_components.RadioItems import RadioItems
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
from numpy.lib.function_base import select
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import os

# Data
#df = pd.read_csv(os.path.join(os.path.dirname(__file__), "ufc-master.csv"))
df = pd.read_csv('https://raw.githubusercontent.com/vickybwu/dash_ufc/main/ufc-master.csv')
df.sort_values(by=['date'], inplace=True)
df['Year'] = [date[-4:] for date in df['date']]



## Set up dropdown menus 
fight_options = []
title_fights = df[df['title_bout'] == True]

# change the winner column to the name of the winner
winners = []
for i in range(len(title_fights)):
    if title_fights['Winner'].iloc[i] == 'Red':
        winners.append(title_fights['R_fighter'].iloc[i])
    else:
        winners.append(title_fights['B_fighter'].iloc[i])
title_fights['Winner'] = winners

# ceate dropdown menu
for ft in title_fights.iterrows():
    display_label = str(ft[1][6] + ' ' + ft[1][0] + ' vs ' + ft[1][1])
    backend_label = ft[0] # The index of the selected row
    fight_options.append({'label': display_label, 'value': backend_label})

# subset data for the data table
title_fights_data_table = title_fights[['location', 'weight_class', 'gender', 'R_Stance', 'B_Stance', 'Winner']]
col_names = ['Location', 'Weight Class', 'Gender', 'Red Stance', 'Blue Stance', 'Winner']


# The App
app = dash.Dash()
app.title = 'Ultimate Fight Championship 2010-2021'
app.layout = html.Div(children = [
# H1 level title 
    html.Div(html.H1('Ultimate Fight Championship 2010-2021'),
            style={'color': 'black', 'fontFamily': 'Arial', 'fontSize': 18, 'textAlign': 'center'}),
# Line break   
    html.Hr(),
# HTML first graph description
    html.Div(html.H2('All Fights'),
            style={'color': 'firebrick', 'fontFamily': 'Arial', 'fontSize': 16, 'textAlign': 'center'}),

# Scatter plot and line Graph (first and second)
    html.Div([
        html.P('Select Gender'),
        dcc.RadioItems(id = 'radiobutton',
                        options = [{'label': 'Male', 'value': 'MALE'},
                                    {'label': 'Female', 'value': 'FEMALE'}],
                        value = 'FEMALE',
                        labelStyle={'display': 'inline-block'}),
        html.Hr(),
        html.H3('There are a total of 4588 UFC fights between 2010-2021, 4132 fights between male fighters and 456 fights between female fighters. See below chart for number of fights hosted each year for each weightclass'),
        dcc.Graph(id='scatter_plot'),
        html.Hr(),
        html.H3('The UFC money line bet allows you to place bets on a fighter for a selected fight. See below chart for average profit per hundred units bet each year for each weightclass'),
        dcc.Graph(id = 'line_graph'),
    ], style={'color': 'black', 'fontFamily': 'Arial', 'fontSize': 15}),


# HTML second graph  description
    html.Div(html.H2('Title Bouts'),
            style={'color': 'firebrick', 'fontFamily': 'Arial', 'fontSize': 16, 'textAlign': 'center'}),

# H3 header
    html.Hr(),
    html.H3('There are 233 title bouts between 2010-2021, 183 fights between male fighters and 40 fighter between female fighters. Select a title bout and see below charts for opponent fighter stats.'),

# Second graph Dropdown menu
    html.Div([
        html.P('Select A Fight'),
        dcc.Dropdown(id = 'title_fight_picker', 
                    options = fight_options , 
                    value = fight_options[0]['value'])
    ], style={'color': 'black', 'fontFamily': 'Arial', 'fontWeight': 'bold', 'fontSize': 15}),

# Data Table
    dt.DataTable(
            id='table_data_1',
            columns = [{"name": col_names[i], "id": title_fights_data_table.columns[i]} for i in range(len(col_names))],
            data=[],
            style_header={'backgroundColor': 'white','color': 'black', 'fontWeight': 'bold', 'fontSize': 15},
            style_data={'backgroundColor': 'white', 'color': 'black', 'fontSize': 15 }
            ),

# Second Graph 
    html.Div([
        dcc.Graph(id='bar_graph1'),
        html.Div(children = [
            dcc.Graph(id = 'small_multiples_1', 
                    style = {'width': 450, 'margin': 0, 'display': 'inline-block'}),
            dcc.Graph(id = 'small_multiples_2', 
                    style = {'width': 450, 'margin': 0, 'display': 'inline-block'}),
            dcc.Graph(id = 'small_multiples_3',
                    style = {'width': 450, 'margin': 0, 'display': 'inline-block'})
        ])
    ]),
])




# First Graph 
@app.callback(Output('scatter_plot', 'figure'),[Input('radiobutton', 'value')])
def first_graph(selected_gender):
    if selected_gender == 'FEMALE':
        colors = px.colors.sequential.Reds
    else:
        colors = px.colors.sequential.ice
    df_by_gender = df[df['gender'] == selected_gender]
    grouped = df_by_gender.groupby(['Year', 'weight_class']).size()
    grouped = pd.DataFrame(grouped)
    grouped.reset_index(inplace=True)
    grouped.rename(columns={0: "Count"}, inplace = True)
    fig = go.Figure()
    for i, wc in enumerate(grouped['weight_class'].unique()):
        grouped_by_wc = grouped[grouped['weight_class'] == wc]
        fig.add_trace(go.Scatter(
            x = grouped_by_wc['Year'],
            y = grouped_by_wc['Count'],
            mode = 'markers',
            marker={'size': 13, 'color': colors[-(i+1)]},
            opacity = 0.9,
            name = wc
        ))
    fig.update_layout(
        title = 'Total Fight Count per Weightclass 2010-2021',
        xaxis = {'title': 'Year', 'showgrid': False},
        yaxis = {'title': 'Count', 'showgrid': False}        
    )
    return fig

#linegraph
@app.callback(Output('line_graph', 'figure'),[Input('radiobutton', 'value')])
def line_graph(selected_gender):
    if selected_gender == 'FEMALE':
        colors = px.colors.sequential.Reds
    else:
        colors = px.colors.sequential.ice  
    df_by_gender = df[df['gender'] == selected_gender]  
    fig5 = go.Figure()
    for i, wc in enumerate(df_by_gender['weight_class'].unique()):
        df2 = df_by_gender[df_by_gender['weight_class'] == wc]
        R_ev = df2['R_ev'].groupby(df2['Year']).mean()
        B_ev = df2['B_ev'].groupby(df2['Year']).mean()
        fig5.add_trace(go.Line(
            x = df2['Year'].unique(),
            y = [(R_ev[i]+B_ev[i])/2 for i in range(len(B_ev))],
            marker_color = colors[-(i+1)],
            mode = 'lines+markers',
            opacity = 0.9,
            name = wc
        ))
    fig5.update_layout(title = 'Average profits per 100 units bet',
                    xaxis = {'title': 'Year', 'showgrid': False},
                    yaxis = {'title': 'Profits', 'showgrid': False})
    return fig5

# Data table
@app.callback(Output('table_data_1', 'data'), Input('title_fight_picker', 'value'))
def display_data_table(selected_fight):
    selected_fight = []+[selected_fight]
    return title_fights_data_table.loc[selected_fight].to_dict('records')


## Second Graph
@app.callback([Output('bar_graph1', 'figure'),
            Output('small_multiples_1', 'figure'),
            Output('small_multiples_2', 'figure'),
            Output('small_multiples_3', 'figure')],
            [Input('title_fight_picker', 'value')])
def display_fight_card(selected_fight):
    filtered_fight = title_fights.loc[selected_fight]

    figure1 = go.Figure()
    interested_columns = ['Significant Strikes Landed/Min', 'Average Submissions Attempted/15Mins', 
        'Average Takedowns Landed/15Mins']
    selected_fighters = [filtered_fight['R_fighter'], filtered_fight['B_fighter']]
    for i, fighter in enumerate(selected_fighters):
        if i == 0:
            attributes = ['R_avg_SIG_STR_landed', 'R_avg_SUB_ATT', 'R_avg_TD_landed']
            color = 'firebrick'
        else:
            attributes = ['B_avg_SIG_STR_landed', 'B_avg_SUB_ATT', 'B_avg_TD_landed']
            color = 'steelblue'
        figure1.add_trace(go.Bar(
            y = interested_columns,
            x = [filtered_fight[attri] for attri in attributes],
            orientation='h',
            opacity = 0.9,
            marker_color = color,
            name = fighter
        ))
    figure1.update_layout(
        title = 'Performance Statistics: '+ filtered_fight['R_fighter'] + ' vs. ' + filtered_fight['B_fighter'],
        yaxis = {'title': 'Technical Categories', 'showgrid': False},
        xaxis = {'title': 'Scores', 'showgrid': False}
    )
    #barplot for fighter heights
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(y = [filtered_fight['R_fighter'], filtered_fight['B_fighter']], 
                        x = [filtered_fight['R_Height_cms'], filtered_fight['B_Height_cms']], 
                        orientation='h',
                        marker_color = ['firebrick', 'steelblue'],
                        opacity = 0.9,
                        width = [0.2, 0.2]))
    fig2.update_layout(xaxis = {'title': 'Height (cm)', 'showgrid': False}, 
                    yaxis = {'title': None, 'showgrid': False})

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(y = [filtered_fight['R_fighter'], filtered_fight['B_fighter']], 
                        x = [filtered_fight['R_Weight_lbs'], filtered_fight['B_Weight_lbs']], 
                        orientation='h',
                        marker_color = ['firebrick', 'steelblue'],
                        opacity = 0.9,
                        width = [0.2, 0.2]))
    fig3.update_layout(xaxis = {'title': 'Weight (lbs)', 'showgrid': False}, 
                    yaxis = {'title': None, 'showgrid': False})

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(y = [filtered_fight['R_fighter'], filtered_fight['B_fighter']], 
                        x = [filtered_fight['R_Reach_cms'], filtered_fight['B_Reach_cms']], 
                        orientation='h',
                        marker_color = ['firebrick', 'steelblue'],
                        opacity = 0.9,
                        width = [0.2, 0.2]))
    fig4.update_layout(xaxis = {'title': 'Reach (cm)', 'showgrid': False}, 
                    yaxis = {'title': None, 'showgrid': False})

    return figure1, fig2, fig3, fig4

# Run App
server = app.server