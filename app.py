import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
from dash_core_components.RadioItems import RadioItems
import dash_html_components as html
from dash.dependencies import Input, Output
from numpy.lib.function_base import select
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import os

# Data
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "ufc-master.csv"))
df['Year'] = [date[-4:] for date in df['date']]



## Dropdown menus 
fight_options = []
title_fights = df[df['title_bout'] == True]
for ft in title_fights.iterrows():
    display_label = str(ft[1][6] + ' ' + ft[1][0] + ' vs ' + ft[1][1])
    backend_label = ft[0] # The index of the selected row
    fight_options.append({'label': display_label, 'value': backend_label})

# middle_line_graph
fig5 = go.Figure()
fig5.add_trace(go.Line(
                x = df['Year'].unique(),
                y = df['R_ev'].groupby(df['Year']).mean(),
                marker_color = 'firebrick',
                mode = 'lines+markers',
                opacity = 0.9,
                name = 'betting on red'
))
fig5.add_trace(go.Line(
                x = df['Year'].unique(),
                y = df['B_ev'].groupby(df['Year']).mean(),
                marker_color = 'steelblue',
                mode = 'lines+markers',
                opacity = 0.9,
                name = 'betting on blue'
))
fig5.update_layout(title = 'Average profits per 100 units bet',
                    xaxis = {'title': 'Year', 'showgrid': False},
                    yaxis = {'title': 'Profits', 'showgrid': False})

# The App
app = dash.Dash()
app.title = 'Ultimate Fight Championship'
app.layout = html.Div(children = [
# H1 level title 
    html.Div(html.H1('Ultimate Fight Championship 2010-2021'),
            style={'color': 'black', 'fontFamily': 'Arial', 'fontSize': 18, 'textAlign': 'center'}),
# Line break   
    html.Hr(),
# HTML first graph description
    html.Div(html.H2('Fight Overivew'),
            style={'color': 'firebrick', 'fontFamily': 'Arial', 'fontSize': 16, 'textAlign': 'center'}),

# First Graph
    html.Div([
        html.P('Select Gender'),
        dcc.RadioItems(id = 'radiobutton',
                        options = [{'label': 'Male', 'value': 'MALE'},
                                    {'label': 'Female', 'value': 'FEMALE'}],
                        value = 'FEMALE',
                        labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='scatter_plot'),
    ], style={'color': 'black', 'fontFamily': 'Arial', 'fontSize': 12}),



# Middle Graph
    html.Div([
        dcc.Graph(id = 'line_graph',
        figure = fig5)
    ]),


# HTML second graph  description
    html.Div(html.H2('Title Bouts'),
            style={'color': 'firebrick', 'fontFamily': 'Arial', 'fontSize': 16, 'textAlign': 'center'}),

# Second Graph 
    html.Div([
        html.P('Select A Fight'),
        dcc.Dropdown(id = 'title_fight_picker', 
                    options = fight_options , 
                    value = fight_options[0]['value']),
        dcc.Graph(id='bar_graph1'),
        html.Div(children = [
            dcc.Graph(id = 'small_multiples_1', 
                    style = {'width': 450, 'margin': 0, 'display': 'inline-block'}),
            dcc.Graph(id = 'small_multiples_2', 
                    style = {'width': 450, 'margin': 0, 'display': 'inline-block'}),
            dcc.Graph(id = 'small_multiples_3',
                    style = {'width': 450, 'margin': 0, 'display': 'inline-block'})
        ])
    ], style={'color': 'black', 'fontFamily': 'Arial', 'fontSize': 12}),
])




# First Graph 
@app.callback(Output('scatter_plot', 'figure'),[Input('radiobutton', 'value')])
def first_graph(selected_gender):
    if selected_gender == 'FEMALE':
        colors = px.colors.sequential.Reds
    else:
        colors = px.colors.sequential.Blues
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

## Second Graph
@app.callback([Output('bar_graph1', 'figure'),
            Output('small_multiples_1', 'figure'),
            Output('small_multiples_2', 'figure'),
            Output('small_multiples_3', 'figure')],
            [Input('title_fight_picker', 'value')])
def display_fight_card(selected_fight):
    filtered_fight = title_fights.loc[selected_fight]

    figure1 = go.Figure()
    interested_columns = ['Significant Strikes Landed/Min', 'Average Submissions Attempted/15Min', 
        'Average Takedowns Landed/15Min']
    selected_fighters = [filtered_fight['R_fighter'], filtered_fight['B_fighter']]
    for i, fighter in enumerate(selected_fighters):
        if i == 0:
            attributes = ['R_avg_SIG_STR_landed', 'R_avg_SUB_ATT', 'R_avg_TD_landed']
            color = 'firebrick'
        else:
            attributes = ['B_avg_SIG_STR_landed', 'B_avg_SUB_ATT', 'B_avg_TD_landed']
            color = 'steelblue'
        figure1.add_trace(go.Bar(
            x = interested_columns,
            y = [filtered_fight[attri] for attri in attributes],
            opacity = 0.9,
            marker_color = color,
            name = fighter
        ))
    figure1.update_layout(
        title = 'Performance Statistics: '+ filtered_fight['R_fighter'] + ' vs. ' + filtered_fight['B_fighter'],
        xaxis = {'title': 'Technical Categories', 'showgrid': False},
        yaxis = {'title': 'Scores', 'showgrid': False}
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