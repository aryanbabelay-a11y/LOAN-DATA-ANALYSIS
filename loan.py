import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── 1. LOAD & INSPECT ─────────────────────────────────────────
df = pd.read_csv('D:/Applicant-details.csv')
print("Shape:", df.shape)
print(df.head(3))
print("\nNull values:\n", df.isnull().sum())
print("\nData types:\n", df.dtypes)

# Rename for convenience
df.rename(columns={'Vehicle_Ownership(car)': 'Vehicle_Ownership'}, inplace=True)

# ── 2. FEATURE ENGINEERING ────────────────────────────────────

# Age groups
df['Age_Group'] = pd.cut(df['Applicant_Age'],
                         bins=[0, 25, 35, 45, 55, 100],
                         labels=['<25', '25-35', '35-45', '45-55', '55+'])

# Income brackets
df['Income_Bracket'] = pd.cut(df['Annual_Income'],
                              bins=[0, 2500000, 5000000, 7500000, 10000000],
                              labels=['Low', 'Medium', 'High', 'Very High'])

# Stability score (combined experience feature)
df['Stability_Score'] = df['Years_in_Current_Employment'] + df['Years_in_Current_Residence']

print("\nDefault Rate Overall:", round(df['Loan_Default_Risk'].mean() * 100, 2), "%")
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df.columns

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:aryan@localhost:5432/postgres')
# Store DataFrame to SQL table
df.to_sql(
    name='applicants',        # Table name
    con=engine,             # Database connection
    if_exists='replace',    # Options: 'fail', 'replace', 'append'
    index=False             # Don't write DataFrame index as a column
)

# ── 3. DEFAULT RATE BY KEY CATEGORIES ────────────────────────

def plot_default_rate(col, title, figsize=(8, 4), color='steelblue'):
    rate = df.groupby(col)['Loan_Default_Risk'].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=figsize)
    rate.plot(kind='bar', color=color, edgecolor='black')
    plt.title(title)
    plt.ylabel('Default Rate (%)')
    plt.xlabel(col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_default_rate('House_Ownership',   'Default Rate by House Ownership',   color='coral')
plot_default_rate('Marital_Status',    'Default Rate by Marital Status',    color='mediumseagreen')
plot_default_rate('Vehicle_Ownership', 'Default Rate by Vehicle Ownership', color='mediumpurple')
plot_default_rate('Age_Group',         'Default Rate by Age Group',         color='dodgerblue')
plot_default_rate('Income_Bracket',    'Default Rate by Income Bracket',    color='tomato')

# ── 4. TOP OCCUPATIONS BY DEFAULT RATE ───────────────────────
plt.figure(figsize=(12, 5))
occ_default = (df.groupby('Occupation')['Loan_Default_Risk']
                 .mean()
                 .sort_values(ascending=False)
                 .head(15) * 100)
occ_default.plot(kind='bar', color='orangered', edgecolor='black')
plt.title('Top 15 Occupations by Default Rate')
plt.ylabel('Default Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ── 5. TOP STATES BY DEFAULT RATE ────────────────────────────
plt.figure(figsize=(12, 5))
state_default = (df.groupby('Residence_State')['Loan_Default_Risk']
                   .mean()
                   .sort_values(ascending=False)
                   .head(15) * 100)
state_default.plot(kind='bar', color='teal', edgecolor='black')
plt.title('Top 15 States by Default Rate')
plt.ylabel('Default Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ── 6. INCOME DISTRIBUTION: DEFAULTERS vs NON-DEFAULTERS ─────
plt.figure(figsize=(9, 4))
sns.kdeplot(data=df, x='Annual_Income', hue='Loan_Default_Risk',
            fill=True, alpha=0.4, palette={0: 'green', 1: 'red'})
plt.title('Income Distribution: Defaulters vs Non-Defaulters')
plt.xlabel('Annual Income')
plt.tight_layout()
plt.show()

# ── 7. AGE DISTRIBUTION ───────────────────────────────────────
plt.figure(figsize=(9, 4))
sns.kdeplot(data=df, x='Applicant_Age', hue='Loan_Default_Risk',
            fill=True, alpha=0.4, palette={0: 'green', 1: 'red'})
plt.title('Age Distribution: Defaulters vs Non-Defaulters')
plt.xlabel('Age')
plt.tight_layout()
plt.show()

# ── 8. WORK EXPERIENCE vs DEFAULT ────────────────────────────
plt.figure(figsize=(8, 4))
sns.boxplot(x='Loan_Default_Risk', y='Work_Experience', data=df,
            palette={0: 'lightgreen', 1: 'salmon'})
plt.title('Work Experience vs Loan Default Risk')
plt.xticks([0, 1], ['Non-Defaulter', 'Defaulter'])
plt.tight_layout()
plt.show()

# ── 9. STABILITY SCORE vs DEFAULT ────────────────────────────
plt.figure(figsize=(8, 4))
sns.boxplot(x='Loan_Default_Risk', y='Stability_Score', data=df,
            palette={0: 'lightblue', 1: 'orange'})
plt.title('Stability Score (Employment + Residence Years) vs Default Risk')
plt.xticks([0, 1], ['Non-Defaulter', 'Defaulter'])
plt.tight_layout()
plt.show()

# ── 10. CORRELATION HEATMAP ───────────────────────────────────
plt.figure(figsize=(8, 5))
num_cols = ['Annual_Income', 'Applicant_Age', 'Work_Experience',
            'Years_in_Current_Employment', 'Years_in_Current_Residence',
            'Stability_Score', 'Loan_Default_Risk']
sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

# ── 11. COUNT PLOT: HOUSE OWNERSHIP × MARITAL STATUS ─────────
plt.figure(figsize=(8, 4))
sns.countplot(x='House_Ownership', hue='Marital_Status', data=df, palette='Set2')
plt.title('House Ownership by Marital Status')
plt.tight_layout()
plt.show()

# ── 12. SUMMARY TABLE ─────────────────────────────────────────
print("\n── Default Rate Summary ──")
for col in ['House_Ownership', 'Marital_Status', 'Vehicle_Ownership',
            'Age_Group', 'Income_Bracket']:
    print(f"\n{col}:")
    print(df.groupby(col)['Loan_Default_Risk']
            .agg(['mean', 'count'])
            .rename(columns={'mean': 'Default_Rate', 'count': 'Count'})
            .assign(Default_Rate=lambda x: (x['Default_Rate'] * 100).round(2)))