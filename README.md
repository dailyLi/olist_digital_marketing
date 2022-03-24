# Olist Digital Marketing Analysis

Dashboard: https://dailyli.github.io/olist_digital_marketing/

## Objective
- To create visual reports on order number, sales, customer acquisition - see [EDA.ipynb](https://github.com/dailyLi/olist_digital_marketing/blob/main/EDA.ipynb)
- To make customer segmentation based on purchase behavior (RFM model) - see [Segmentation.ipynb](https://github.com/dailyLi/olist_digital_marketing/blob/main/Segmentation.ipynb)

## Background
The dataset was provided by Olist, the largest department store in Brazilian marketplaces. Olist connects small businesses from all over Brazil to channels without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners. See more on Olist website: www.olist.com

Business process: after a customer purchases the product from Olist Store a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments.

## Datasets
Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- orders: the core dataset. From each order you might find all other information
- customers: has information about the customer and its location. Use it to identify unique customers in the orders dataset and to find the orders delivery location
- payments: includes data about the orders payment options and payment amount
