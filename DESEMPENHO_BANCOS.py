# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:44:32 2022

@author: w3110
"""

#importação de bibliotecas
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib. pyplot as plt
import datetime
import matplotlib.dates as mdates

#obtem dados com 'yfinance' e realiza pré-processamento
def dados1(acao):
    d = pd.DataFrame(yf.download(acao,interval = "1mo",start = '2021-05-01', end = '2022-05-31'))
    d = d.drop(columns=['Open', 'High', 'Low', 'Adj Close','Volume'])
    d['Data'] = d.index
    d = d.rename(columns={'Close': 'Fechamento'})
    d = d.dropna()
    d.index = range(1,(len(d)+1))
    return(d.round(2))

 #Calcula coeficiente de variação mensal, variação do papel no período e soma dos dividendos no período
def calc(acao):
    acao = acao.iloc[1:14]
    coef = ((acao['Fechamento'].std()/acao['Fechamento'].mean())*100)
    return(round(coef,2))

def calc2(acao):
    coef = ((acao['Fechamento'].iloc[-1] - acao['Fechamento'].iloc[0])/acao['Fechamento'].iloc[0])*100
    return(round(coef,2))

def dados3(acao):
    d = yf.Ticker(acao)
    d = pd.DataFrame(d.history(interval = "1mo",start = '2021-05-31', end = '2022-05-31'))
    d = d["Dividends"].sum()
    return(round(d,2))

#Calcula coeficiente de variação mensal, variação do papel no período, soma dos dividendos no período e converte em DataFrames
ITUB4 = dados1('ITUB4.SA')
BBAS3 = dados1('BBAS3.SA')
BBDC4 = dados1('BBDC4.SA')
SANB11 = dados1('SANB11.SA')
IBOV = dados1('^BVSP')

ITUB4_c = calc(ITUB4)
BBAS3_c = calc(BBAS3)
BBDC4_c = calc(BBDC4)
SANB11_c = calc(SANB11)
IBOV_c = calc(IBOV)

ITUB4_c2 = calc2(ITUB4)
BBAS3_c2 = calc2(BBAS3)
BBDC4_c2 = calc2(BBDC4)
SANB11_c2 = calc2(SANB11)
IBOV_c2 = calc2(IBOV)

ITUB4_d = dados3("ITUB4.SA")
BBAS3_d = dados3("BBAS3.SA")
BBDC4_d = dados3("BBDC4.SA")
SANB11_d = dados3("SANB11.SA")

BANCOS3_CV = pd.DataFrame.from_dict({'ITUB4':ITUB4_c,'BBAS3':BBAS3_c,'BBDC4':BBDC4_c,'SANB11':SANB11_c,'IBOV':IBOV_c},orient='index').rename(columns={0:'Coef. Variacao'})
BANCOS4_V = pd.DataFrame.from_dict({'ITUB4':ITUB4_c2,'BBAS3':BBAS3_c2,'BBDC4':BBDC4_c2,'SANB11':SANB11_c2,'IBOV':IBOV_c2},orient='index').rename(columns={0:'Variacao_Percentual'})
BANCOS5_D = pd.DataFrame.from_dict({'ITUB4':ITUB4_d,'BBAS3':BBAS3_d,'BBDC4':BBDC4_d,'SANB11':SANB11_d},orient='index').rename(columns={0:'Dividendos'})

#Exporta Dataframes em xlsx para trabalho no Power Bi
with pd.ExcelWriter('IBOV4.xlsx') as writer:  
    BANCOS3_CV.to_excel(writer, sheet_name='COEF_VARIACAO')
    BANCOS4_V.to_excel(writer, sheet_name='VARIACAO_PERCENTUAL')
    BANCOS5_D.to_excel(writer, sheet_name='DIVIDENDOS')

#Código dos Gráficos (matplotlib) de variação mensal presente no Dashboard
def dados4(acao):
    d = pd.DataFrame(yf.download(acao,interval = "1mo",start = '2021-05-01', end = '2022-05-31'))
    d = d.drop(columns=['Open', 'High', 'Low', 'Adj Close','Volume'])
    d = d.dropna()
    return(d.round(2))

ITUB4 = dados4('ITUB4.SA').pct_change()*100
BBAS3 = dados4('BBAS3.SA').pct_change()*100
BBDC4 = dados4('BBDC4.SA').pct_change()*100
SANB11 = dados4('SANB11.SA').pct_change()*100
IBOV = dados4('^BVSP').pct_change()*100

BANCOS3 = pd.DataFrame()
BANCOS3['ITAU'] = ITUB4['Close'].round(2)
BANCOS3['BB'] = BBAS3['Close'].round(2)
BANCOS3['BRADESCO'] = BBDC4['Close'].round(2)
BANCOS3['SANTANDER'] = SANB11['Close'].round(2)
BANCOS3['IBOV'] = IBOV['Close'].round(2)
BANCOS3.fillna(value = 0,  
          inplace = True) 

fig, ax = plt.subplots(figsize=(5, 5))
month_year_formatter = mdates.DateFormatter('%b, %Y')
monthly_locator = mdates.MonthLocator()
ax.xaxis.set_minor_locator(monthly_locator)
ax.xaxis.set_major_formatter(month_year_formatter)
ax.plot(BANCOS3.index, BANCOS3['IBOV'], marker='', color='blue', linestyle='dashed',linewidth=4, alpha=0.7)
ax.plot(BANCOS3.index, BANCOS3['SANTANDER'], marker='', color='#FF4500', linewidth=4, alpha=0.7)
 
ax.fill_between(
    BANCOS3.index, BANCOS3['SANTANDER'], BANCOS3['IBOV'], where=(BANCOS3['SANTANDER'] > BANCOS3['IBOV']), 
    interpolate=True, color="blue", alpha=0.25, 
    label="Positive"
)


ax.fill_between(
    BANCOS3.index, BANCOS3['SANTANDER'], BANCOS3['IBOV'], where=(BANCOS3['SANTANDER'] <= BANCOS3['IBOV']), 
    interpolate=True, color="orange", alpha=0.25,
    label="Negative"
)

ax.set_ylabel("Variação Percentual (%)",fontsize = 12)
fig.autofmt_xdate()
plt.legend(["IBOV","SANB11"],  loc='upper left')
ax.set_title("Variação percentual mensal - SANTANDER")
plt.show()

