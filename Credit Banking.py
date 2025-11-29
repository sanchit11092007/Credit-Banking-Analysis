#📌 Credit Banking Project 
# Libraries import 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

#Load datasets 
Credit_Banking = pd.read_csv('Credit Banking_Project1.csv')
spend = pd.read_csv('spend.csv')
repay = pd.read_csv('repayment.csv')

#Display basic structure of datasets
print(Credit_Banking.head())
print(spend.head())
print(repay.head())

print(Credit_Banking.info())
print(spend.info())
print(repay.info())

#Summary of Customer Demographics 
print(Credit_Banking.describe())

#Replace invalid/ missing age values with mean age of valid customers (>18)
mean = Credit_Banking[(Credit_Banking['Age'] >= 18) & (Credit_Banking['Age'] <= 90)]['Age'].mean()
print(mean)

# Impute ages outside the 18-90 range with the calculated mean.
Credit_Banking.loc[(Credit_Banking['Age'] < 18) | (Credit_Banking['Age'] > 90), 'Age'] = mean 
print(Credit_Banking)

# Standardizing column names for merging consistency
repay.columns = ['SL No:', 'Customer', 'Month', 'Amount', 'Unnamed: 4']
spend.columns = ['Sl No:', 'Customer', 'Month', 'Type', 'Amount']

# Dropping unnecessary columns
spend.drop('Sl No:', axis = 1, inplace = True)
repay.drop('SL No:', axis = 1, inplace = True)
repay.drop('Unnamed: 4', axis = 1, inplace = True)

# Grouping and summing up the amounts
repayed = pd.DataFrame(repay.groupby('Customer')['Amount'].sum()).reset_index(drop = False)

spent = pd.DataFrame(spend.groupby('Customer')['Amount'].sum()).reset_index(drop = False)

print(repayed)
print(spent)
# Merging the datasets
merged = pd.merge(spent, repayed, on = 'Customer', how = 'inner')
print(merged)

merged.columns = [ 'Customer', 'spent', 'repayed']
print(merged)

# Calculating surplus and return
surplus = merged[merged['spent'] < merged['repayed']].copy()
surplus['difference'] = surplus['repayed'] - surplus['spent']
print(surplus)

surplus['return'] = ((surplus['difference']*2)/100)+surplus['difference']
print(surplus)

final_surplus = pd.DataFrame(surplus.groupby('Customer')['return'].sum())
final_surplus.reset_index(drop = False, inplace = True)
print(final_surplus)

# Converting month to datetime and period
spend['Date'] = pd.to_datetime(spend['Month'])

spend['Date'] = spend['Date'].dt.to_period('M')
spend['Date'] = spend['Date'].dt.to_timestamp()

print(spend)

monthly__spend = pd.DataFrame(spend.groupby(['Customer', 'Date'])['Amount'].sum()).reset_index(drop = False)
print(monthly__spend)

# Converting month to datetime and period
repay['Date'] = pd.to_datetime(repay['Month'])

repay['Date'] = repay['Date'].dt.to_period('M')

monthly_repay = pd.DataFrame(repay.groupby(['Customer', 'Date'])['Amount'].sum()).reset_index(drop = False)

print(monthly_repay)

# Grouping and summing up the amounts
max_spending = pd.DataFrame(spend.groupby(['Customer'])['Amount'].sum()).reset_index(drop =False)
max_spending.sort_values('Amount', ascending =False, inplace=True)
print(max_spending)

segment_max = pd.merge(max_spending,Credit_Banking[['Customer','Segment']],on='Customer',how='inner')
segment_max.drop('Customer',inplace=True,axis=1)
print(segment_max)

# The result of sort_values here is printed but not assigned, which is acceptable for a print statement.
print(segment_max.sort_values(by='Amount',ascending=False))

segment_max_final = pd.DataFrame(segment_max.groupby('Segment')['Amount'].sum()).reset_index(drop=False)

segment_max_final.sort_values('Amount',ascending=False, inplace=True)
print(segment_max_final)

