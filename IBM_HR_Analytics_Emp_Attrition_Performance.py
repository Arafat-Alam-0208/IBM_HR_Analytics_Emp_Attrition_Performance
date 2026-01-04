import pandas as pd
import numpy as np
from sqlalchemy import create_engine # To Import file to Sql Workbench
import pymysql

file_path = "/Users/mohammedarafat/major_project/IBM HR Analytics/WA_Fn-UseC_-HR-Employee-Attrition.csv"
def load_file(file_path):
    df = pd.read_csv(file_path)
    return df

df = load_file(file_path)
# print(df.shape) #. (1470, 35) 
print(df.columns.to_list())

# # check Null value in df
# print(df.isnull().sum()) # NO NULL Value in df 🥳 

# # Print columns
print(df.columns)


# 1️⃣ Attrition Overview
# What is the overall attrition rate in the company?
# What is attrition evenly distributed or concentrated in specific groups?

def attrition_overview(df):
    summary_list = []  # List to store all rows of the summary report
    # `YES` or `NO`value count
    count = df['Attrition'].value_counts()
    # print(f"\n{count}")

    # Percentage of Attrition Rate.
    percentage = df['Attrition'].value_counts(normalize=True) * 100
    # print(f"Percentage {percentage.round(2)}")

    # Attrition evenly distributed or concentrated 
    grouped_attrition  = df.groupby(['Department'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean().round(2) * 100) # left_pct = (Employees who left ÷ Total employees) × 100
    ]).reset_index()
    print(f"\n Grouped Attribute: \n{grouped_attrition}")

    ## Overall Attrition Rate
    overall_attrition_rate = (df['Attrition'].value_counts(normalize=True) * 100).round(2).reset_index()
    print(f"\n Overall Attrition Rate: {overall_attrition_rate}%")

    overall_attrition_rate.columns = ['segment', 'left_pct'] # rename columns & in segment we have Yes & No value.

    overall_attrition_rate['question'] = 'Overall Attrition Rate_%'
    overall_attrition_rate['dimension'] = 'Attriton_%'
    overall_attrition_rate['Total'] = None
    overall_attrition_rate['left'] = None
    
    summary_list.append(overall_attrition_rate[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    
    ## Add data into summary reprot
    grouped_attrition['question'] = 'Attrition Overview'
    grouped_attrition['dimension'] = 'Department'
    grouped_attrition.rename(columns={'Department': 'segment'}, inplace=True)

    summary_list.append(grouped_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # Combine all summaries into one DataFrame
    final_summary = pd.concat(summary_list, ignore_index=True)
    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary

attrition_overview(df)
# print(reuslt_attrition_overview)


# 2️⃣ Demographic-Based Questions
# Does attrition vary by age group?
# Is attrition higher among single vs married employees?
# Does gender show any noticeable pattern?

def Demographic_Based(df):
    summary_list = []  # List to store all rows of the summary report
    # attrition vary by age group
    age_attrition = df.groupby(['Age'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).round(2).reset_index()
    print(age_attrition[age_attrition['left_pct'] > 0].sort_values('left_pct', ascending=False).head(10))

    print('\n')

    # attrition higher among single vs married employees?
    MaritalStatus_attrition = pd.crosstab(df['MaritalStatus'], df['Attrition'])
    print(f"MaritalStatus_attrition: \n{MaritalStatus_attrition}") 

    marital_attrition = df.groupby(['MaritalStatus'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).round(2).reset_index()
    print(f"\n marital_attrition: \n{marital_attrition}")

    print('\n')

    # Attrition between age group like.: 18 to 30, 31 to 40, 40 to 50, 50 to 60
    # Create age group
    df['Age_Group'] = pd.cut(df['Age'], 
           bins= [18, 30, 40, 50, 60],
           labels=["18-30", "31-40", "41-50", "51-60"],
            ) # right=False. I remove bcz now it will take 18 to 30 if i will add 'right=False' then i have to write 18 to 29 
    
    # Analyze attrition by age group
    age_groups_attrition = df.groupby(['Age_Group'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).round(2).reset_index()
    print(f"Analyze attrition by age group: \n {age_groups_attrition}")
    

    print('\n')
    # Does gender show any noticeable pattern?
    gender_attrition = df.groupby(['Gender'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)

    print(f"Gender Attrition:\n {gender_attrition}")


    ## Add data into summary reprot
    # AGE INDIVIDUAL
    age_groups_attrition['question'] = 'Demographic-Based Attrition by Age Group'
    age_groups_attrition['dimension'] = 'Age_Group'
    age_groups_attrition.rename(columns={'Age_Group': 'segment'}, inplace=True)
    
    summary_list.append(age_groups_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    

    # GENDER
    gender_attrition['question'] = 'Attrition by Gender'
    gender_attrition['dimension'] = 'Gender'
    gender_attrition.rename(columns={'Gender': 'segment'}, inplace=True)
    
    summary_list.append(gender_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    

    # Merital Status
    marital_attrition['question'] = 'Attrition by Marital Status'
    marital_attrition['dimension'] = 'MaritalStatus'
    marital_attrition.rename(columns={'MaritalStatus': 'segment'}, inplace=True)

    summary_list.append(marital_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    
    
    # Combine all summaries into one DataFrame
    final_summary = pd.concat(summary_list, ignore_index=True)
    
    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary


# Demographic_Based(df)
Demographic_Based(df)


# 3️⃣ Job & Career Factors
# Which job roles have the highest attrition?
# Does job level impact attrition?
# Are new employees leaving more than experienced ones?


def Job_and_Career(df):
    summary_list = []  # List to store all rows of the summary report
    # Which job roles have the highest attrition?
    job_role_attrition = df.groupby(['JobRole'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().sort_values('left_pct', ascending=False).round(2)

    print(f"\n Job Roles highest attrition: \n {job_role_attrition}")

    print('\n')

    # Does job level impact attrition?
    job_level_attrition = df.groupby(['JobLevel'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().sort_values('left_pct', ascending=False).round(2)

    print(f"job_level_attrition: \n{job_level_attrition}")

    # Are new employees leaving more than experienced ones?
    # create Tenure
    df['Tenure_Group_YearsAtCompany'] = pd.cut(df['YearsAtCompany'], 
                                bins= [0, 1, 3, 5, 10, 40],
                                labels= ['<1 year', '1-3 years', '3-5 years', '5-10 years', '10+ years'],
                                right=False)

    # Attrition By Tenure
    emp_range_attrition = df.groupby(['Tenure_Group_YearsAtCompany'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().sort_values('left_pct', ascending=False).round(2)

    print(f"\n Attrition By Tenure: \n{emp_range_attrition}")

    print('\n')

    ## JobRole Tenure & Satisfaction
    job_role_tenure_satisfaction = df.groupby(['JobRole', 'JobSatisfaction', 'Tenure_Group_YearsAtCompany'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)   
    ]).reset_index().round(2)

    print(f"Job Role Tenure & Satisfaction:\n {job_role_tenure_satisfaction.sort_values('left_pct', ascending=False).head(10)}")

    # Job-Role summary for final report
    job_role_attrition['question'] = 'Job & Career - Attrition by Job Role'
    job_role_attrition['dimension'] = 'JobRole'
    job_role_attrition.rename(columns={'JobRole': 'segment'}, inplace=True)

    summary_list.append(job_role_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
            
    #job_level_attrition summary for final report
    job_level_attrition['question'] = 'Job & Career - Attrition by Job Level'
    job_level_attrition['dimension'] = 'JobLevel'
    job_level_attrition.rename(columns={'JobLevel': 'segment'}, inplace=True)

    summary_list.append(job_level_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # emp_range_attrition summary for final report
    emp_range_attrition['question'] = 'Job & Career - Attrition by Tenure Group'
    emp_range_attrition['dimension'] = 'Tenure_Group_YearsAtCompany'
    emp_range_attrition.rename(columns={'Tenure_Group_YearsAtCompany': 'segment'}, inplace=True)

    summary_list.append(emp_range_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    
    # job_role_tenure_satisfaction summary for final report
    job_role_tenure_satisfaction['question'] = 'Job & Career - Job Role, Tenure & Satisfaction vs Attrition'
    job_role_tenure_satisfaction['dimension'] = 'JobRole_Tenure_JobSatisfaction'
    job_role_tenure_satisfaction['segment'] = "Role: " + job_role_tenure_satisfaction['JobRole'].astype(str) + ' | ' + " Tenure: " + job_role_tenure_satisfaction['Tenure_Group_YearsAtCompany'].astype(str) + ' | ' + " JS: " + job_role_tenure_satisfaction['JobSatisfaction'].astype(str)

    summary_list.append(job_role_tenure_satisfaction[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    
    # Combine all summaries into one DataFrame
    print(f"Job Role Tenure & Satisfaction:\n {job_role_tenure_satisfaction.shape}")
    print(f"Job Role Tenure & Satisfaction:\n {job_role_tenure_satisfaction.head()}"
          )
    final_summary = pd.concat(summary_list, ignore_index=True)
    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary

Job_and_Career(df)


# 4️⃣ Compensation & Benefits
# Is attrition higher among lower-paid employees?
# Does salary hike percentage influence attrition?
# Is there a relationship between stock options and attrition?

def Compensation_and_Benefits(df):
    summary_list = []  # List to store all rows of the summary report
    emp_salary = []

    # MonthlyIncome = ACTUAL salary employee receives   <-- In DF 258 employees has higher MonthlyIncome which is invalid that's why no % of combing both MonthlyIncome and MonthlyRate
    # MonthlyRate = HOURLY/DAILY rate × hours (before deductions) 

    print('\n')
    print("="*60)
    print("ATTRITION BY SALARY LEVEL ANALYSIS")
    print("="*60)

    # Create Salary quartiles
    df['Salary_Quartiles'] = pd.qcut(df['MonthlyIncome'], q=4, labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)'])
    
    salary_quartiles_attrition = df.groupby(['Salary_Quartiles'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)

    salary_quartiles_attrition['question'] = 'Compensation & Benefits - Attrition by Salary Quartiles'
    salary_quartiles_attrition['dimension'] = 'Salary_Quartiles'
    salary_quartiles_attrition.rename(columns={'Salary_Quartiles': 'segment'}, inplace=True)

    summary_list.append(salary_quartiles_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    # print(salary_quartiles_attrition)

    # Does salary hike percentage influence attrition?
    print('\n')
    print("="*60)
    print("Salary hike percentage influence attrition ANALYSIS")
    print("="*60)

    df['Hike_Group'] = pd.cut(df['PercentSalaryHike'], bins=[0, 5, 10, 15, 20, 100], labels=['0-5%', '6-10%', '11-15%', '16-20%', '20%+'])

     # 2. Analyze attrition by hike group
    hike_analysis = df.groupby(['Hike_Group'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)
    
    hike_analysis['question'] = 'Compensation & Benefits - Does Salary hike percentage influence attrition'
    hike_analysis['dimension'] = 'Hike_Group'
    hike_analysis.rename(columns={'Hike_Group': 'segment'}, inplace=True)

    summary_list.append(hike_analysis[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    print("📊 ATTRITION BY SALARY HIKE PERCENTAGE:")
    print(hike_analysis)

    hike_0_5 = df.loc[df['Hike_Group'] == '20%+']
    print(hike_0_5[['Age', 'PercentSalaryHike', 'Attrition', 'MonthlyIncome']].head())


    print('\n')
    print("="*60)
    print("Do employees who receive company stock/equity leave less often? ANALYSIS")
    print("="*60)

    # Your direct analysis code
    stock_attrition = df.groupby('StockOptionLevel')['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2).sort_index()

    stock_attrition['question'] = 'Compensation & Benefits - Stock Option Level vs Attrition'
    stock_attrition['dimension'] = 'StockOptionLevel'
    stock_attrition.rename(columns={'StockOptionLevel': 'segment'}, inplace=True)

    summary_list.append(stock_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # print(stock_attrition)

    # Combine all summaries into one DataFrame
    final_summary = pd.concat(summary_list, ignore_index=True)

    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary

Compensation_and_Benefits(df)

# # Retrive the columns name contain `hike` , `increase` in dataframe.
hike_cols = [col for col in df.columns if 'satisfaction' in col.lower()] # or 
            #  'increase' in col.lower() or 'raise' in col.lower()]
print("Possible salary hike columns:", hike_cols)


# 5️⃣ Work-Life & Satisfaction
# Does overtime increase attrition?
# How do job satisfaction and work-life balance relate to attrition?
# Are employees with low environment satisfaction leaving more?

def Work_Life_and_Satisfaction(df):
    summary_list = []  # List to store all rows of the summary report

    print('\n')
    print("="*60)
    print("Does overtime increase attrition? ANALYSIS")
    print("="*60)
    overtime_attrition = df.groupby(['OverTime'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2).sort_index()

    overtime_attrition['question'] = 'Work-Life & Satisfaction - Does Overtime increase attrition'
    overtime_attrition['dimension'] = 'OverTime'
    overtime_attrition.rename(columns={'OverTime': 'segment'}, inplace=True)

    summary_list.append(overtime_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    # print(f"{overtime_attrition}")

    # How do job satisfaction and work-life balance relate to attrition?
    print('\n')
    print("="*60)
    print("Do unhappy or overworked employees leave more often? ANALYSIS")
    print("="*60)

    # 1. Analyze JobSatisfaction (Unhappiness)
    satisfaction_analysis = df.groupby(['JobSatisfaction'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)

    satisfaction_analysis['question'] = 'Work-Life & Satisfaction - Job Satisfaction vs Attrition'
    satisfaction_analysis['dimension'] = 'JobSatisfaction'
    satisfaction_analysis.rename(columns={'JobSatisfaction': 'segment'}, inplace=True)

    summary_list.append(satisfaction_analysis[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # 2. Analyze WorkLifeBalance
    worklife_balance = df.groupby(['WorkLifeBalance'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)

    worklife_balance['question'] = 'Work-Life & Satisfaction - Work Life Balance vs Attrition'
    worklife_balance['dimension'] = 'WorkLifeBalance'
    worklife_balance.rename(columns={'WorkLifeBalance': 'segment'}, inplace=True)

    summary_list.append(worklife_balance[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # print("\n1. UNHAPPINESS Analysis (Job Satisfaction):")
    # print(satisfaction_analysis.sort_values('left_pct', ascending=False))

    # print("\n2. OVERWORK Analysis (Work-Life Balance):")
    # print(worklife_balance.sort_values('left_pct', ascending=False))


    ## We will get the data about UnHappy & WLB is worst employee often Attrition.
    combined = df.groupby(['JobSatisfaction', 'WorkLifeBalance'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).round(2)
    
    print("\n1. UNHAPPINESS Analysis (Job Satisfaction): & OVERWORK Analysis (Work-Life Balance)")
    print(combined)

    # Are employees with low environment satisfaction leaving more?
    print('\n')
    print("="*60)
    print("Are employees with low environment satisfaction leaving more? ANALYSIS")
    print("="*60)

    EnvironmentSatisfaction_attrition = df.groupby(['EnvironmentSatisfaction'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)

    EnvironmentSatisfaction_attrition['question'] = 'Work-Life & Satisfaction - Environment Satisfaction vs Attrition'
    EnvironmentSatisfaction_attrition['dimension'] = 'EnvironmentSatisfaction'
    EnvironmentSatisfaction_attrition.rename(columns={'EnvironmentSatisfaction': 'segment'}, inplace=True)

    summary_list.append(EnvironmentSatisfaction_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])
    print(f"EnvironmentSatisfaction Attriton: \n{EnvironmentSatisfaction_attrition}")

    final_summary = pd.concat(summary_list, ignore_index=True)
    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary

Work_Life_and_Satisfaction(df)


# 6️⃣ Performance & Growth
# Are high performers leaving the company?
# Does promotion frequency affect attrition?
# Is attrition higher for employees with long time since last promotion?

def Performance_and_Growth(df):
    summary_list = []  # List to store all rows of the summary report
    # Are high performers leaving the company?
    PerformanceRating_attrition = df.groupby(['PerformanceRating', 'WorkLifeBalance'])['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)
    ## Higher & Average Performer are leaving, Even there Worklife are not balanced.
    # print(f"PerformanceRating Attriton: \n{PerformanceRating_attrition}")
    PerformanceRating_attrition['question'] = 'Performance & Growth - Performance Rating && WLB vs Attrition'
    PerformanceRating_attrition['dimension'] = 'PerformanceRating_WorkLifeBalance'
    PerformanceRating_attrition['segment'] = "PR: " + PerformanceRating_attrition['PerformanceRating'].astype(str) + ' | ' + " WLB: " + PerformanceRating_attrition['WorkLifeBalance'].astype(str)

    summary_list.append(PerformanceRating_attrition[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # Does promotion frequency affect attrition?
    print('\n')
    print("="*60)
    print("Do employees who get promoted more often stay longer (leave less), or do those who rarely get promoted leave more? ANALYSIS")
    print("="*60)
    
    promo_time_analysis = df.groupby('YearsSinceLastPromotion')['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2).sort_index()
    
    promo_time_analysis['question'] = 'Performance & Growth - Promotion Frequency vs Attrition'
    promo_time_analysis['dimension'] = 'YearsSinceLastPromotion'
    promo_time_analysis.rename(columns={'YearsSinceLastPromotion': 'segment'}, inplace=True)

    summary_list.append(promo_time_analysis[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    # Yes, more frequent promotions → lower attrition
    print("Time Since Last Promotion vs Attrition:")
    print(promo_time_analysis)

    # "Is attrition higher for employees with long time since last promotion?"
    # Answer:  Yes, longer time since promotion → higher attrition

    buckets = pd.cut(
    df['YearsSinceLastPromotion'],
    bins=[-1, 0, 1, 3, 5, 8, 20],  # Custom bins based on your pattern
    labels=[
        'Just Promoted (0 yrs)',
        '1 Year Since', 
        '2-3 Years Since',
        '4-5 Years Since',
        '6-8 Years Since',
        '9+ Years Since'
    ]
)

    # Group by these buckets
    bucket_analysis = df.groupby(buckets)['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ]).reset_index().round(2)

    bucket_analysis['question'] = 'Performance & Growth - Promotion Time Buckets vs Attrition'
    bucket_analysis['dimension'] = 'Promotion_Time_Buckets'
    bucket_analysis.rename(columns={buckets.name: 'segment'}, inplace=True)

    summary_list.append(bucket_analysis[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct']])

    print("Promotion Time Buckets vs Attrition:")
    print(bucket_analysis.sort_values('left_pct', ascending=False))
    # The Discrepancy Explained:
    # Individual years 9, 13, 15 have HIGH attrition (23.53%, 20%, 23.08%)
    # But years 10, 11, 12, 14 have LOW attrition (16.67%, 8.33%, 0%, 11.11%)

    # When you average them together in bucket "9+ Years", you get 14.61%

    final_summary =  pd.concat(summary_list, ignore_index=True)
    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary

Performance_and_Growth(df)



# 7️⃣ Managerial & Organizational Impact
# Are there managers or departments with unusually high attrition?
# Does distance from home influence attrition?
# Is attrition linked to training opportunities?

def Managerial_and_Organizational_Impact(df):
    summary_list = []  # List to store all rows of the summary report:
    print('\n')
    print("="*60)
    print("Which specific managers or departments are losing employees at alarmingly high rates compared to others? ANALYSIS")
    print("="*60)

    # Analyse department level Attriton.
    department_attrition = df.groupby('Department').agg({
    'Attrition': [
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ],
    'YearsAtCompany': [
        ('Avg_Tenure', 'mean')
    ],
    'JobSatisfaction': [
        ('Avg_Satisfaction', 'mean')
    ]
    }).round(2)


    # print(department_attrition)

    print("\n")
    
    JobRole_Manager_Attrition = df.groupby('JobRole').agg({
    'Attrition': [
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ],
    'YearsAtCompany': [
        ('Avg_Tenure', 'mean')
    ],
    'JobSatisfaction': [
        ('Avg_Satisfaction', 'mean')
    ]
    }).reset_index().round(2)

    managerRole = [role for role in JobRole_Manager_Attrition.index
                        if 'manager' in str(role).lower()]
    manager_analysis = JobRole_Manager_Attrition.loc[managerRole]

    # print(manager_analysis)

    # # Does distance from home influence attrition?
    print('\n')
    print("Does distance from home influence attrition? ANALYSIS")
    print("="*60)

    distance_from_home_attrition = df.groupby('DistanceFromHome').agg({
    'Attrition': [
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100)
    ],
    'YearsAtCompany': [
        ('Avg_Tenure', 'mean')
    ],
    'JobSatisfaction': [
        ('Avg_Satisfaction', 'mean')
    ]
    }).reset_index().round(2)

    # print(distance_from_home_attrition)

    # Create distance buckets
    df['Commute_Bucket'] = pd.cut(
        df['DistanceFromHome'],
        bins=[0, 5, 10, 15, 20, 30, 50],  # Custom bins
        labels=['Very Close (0-5 km)', 
                'Close (6-10 km)', 
                'Moderate (11-15 km)',
                'Far (16-20 km)',
                'Very Far (21-30 km)',
                'Extreme (31+ km)']
    )

    # Analyze by buckets
    commute_analysis = df.groupby('Commute_Bucket')['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100),
        ('Avg_Tenure', lambda x: df.loc[x.index, 'YearsAtCompany'].mean()),
        ('Avg_Satisfaction', lambda x: df.loc[x.index, 'JobSatisfaction'].mean())
    ]).reset_index().round(2).sort_values('left_pct', ascending=False)

    commute_analysis['question'] = 'Managerial & Organizational Impact - Commute Distance Buckets vs Attrition'
    commute_analysis['dimension'] = 'Commute_Bucket'
    commute_analysis.rename(columns={'Commute_Bucket': 'segment'}, inplace=True)

    summary_list.append(commute_analysis[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct', 'Avg_Tenure', 'Avg_Satisfaction']])

    print("Commute Distance Buckets vs Attrition:")
    print(commute_analysis)

    print('\n')
    print("Do employees who get more/fewer training opportunities leave more or less often? ANALYSIS")
    print("="*60)

    training_analysis = df.groupby('TrainingTimesLastYear')['Attrition'].agg([
        ('Total', 'count'),
        ('left', lambda x: (x == 'Yes').sum()),
        ('left_pct', lambda x: (x == 'Yes').mean() * 100),
        ('Avg_Satisfaction', lambda x: df.loc[x.index, 'JobSatisfaction'].mean()),
        ('Avg_Tenure', lambda x: df.loc[x.index, 'YearsAtCompany'].mean())
    ]).reset_index().round(2).sort_values('TrainingTimesLastYear')

    training_analysis['question'] = 'Managerial & Organizational Impact - Training Frequency vs Attrition'
    training_analysis['dimension'] = 'TrainingTimesLastYear'
    training_analysis.rename(columns={'TrainingTimesLastYear': 'segment'}, inplace=True)

    summary_list.append(training_analysis[['question', 'dimension', 'segment', 'Total', 'left', 'left_pct', 'Avg_Satisfaction', 'Avg_Tenure']])

    print("Training Frequency vs Attrition:")
    print(training_analysis)

    final_summary = pd.concat(summary_list, ignore_index=True)
    # Return a dictionary instead of a set because Series/DataFrame are unhashable
    return final_summary

Managerial_and_Organizational_Impact(df)

# Create final summary for ALL questions
final_summary = pd.concat([
    attrition_overview(df),
    Demographic_Based(df),
    Job_and_Career(df),
    Compensation_and_Benefits(df),
    Work_Life_and_Satisfaction(df),
    Performance_and_Growth(df),
    Managerial_and_Organizational_Impact(df)
], ignore_index=True)

# Optional but recommended safety step
final_summary = final_summary.drop_duplicates()

# Save to CSV (ready for Excel / Tableau)
# final_summary.to_csv("HR_Master_Summary.csv", index=False)
print("Final summary saved to HR_Master_Summary.csv")


# 8️⃣ Business Impact Thinking (VERY IMPORTANT)
# Which 3 factors appear to be the strongest drivers of attrition?
# If HR could fix only one thing, what should it be and why?
# Which employee group should HR focus on retaining first?

# # Which 3 factors appear to be the strongest drivers of attrition?


# summary_report placeholder (overall_attrition_rate not defined in this script)

# summary_rows = []


# | Column         | Meaning              |
# | -------------- | -------------------- |
# | `analysis_day` | Day1, Day2, etc      |
# | `question`     | Business question    |
# | `dimension`    | Age, JobRole, Gender |
# | `segment`      | 18–25, Sales, Male   |
# | `total`        | Total employees      |
# | `left`         | Employees left       |
# | `left_pct`     | Attrition %          |

# 'question',
# 'dimension',
# 'segment',
# 'total',
# 'left',
# 'left_pct'


# Database connection
# For MySQL
# engine = create_engine('mysql+pymysql://root:Alam0208$@localhost:3306/hr_analytics')

# For PostgreSQL
# engine = create_engine('postgresql+psycopg2://username:password@localhost:5432/your_database')

# Read CSV file
df = pd.read_csv('/Users/mohammedarafat/major_project/IBM HR Analytics/WA_Fn-UseC_-HR-Employee-Attrition.csv')

# Optional: Clean/transform data
# df.columns = df.columns.str.strip()  # Clean column names
# df = df.fillna('NULL')  # Handle missing values

# Insert data into SQL table
# Option 1: Replace existing data
# df.to_sql('hr_employee', engine, if_exists='replace', index=False)

# Option 2: Append to existing data
# df.to_sql('your_table_name', engine, if_exists='append', index=False)

print(f"Successfully loaded {len(df)} rows into database")


