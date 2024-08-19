import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the plot style
sns.set(style="whitegrid")

# Load the CSV files into pandas DataFrames
calendar = pd.read_csv('calendar.csv')
sales_train_evaluation = pd.read_csv('sales_train_evaluation.csv')
sales_train_validation = pd.read_csv('sales_train_validation.csv')
sample_submission = pd.read_csv('sample_submission.csv')
sell_prices = pd.read_csv('sell_prices.csv')

# Display the first few rows of each DataFrame to understand their structure
print(calendar.head())
print(sales_train_evaluation.head())
print(sales_train_validation.head())
print(sample_submission.head())
print(sell_prices.head())

# Check the shape of the data
print("Calendar shape:", calendar.shape)
print("Sales Train Evaluation shape:", sales_train_evaluation.shape)
print("Sales Train Validation shape:", sales_train_validation.shape)
print("Sell Prices shape:", sell_prices.shape)

# Get basic statistics of the data
print(sales_train_evaluation.describe())
print(sell_prices.describe())



total_sales = sales_train_evaluation.iloc[:, 6:].sum(axis=0)

# Extract dates from the calendar
dates = calendar[calendar['d'].isin(sales_train_evaluation.columns[6:])]['date']

# Plotting total sales over time
plt.figure(figsize=(14, 6))
plt.plot(dates, total_sales)
plt.title('Total Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')

# Modify x-ticks to reduce noise
plt.xticks(rotation=45, ha='right', fontsize=8)

# Set x-ticks to show fewer dates by using a step
plt.xticks(range(0, len(dates), max(1, len(dates) // 15)), dates[::max(1, len(dates) // 15)])

plt.grid(True)
plt.tight_layout()
plt.show()


# Plotting the distribution of sell prices
plt.figure(figsize=(10, 6))
sns.histplot(sell_prices['sell_price'], bins=50, kde=True)
plt.title('Distribution of Sell Prices')
plt.xlabel('Sell Price')
plt.ylabel('Frequency')
plt.show()

# Group by state and sum sales
state_sales = sales_train_evaluation.groupby('state_id').sum().iloc[:, 6:].sum(axis=1)

# Plotting sales by state
plt.figure(figsize=(10, 6))
state_sales.plot(kind='bar')
plt.title('Total Sales by State')
plt.xlabel('State')
plt.ylabel('Total Sales')
plt.show()


# Group by category and sum sales
category_sales = sales_train_evaluation.groupby('cat_id').sum().iloc[:, 6:].sum(axis=1)

# Plotting sales by category
plt.figure(figsize=(10, 6))
category_sales.plot(kind='bar')
plt.title('Total Sales by Product Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')

# Rotate the x-ticks labels for better visibility and adjust the layout
plt.xticks(rotation=0)  # Rotates labels by 0 degrees (you can adjust the angle as needed)
plt.tight_layout()  # Automatically adjusts subplot params to give specified padding

plt.show()


# Reduce the number of days for demonstration (e.g., d_1 to d_100)
cols_to_keep = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'] + [f'd_{i}' for i in range(1, 101)]
reduced_sales = sales_train_evaluation[cols_to_keep]

# Now melt the reduced sales data
melted_sales = reduced_sales.melt(id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'], 
                                  var_name='d', 
                                  value_name='sales')


# Merge with calendar
sales_and_calendar = pd.merge(melted_sales, calendar, on='d')

# Aggregate sales by event name
event_sales = sales_and_calendar.groupby('event_name_1').sum()['sales']

# Plotting sales by event
plt.figure(figsize=(12, 6))
event_sales.sort_values(ascending=False).plot(kind='bar')
plt.title('Total Sales by Event')
plt.xlabel('Event Name')
plt.ylabel('Total Sales')

# Rotate the x-ticks labels for better visibility and adjust the layout
plt.xticks(rotation=45, ha='right')  # Rotate labels by 45 degrees and align them to the right
plt.tight_layout()  # Automatically adjusts subplot params to give specified padding

plt.show()