# Bar Chart: Total spending by Segment 
plt.figure(figsize=(10,6))
plt.bar(segment_max_final['Segment'],segment_max_final['Amount'])
plt.xlabel('Segment',fontsize=12)
plt.ylabel('Amount',fontsize=12)
plt.title('Max Spending by Segment',fontsize=15)
plt.xticks(rotation=45,fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Pie Chart: Total spending by Segment 
plt.figure(figsize=(8,8))
plt.pie(
    segment_max_final['Amount'],
    labels=segment_max_final['Segment'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['red','green','blue','yellow','pink','orange']
)
plt.title('Max Spending by Segment',fontsize=15)
plt.show()

print(Credit_Banking['Age'].describe())

# Age Group Analysis 
bins = [18,36,54,72,90]
age_bins = pd.cut(Credit_Banking['Age'],bins=bins,labels=['A','B','C','D'])
print(age_bins.value_counts())
Credit_Banking['Age_Group'] = age_bins

# Age Wise Spending Analysis 
age_wise_spending = pd.merge(
    Credit_Banking[['Customer','Age','Age_Group']],
    max_spending,
    on='Customer',
    how='inner'
)
print(age_wise_spending)

# The result of sort_values here is assigned, which is correct.
age_wise_spending_group = age_wise_spending.sort_values('Amount',ascending=False)
print(age_wise_spending_group)



age_wise_spending_aggregated = pd.DataFrame(age_wise_spending.groupby('Age_Group')['Amount'].sum()).reset_index(drop=False)
age_wise_spending_aggregated.sort_values('Amount', ascending=False, inplace=True)


# Bar Chart: Age Wise Spending Analysis 
plt.figure(figsize=(10,6))
plt.bar(age_wise_spending_aggregated['Age_Group'],age_wise_spending_aggregated['Amount'])
plt.xlabel('Age Group',fontsize=12)
plt.ylabel('Amount',fontsize=12)
plt.title('Age Wise Spending Analysis',fontsize=15)
plt.xticks(rotation=45,fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Pie Chart: Age Wise Spending Analysis 
plt.figure(figsize=(8,8))
plt.pie(
    age_wise_spending_aggregated['Amount'],
    labels=age_wise_spending_aggregated['Age_Group'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['red','green','blue','yellow','pink','orange']
)
plt.title('Age Wise Spending Analysis',fontsize=15)
plt.show()

# Segment Expenditure Analysis 
segment_expenditure = pd.merge(Credit_Banking[['Customer','Segment']],max_spending,on='Customer',how='inner')
segment_expenditure = pd.merge(segment_expenditure, merged[['Customer', 'repayed']], on='Customer', how='inner')
print(segment_expenditure)

segment_expenditure['Difference'] = segment_expenditure['Amount'] - segment_expenditure['repayed']
print(segment_expenditure)

segment_expenditure_high = pd.DataFrame(segment_expenditure.groupby('Segment')['Difference'].sum()).reset_index(drop=False)
print(segment_expenditure_high)

# Transaction Category Analysis 
dict_map = {'Travel': ['AIR TICKET', 'BUS TICKET', 'BIKE', 'CAR', 'AUTO'],
            'Needs': ['FOOD', 'PETRO', 'CLOTHES', 'RENTAL'],
            'Shopping': ['SHOPPING', 'CAMERA', 'JEWELLERY', 'SANDALS', 'MOVIE TICKET']}

# Reverse Mapping 
new_map = {}
for key in dict_map:
    for val in dict_map[key]:
        new_map[val] = key

print(new_map)

spend['Category'] = spend['Type'].map(new_map)

category_wise_spending = pd.DataFrame(spend.groupby('Category')['Amount'].sum()).reset_index(drop=False)
print(category_wise_spending)

# Bar Chart: Category Wise Spending 
plt.figure(figsize=(10,6))
plt.bar(category_wise_spending['Category'],category_wise_spending['Amount'])
plt.xlabel('Category',fontsize=12)
plt.ylabel('Amount',fontsize=12)
plt.title('Category Wise Spending',fontsize=15)
plt.xticks(rotation=45,fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

spend_of_customer = pd.DataFrame(spend.groupby(['Customer', 'Month'])['Amount'].sum()).reset_index(drop = False)
repayment_of_customer = pd.DataFrame(repay.groupby(['Customer', 'Month'])['Amount'].sum()).reset_index(drop = False)

# Customer Monthly Expenses Analysis 
customer_merged_expenses = pd.merge(spend_of_customer, repayment_of_customer, on = ['Customer', 'Month'], how = 'inner')
customer_merged_expenses.rename(columns={'Amount_x': 'spent', 'Amount_y': 'repayed'}, inplace=True)

customer_merged_expenses['Date'] = pd.to_datetime(customer_merged_expenses['Month'])
customer_merged_expenses['Date'] = customer_merged_expenses['Date'].dt.to_period('M')
customer_merged_expenses['Difference'] = customer_merged_expenses['repayed'] - customer_merged_expenses['spent']
print(customer_merged_expenses)

monthly_profit = pd.DataFrame(customer_merged_expenses.groupby('Date')['Difference'].sum()).reset_index(drop = False)

monthly_profit.sort_values('Difference', ascending = False, inplace=True)
print(monthly_profit)

due_amount_of_customer = pd.DataFrame(customer_merged_expenses.groupby('Customer')['Difference'].sum()).reset_index(drop = False)
due_amount_of_customer.sort_values('Difference', ascending = False, inplace=True)
print(due_amount_of_customer)

top_customers = pd.concat([due_amount_of_customer.head(10), due_amount_of_customer.tail(10)])


# Bar Chart: Due amount per customer
plt.figure(figsize=(12, 6))
plt.bar(top_customers['Customer'], top_customers['Difference'], color=['green' if diff > 0 else 'red' for diff in top_customers['Difference']])

plt.xlabel('Customer', fontsize=10)
plt.ylabel('Net Financial Difference (Repaid - Spent)', fontsize=12)
plt.title('Top 10 Surplus and Top 10 Debt Customers', fontsize=14)
plt.xticks(rotation= 90, ha='right')
plt.tight_layout()
plt.show()