import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('/Users/VickyWu/Desktop/datavizufc/ufc-master.csv')

app = dash.Dash()


# https://dash.plot.ly/dash-core-components/dropdown
# We need to construct a dictionary of dropdown values for the years
df['Year'] = [date[-4:] for date in df['date']]

year_options = []
for year in df['Year'].unique():
    year_options.append({'label':year,'value':year})

app.title = 'Ultimate Fights'
app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='year-picker',options=year_options,value=year_options[0])
])

@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])
def update_figure(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    traces = []
    for wc in filtered_df['weight_class'].unique():
        df_by_wc = filtered_df[filtered_df['weight_class'] == wc]
        traces.append(go.Scatter(
            x=df_by_wc['R_ev'],
            y=df_by_wc['B_ev'],
            text=df_by_wc[['R_fighter', 'B_fighter']],
            mode='markers',
            opacity=0.7,
            marker={'size': 12},
            name=wc
        ))
    figure = {'data': traces ,
        'layout': go.Layout(
        title = 'Profit on a 100 unit winning bet Red vs Blue',
        xaxis={'title': 'Profit on betting Red'},
        yaxis={'title': 'Profit on betting Blue'},
        hovermode='closest'
    )}

    return figure

if __name__ == '__main__':
    app.run_server()