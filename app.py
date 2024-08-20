import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

from plots import monthly_sales_and_profit, sales_map, sales_and_profit_wrt_categories, \
    orders_by_segment, top_customers, sales_by_region
from utils import format_currency_label

# Load the dataset
df = pd.read_csv('data/Superstore Dataset.csv')

# Parse order date
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month-Num'] = df['Order Date'].dt.month
df['Month'] = df['Order Date'].dt.month_name()
df['Month-Year'] = df['Order Date'].dt.to_period('M')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                # external_scripts=['https://cdn.plot.ly/plotly-latest.min.js']
                )

# Define the tabs in a row component
tabs = dcc.Tabs(
    id='tabs',
    value='Overview',
    children=[
        dcc.Tab(label='Overview', value='Overview', className='custom-tab'),
        dcc.Tab(label='Sales by Geography', value='Sales by Geography', className='custom-tab'),
        dcc.Tab(label='Customer Segment Analysis', value='Customer Segment Analysis', className='custom-tab'),
        dcc.Tab(label='Product Performance', value='Product Performance', className='custom-tab'),
        dcc.Tab(label='Financial Analysis', value='Financial Analysis', className='custom-tab'),
    ],
    className='custom-tabs-container',
)

# Layout of the Dash app
app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Superstore Dashboard"))], className="header"),
    dbc.Row([tabs], className="mb-4"),
    # Year filter dropdown
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='year-filter',
            options=[{'label': year, 'value': year} for year in df['Year'].unique()],
            value=None,
            placeholder="Select Year",
            className="year-filter-dropdown"
        ), width=2, className="ml-auto"),
    ], justify='end'),
    dbc.Row([dbc.Col(html.Div(id='content'), width=12)]),

], fluid=True)

# Callback to update the content based on the selected tab
@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'value'),
     Input('year-filter', 'value')]
)
def render_content(tab, selected_year):
    if tab == 'Overview':
        if selected_year:
            df_filtered = df[df['Year'] == selected_year]
        else:
            df_filtered = df

        # Calculate KPIs
        total_sales = df_filtered['Sales'].sum()
        total_discount = df_filtered['Discount'].sum()
        total_profit = df_filtered['Profit'].sum()
        total_quantity = df_filtered['Quantity'].sum()
        monthly_sales_profit = monthly_sales_and_profit(df_filtered)
        categorical_sales_and_profit = sales_and_profit_wrt_categories(df_filtered)
        orders_analytics = orders_by_segment(df_filtered)

        return html.Div([
                # First row
                dbc.Row([
                    # First column in the first row
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(dbc.Card([
                                html.H2(format_currency_label(total_sales, prefix="$"),
                                        id='total-sales', className='card-title'),
                                html.P('Sales')
                            ], body=True, color='#2a9d8f', inverse=True), width=3),

                            dbc.Col(dbc.Card([
                                html.H2(format_currency_label(total_profit, prefix="$"),
                                        id='total-profit', className='card-title'),
                                html.P('Profit')
                            ], body=True, color='#e9c46a', inverse=True), width=3),

                            dbc.Col(dbc.Card([
                                html.H2(format_currency_label(total_discount),
                                        id='total-discount', className='card-title'),
                                html.P('Discount')
                            ], body=True, color='#f4a261', inverse=True), width=3),

                            dbc.Col(dbc.Card([
                                html.H2(format_currency_label(total_quantity),
                                        id='total-quantity', className='card-title'),
                                html.P('Total Quantities')
                            ], body=True, color='#e76f51', inverse=True), width=3),
                        ], className="mb-4"),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id='sales-profit-month-chart',
                                              figure=monthly_sales_profit,
                                              config={'displayModeBar': False}))
                        ]),
                    ], width=6),  # Adjust the width as needed

                    # Second column in the first row
                    dbc.Col(
                        dbc.Col(dcc.Graph(id='regional-sales-and-profit-chart',
                                          figure=sales_map(df_filtered),
                                          config={'displayModeBar': False}))
                        , width=6)  # Adjust the width as needed
                ]),

                # Second row
                dbc.Row([
                    dbc.Col([dcc.Graph(id="categorical-sales-sand-profit",
                                       figure=categorical_sales_and_profit,
                                       config={'displayModeBar': False})],
                            width=4),
                    dbc.Col([dbc.Row([dcc.Graph(id="order-analytics-chart",
                                       figure=orders_analytics,
                                       config={'displayModeBar': False})]),
                             dbc.Row([dbc.Col([dcc.Graph(id="discount-analytics-chart",
                                                figure=top_customers(df_filtered),
                                                config={'displayModeBar': False})],
                                     style={"margin-top": "15px"}),
                                      dbc.Col([dcc.Graph(id="sales-by-region-pie",
                                                         figure=sales_by_region(df_filtered),
                                                         config={'displayModeBar': False})],
                                              style={"margin-top": "15px"})
                                      ]),
                             ],
                            width=8)
                ], className="mb-2", style={"margin-top": "15px"})
            ])

    elif tab == 'Sales by Geography':
        return html.Div([html.H3('Sales by Geographic Segments')])
    elif tab == 'Customer Segment Analysis':
        return html.Div([html.H3('Customer Segment Analysis')])
    elif tab == 'Product Performance':
        return html.Div([html.H3('Product Performance')])
    elif tab == 'Financial Analysis':
        return html.Div([html.H3('Financial Analysis')])
    return html.Div([html.H3('Select a tab to see the content.')])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
