import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk

# Set the plot style
sns.set(style="whitegrid")

# Load the CSV files into pandas DataFrames
calendar = pd.read_csv('calendar.csv')
sales_train_evaluation = pd.read_csv('sales_train_evaluation.csv')
sales_train_validation = pd.read_csv('sales_train_validation.csv')
sample_submission = pd.read_csv('sample_submission.csv')
sell_prices = pd.read_csv('sell_prices.csv')

# Functions for each plot

def plot_total_sales_over_time():
    total_sales = sales_train_evaluation.iloc[:, 6:].sum(axis=0)
    dates = calendar[calendar['d'].isin(sales_train_evaluation.columns[6:])]['date']
    
    plt.figure(figsize=(14, 6))
    plt.plot(dates, total_sales)
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.xticks(range(0, len(dates), max(1, len(dates) // 15)), dates[::max(1, len(dates) // 15)])
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_sell_price_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(sell_prices['sell_price'], bins=50, kde=True)
    plt.title('Distribution of Sell Prices')
    plt.xlabel('Sell Price')
    plt.ylabel('Frequency')
    plt.show()

def plot_sales_by_state():
    state_sales = sales_train_evaluation.groupby('state_id').sum().iloc[:, 6:].sum(axis=1)
    plt.figure(figsize=(10, 6))
    state_sales.plot(kind='bar')
    plt.title('Total Sales by State')
    plt.xlabel('State')
    plt.ylabel('Total Sales')
    plt.show()

def plot_sales_by_category():
    category_sales = sales_train_evaluation.groupby('cat_id').sum().iloc[:, 6:].sum(axis=1)
    plt.figure(figsize=(10, 6))
    category_sales.plot(kind='bar')
    plt.title('Total Sales by Product Category')
    plt.xlabel('Category')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def plot_sales_by_event():
    cols_to_keep = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'] + [f'd_{i}' for i in range(1, 101)]
    reduced_sales = sales_train_evaluation[cols_to_keep]
    melted_sales = reduced_sales.melt(id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'], 
                                      var_name='d', 
                                      value_name='sales')
    sales_and_calendar = pd.merge(melted_sales, calendar, on='d')
    event_sales = sales_and_calendar.groupby('event_name_1').sum()['sales']

    plt.figure(figsize=(12, 6))
    event_sales.sort_values(ascending=False).plot(kind='bar')
    plt.title('Total Sales by Event')
    plt.xlabel('Event Name')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Tkinter GUI setup
root = tk.Tk()
root.title("M5 Forecasting Challenge Plots")

# Creating buttons for each plot
button1 = ttk.Button(root, text="Total Sales Over Time", command=plot_total_sales_over_time)
button1.pack(pady=10)

button2 = ttk.Button(root, text="Sell Price Distribution", command=plot_sell_price_distribution)
button2.pack(pady=10)

button3 = ttk.Button(root, text="Sales by State", command=plot_sales_by_state)
button3.pack(pady=10)

button4 = ttk.Button(root, text="Sales by Product Category", command=plot_sales_by_category)
button4.pack(pady=10)

button5 = ttk.Button(root, text="Sales by Event", command=plot_sales_by_event)
button5.pack(pady=10)

root.mainloop()
