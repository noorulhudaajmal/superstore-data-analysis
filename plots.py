import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

from utils import format_currency_label, add_state_code


def monthly_sales_and_profit(df):
    summed_data = df.groupby(['Month-Num', 'Month'])[['Sales', 'Profit']].sum().reset_index()
    summed_data = summed_data.sort_values(by='Month-Num')
    summed_data['Profit-Text'] = summed_data['Profit'].apply(format_currency_label)
    summed_data['Sales-Text'] = summed_data['Sales'].apply(format_currency_label)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=summed_data['Month'], y=summed_data['Sales'], mode="lines+markers+text",
            line=dict(color='#094780', width=4), marker=dict(color='#094780', size=12),
            text=summed_data['Sales-Text'], textposition="top center",
            fill='tozeroy', fillcolor="#00b4d8", name='Sales'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=summed_data['Month'], y=summed_data['Profit'], mode="lines+markers+text",
            line=dict(color='#c1121f', width=4), marker=dict(color='#c1121f', size=12),
            text=summed_data['Profit-Text'], textposition="top center",
            fill='tozeroy', fillcolor="#f4a261", name='Profit'
        )
    )

    fig.update_layout(
        title='<b>Monthly Sales and Profit</b>',
        xaxis_title='Month',
        yaxis_title='Sales & Profit ($)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
        legend=dict(orientation="h", xanchor='center', x=0.8, y=-0.15),
        height=400
    )

    return fig


def sales_map(df):
    sales_data = df.groupby('State')['Sales'].sum().reset_index()
    sales_data['State-Code'] = sales_data['State'].apply(add_state_code)

    # Create the choropleth map for State-level data
    fig = px.choropleth(
        sales_data,
        locations='State-Code',
        locationmode="USA-states",
        color='Sales',
        color_continuous_scale="sunset",
        scope="usa",
        labels={'Sales': 'Total Sales'},
        hover_name='State',
        hover_data={'State-Code': False, 'State': False, 'Sales': True},  # Control hover display
        title='<b>Sales by State in the USA</b>'
    )

    fig.update_layout(
        geo=dict(
            showcoastlines=True,
            projection_type='albers usa'
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
        height=550
    )

    return fig


def sales_by_region(df_filtered):
    # Aggregate data by region
    region_sales = df_filtered.groupby('Region')['Sales'].sum().reset_index()

    fig = go.Figure()

    # Add the Sales pie chart
    fig.add_trace(
        go.Pie(
            labels=region_sales['Region'],
            values=region_sales['Sales'],
            name="Sales",
            marker=dict(colors=['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']),
            hole=0.4
        )
    )

    # Update layout
    fig.update_layout(
        title_text="<b>Sales by Region</b>",
        showlegend=True,
        margin=dict(t=50),
        height=420
    )

    return fig


def sales_and_profit_wrt_categories(data):
    # Create a subplot with 2 rows
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=False,
                        vertical_spacing=0.15,
                        row_heights=[1, 3])

    # Upper chart: Sales and Profit by Category (Vertical Bars)
    categories = data.groupby('Category')[['Sales', 'Profit']].sum().reset_index()

    fig.add_trace(
        go.Bar(x=categories['Category'], y=categories['Sales'],
               name='Sales', marker_color='#264653'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=categories['Category'], y=categories['Profit'],
               name='Profit', marker_color='#2a9d8f'),
        row=1, col=1
    )

    # Bottom chart: Sales and Profit by Sub-Category (Horizontal Bars)
    sub_categories = data.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index()
    sub_categories.sort_values(by='Sales', ascending=True, inplace=True)

    fig.add_trace(
        go.Bar(y=sub_categories['Sub-Category'], x=sub_categories['Sales'],
               name='Sales', marker_color='#264653', orientation='h',
               showlegend=False),
        row=2, col=1
    )

    fig.add_trace(
        go.Bar(y=sub_categories['Sub-Category'], x=sub_categories['Profit'],
               name='Profit', marker_color='#2a9d8f', orientation='h',
               showlegend=False),
        row=2, col=1
    )

    fig.update_layout(
        height=900,
        showlegend=True,
        title_text="<b>Sales and Profit wrt Category and Sub-Category</b>",
        title_font=dict(size=20, color='#000000', family="Arial"),
        title_x=0.5,
        barmode='group',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
        legend=dict(orientation="h", xanchor='center', x=0.5, y=-0.15),
    )

    # Update x-axis and y-axis titles for the subplots
    fig.update_xaxes(title_text="Category", row=1, col=1)
    fig.update_yaxes(title_text="Total Sales and Profit", row=1, col=1)

    fig.update_xaxes(title_text="Total Sales and Profit", row=2, col=1)
    fig.update_yaxes(title_text="Sub-Category", row=2, col=1)

    return fig


def orders_by_segment(data):
    fig = make_subplots(rows=1, cols=2,
                        shared_xaxes=False,
                        vertical_spacing=0.15,
                        subplot_titles=("<b>Orders wrt Customer Segment</b>",
                                        "<b>Order Breakdown w.r.t Shipping Mode</b>"),
                        specs=[[{"type": "xy"}, {"type": "domain"}]]
                        )

    segment_orders = data.groupby('Segment')['Quantity'].sum().reset_index()

    fig.add_trace(
        go.Bar(x=segment_orders['Segment'], y=segment_orders['Quantity'], text=segment_orders['Quantity'],
               marker_color='#264653', name='Orders', showlegend=False),
        row=1, col=1
    )

    shipping_preference = data.groupby('Ship Mode')['Quantity'].sum().reset_index()

    fig.add_trace(
        go.Pie(labels=shipping_preference['Ship Mode'], values=shipping_preference['Quantity'],
               marker=dict(colors=['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']),
               name='Orders', hole=0.4),
        row=1, col=2
    )

    fig.update_layout(
        height=450,
        title_font=dict(size=20, color='#000000', family="Arial"),
        title_x=0.5,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
    )

    fig.update_yaxes(title_text="Order Qty", row=1, col=1)

    return fig


def top_customers(data):
    top_customers = data.groupby('Customer Name')['Quantity'].sum().reset_index()
    top_customers = top_customers.sort_values(by='Quantity', ascending=True).head(5)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(y=top_customers['Customer Name'], x=top_customers['Quantity'],
               name='Customer', marker_color='#2a9d8f', orientation='h',
               text=top_customers['Quantity'],
               showlegend=False),
    )

    fig.update_layout(
        title='<b>Top Customers</b>',
        xaxis_title='Ordered Quantity',
        yaxis_title='Customers Name',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
        height=420
    )

    return fig


