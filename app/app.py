from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import plotly.io as pio
#px.defaults.color_continuous_scale = px.colors.sequential.Sunset

pio.templates.default = 'plotly_dark'

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

markdown_text = '''
### Background

The dataset was provided by Olist, the largest department store in Brazilian marketplaces. Olist connects small businesses from all over Brazil to channels without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners. See more on Olist website: www.olist.com

Business process: after a customer purchases the product from Olist Store a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments.
'''

df = pd.read_csv("combined_data.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["first_order_date"] = pd.to_datetime(df["first_order_date"])

#daily order number

byDate = df.groupby([df['order_purchase_timestamp'].dt.date, "usertype"])["order_id"].count().reset_index()

fig_daily_order = px.line(byDate, x='order_purchase_timestamp', y='order_id', color='usertype',
                 labels={'order_purchase_timestamp':'Date', 'order_id':'Number of orders'}, height=500,
                 title='Order number by date')

#week hour heatmap

byWkdHr = df.groupby(["weekday", "hour"]).count()["order_id"].unstack()
fig_wkdhr = px.imshow(byWkdHr, text_auto=True, 
               title="Order number by day of the week and hour of the day")

#monthly revenue

byMonth_revenue = df.groupby([df['order_purchase_timestamp'].dt.to_period('M')])["payment_value"].sum().reset_index()
byMonth_revenue['order_purchase_timestamp'] = byMonth_revenue['order_purchase_timestamp'].astype('string')

fig_monthly_revenue = px.bar(byMonth_revenue, x='order_purchase_timestamp', y='payment_value', 
                text='payment_value', 
                labels={'order_purchase_timestamp':'Month', 'payment_value':'Revenue'}, height=500,
                title='Revenue by month')

#monthly revenue growth
byMonth_revenue['MonthlyGrowth'] = (byMonth_revenue['payment_value'].pct_change()*100).round(2)

fig_monthly_revenue_growth = px.line(byMonth_revenue, x='order_purchase_timestamp', y='MonthlyGrowth', 
                 text='MonthlyGrowth', height=500,
                 labels={'order_purchase_timestamp':'Month', 'MonthlyGrowth':'Growth rate in %'}, 
                 title='Revenue growth rate by month')


#monthly new customer
newCus = df.groupby([df['first_order_date'].dt.to_period('M')])['customer_unique_id'].count().reset_index()
newCus.columns = ['first_order_month','new_customer_count']
newCus['first_order_month'] = newCus['first_order_month'].astype('string')

fig_new_cus = px.bar(newCus, x='first_order_month', y='new_customer_count', text='new_customer_count',
              labels={'first_order_month':'Month', 'new_customer_count':'# of new customers'}, height=500,
              title='New customer number by month')

#fig_new_cus.update_layout(
#    plot_bgcolor=colors['background'],
#    paper_bgcolor=colors['background'],
#    font_color=colors['text']
#)

#monthly new customer growth rate
newCus['MonthlyGrowth'] = (newCus['new_customer_count'].pct_change()*100).round(2)

fig_monthly_cus_growth = px.line(newCus, x='first_order_month', y='MonthlyGrowth', 
                 text='MonthlyGrowth', height=500,
                 labels={'first_order_month':'Month', 'MonthlyGrowth':'Growth rate in %'}, 
                 title='New customer number growth rate by month')


app.layout = html.Div(style={'backgroundColor': colors['background']},
    children=[
    html.H1(
        children='Olist Data Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    dcc.Graph(
        id='daily_order',
        figure=fig_daily_order,
        style={
            'width':'80%',
            'display':'inline-block'
        }
    ),
    
    dcc.Graph(
        id='whdhr',
        figure=fig_wkdhr,
        style={
            'width':'80%',
            'display':'inline-block'
        }
    ),
    
    dcc.Graph(
        id='monthly_revenue',
        figure=fig_monthly_revenue,
        style={
            'width':'50%',
            'display':'inline-block'
        }        
    ),
    
    dcc.Graph(
        id='monthly_revenue_growth',
        figure=fig_monthly_revenue_growth,
        style={
            'width':'50%',
            'display':'inline-block'
        }        
    ),
    
    dcc.Graph(
        id='monthly_new_cus',
        figure=fig_new_cus,
        style={
            'width':'50%',
            'display':'inline-block'
        }        
    ),          
    
    dcc.Graph(
        id='monthly_cus_growth',
        figure=fig_monthly_cus_growth,
        style={
            'width':'50%',
            'display':'inline-block'
        }        
    )     
])

if __name__ == '__main__':
    app.run_server(debug=True)