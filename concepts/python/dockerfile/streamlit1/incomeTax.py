import streamlit as st
import plotly.express as px
import pandas as pd

maxTaxable=250000

taxBands = pd.DataFrame()
taxBands['taxYear'] = ["2018-2019", "2019-2020", "2020-2021", "2021-2022"]
taxBands['allowance'] = [11850, 12500, 12500, 12570]
taxBands['basic'] = [46350, 50000, 50000, 50270 ]
taxBands['high'] = [150000, 150000, 150000, 150000]
taxBands.set_index('taxYear', inplace=True)
taxBands


def incomeTax(beforeTax, PersonalAllowances=12500, BasicRate=50000, HigherRate=150000):
    Tax=[]
    for income in range(beforeTax):
        if income <= PersonalAllowances:
            Tax.append(0)
        elif PersonalAllowances < income <= BasicRate:
            tax = (income - PersonalAllowances) * 0.2
            Tax.append(tax)
        elif BasicRate < income <= 100000:
            tax = (BasicRate - PersonalAllowances) * 0.2 + (income - BasicRate) * 0.4
            Tax.append(tax)
        elif 100000 < income < HigherRate:
            AdjustedPersonalAllowances = PersonalAllowances - (income - 100000)/2
            if AdjustedPersonalAllowances >= 0:
                AdjustedBasicRate = BasicRate - (income - 100000)/2
                tax = (AdjustedBasicRate - AdjustedPersonalAllowances) * 0.2 + (income - AdjustedBasicRate) * 0.4
                Tax.append(tax)
            else:
                AdjustedBasicRate = BasicRate - PersonalAllowances
                tax = AdjustedBasicRate * 0.2 + (income - AdjustedBasicRate) * 0.4
                Tax.append(tax)
        else: # income > HigherRate
            AdjustedBasicRate = BasicRate - PersonalAllowances
            tax = AdjustedBasicRate * 0.2 + (income - AdjustedBasicRate) * 0.4 + (income - HigherRate) * 0.05
            Tax.append(tax)

    return Tax


# GUI Part
st.sidebar.header("User inputs")

def getUserInput(MAXbeforeTax):
    taxYear = st.sidebar.selectbox("Tax Year", taxBands.index, index=2)
    beforetax = st.sidebar.slider("PAYE income before tax:", max_value=MAXbeforeTax, value=120000)
    taxCode = st.sidebar.text_input("Tax Code (to be implemented)", "1250L", 8)
    return taxYear,beforetax, taxCode


taxYear, beforetax, taxCode = getUserInput(maxTaxable)

pAllowance = taxBands['allowance'][taxYear]
bRate=taxBands['basic'][taxYear]
hRate=taxBands['high'][taxYear]

df = pd.DataFrame()
df['income'] = range(maxTaxable)
df.income.replace(0,-1, inplace=True)
df['tax'] = incomeTax(maxTaxable, PersonalAllowances=pAllowance, BasicRate=bRate, HigherRate=hRate)
df['taxRate'] = df['tax'] / df['income']
df['low_income_tax'] = df['tax'][:bRate]
df['mid_income_tax'] = df['tax'][bRate:hRate]
df['hih_income_tax'] = df['tax'][hRate:]

fig = px.area(df, x='income', y=['low_income_tax', 'mid_income_tax', 'hih_income_tax', 'taxRate'], labels={"variable": "Income Bands"})
fig.add_vline(beforetax,line_width=3, line_dash="dash", line_color="green", opacity=0.7)
fig.update_layout(xaxis={"title": "Income"}, yaxis={"title": "Tax"})
st.plotly_chart(fig)


st.write(f"The tax year is: {taxYear}, Your preTax income is {beforetax} and taxcode is: {taxCode}")
st.write(df.iloc[beforetax].dropna())