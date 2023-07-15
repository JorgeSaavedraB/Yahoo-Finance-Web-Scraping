#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import time
import datetime

from web_scraping_yahoo_finance import basic_inf
from web_scraping_yahoo_finance import stock_price
from web_scraping_yahoo_finance import Financial_Statements
from web_scraping_yahoo_finance import Financial_Statements_2

import matplotlib.pyplot as plt

from selenium.webdriver.chrome.service import Service
from selenium import webdriver


# In[2]:


def find(F_S, word):
    for i in range(len(F_S)):
        
        if(F_S[i][0] == word):
            j = i
            break
            
        else:
            None
            
    return j


# In[3]:


def plot_bars(F_S, name_data, y_label):
    y = []
    for elmts in F_S[1][:]:
        y.append(float(elmts))

    DF = pd.DataFrame({'dates': F_S[0][:], name_data : y})

    DF.plot(x = 'dates', y = name_data, kind = 'bar', grid = True, legend = True, use_index = True, xlabel = '', ylabel = y_label)


# ### Financial Statements

# In[4]:


def All_Financial_Statements(ticker):
    C_F_A = Financial_Statements_2(ticker, 'cash flow', 'anual')
    df = pd.DataFrame(C_F_A)
   
    C_F_Q = Financial_Statements_2(ticker, 'cash flow', 'quarterly')
    df = pd.DataFrame(C_F_Q)
 
    B_S_A = Financial_Statements_2(ticker, 'balance sheet', 'anual')
    df = pd.DataFrame(B_S_A)

    B_S_Q = Financial_Statements_2(ticker, 'balance sheet', 'quarterly')
    df = pd.DataFrame(B_S_Q)

    I_S_A = Financial_Statements_2(ticker, 'income statement', 'anual')
    df = pd.DataFrame(I_S_A)

    I_S_Q = Financial_Statements_2(ticker, 'income statement', 'quarterly')
    df = pd.DataFrame(I_S_Q)

    return(C_F_A, C_F_Q, B_S_A, B_S_Q, I_S_A, I_S_Q)


# ### Number of shares

# In[7]:


def Num_Shares_A(I_S_A, B_S_A):
    F_S = I_S_A
    
    F_S0 = B_S_A
    
    k = find(F_S, 'Diluted Average Shares')
    
    z = find(F_S0, 'Ordinary Shares Number')
    
    total_S = [F_S[0][1: len(F_S[0]) - 1]]
    num_shares = []
    
    for l in range(1, len(F_S[0][:]) - 1):
        
        # Due sometimes the Ordinary Shares Number is not in the Income Statement
        if(pd.isna(F_S[k][l]) == True):
            print('*')
            n_shares = F_S0[z][l]
            
        else:
            n_shares = F_S[k][l]
        
        n_shares = (n_shares).replace(',', '')
        num_shares.append(n_shares)
        
    total_S.append(num_shares)

    return(total_S)


# ### EPS

# In[9]:


def EPS_Q(ticker, I_S_Q, B_S_Q):
    F_S = I_S_Q
    
    F_S0 = B_S_Q
    
    j = find(F_S, 'Net Income Common Stockholders')
    
    k = find(F_S, 'Diluted Average Shares')
    
    z = find(F_S0, 'Ordinary Shares Number')
    
    T_EPS = 0
    All_EPS = []
    
    for l in range(1, len(F_S[0][:]) - 1):
        n_shares = 0
        
        # Due sometimes the Ordinary Shares Number is not in the Income Statement
        if(pd.isna(F_S[k][l]) == True):
            print('*')
            n_shares = F_S0[z][l]
            
        else:
            n_shares = F_S[k][l]
            
        EPS = float((F_S[j][l]).replace(',', '')) / float((n_shares).replace(',', ''))
        EPS = round(EPS, 2)
        All_EPS.append(EPS)
        T_EPS = T_EPS + EPS
    
    t_info = [F_S[0][1:len(F_S[0][:]) - 1]]
    t_info.append(All_EPS)
    
    return(t_info)


# In[11]:


def EPS_A(ticker, I_S_A, B_S_A):
    F_S = I_S_A
    
    F_S0 = B_S_A
    
    j = find(F_S, 'Net Income Common Stockholders')
    
    k = find(F_S, 'Diluted Average Shares')
    
    z = find(F_S0, 'Ordinary Shares Number')
    
    T_EPS = 0
    All_EPS = []
    
    for l in range(1, len(F_S[0][:]) - 1):
        n_shares = 0
        
        # Due sometimes the Ordinary Shares Number is not in the Income Statement
        if(pd.isna(F_S[k][l]) == True):
            print('*')
            n_shares = F_S0[z][l]
            
        else:
            n_shares = F_S[k][l]
            
        EPS = float((F_S[j][l]).replace(',', '')) / float((n_shares).replace(',', ''))
        EPS = round(EPS, 2)
        All_EPS.append(EPS)
        T_EPS = T_EPS + EPS
    
    t_info = [F_S[0][1:len(F_S[0][:]) - 1]]
    t_info.append(All_EPS)
    
    return(t_info)


# ### Historical prices (end year)

# In[13]:


def Historical_prices_EY(ticker, I_S_A, B_S_A):
    close_prices = []
    
    for EPS in EPS_A(ticker, I_S_A, B_S_A)[0]:
        date_A = datetime.datetime.strptime(EPS, '%m/%d/%Y')    
        
        if(date_A.weekday() == 6):
            period1 = int(time.mktime(datetime.datetime(date_A.year, date_A.month, date_A.day-2).timetuple()))
            print(date_A.year, date_A.month, date_A.day-2)
        elif(date_A.weekday() == 5):
            period1 = int(time.mktime(datetime.datetime(date_A.year, date_A.month, date_A.day-1).timetuple()))
            print(date_A.year, date_A.month, date_A.day-1)
        else:
            period1 = int(time.mktime(datetime.datetime(date_A.year, date_A.month, date_A.day).timetuple()))
        
        
        period2 = int(time.mktime(datetime.datetime(date_A.year + 1, 1, 1).timetuple()))

        interval = '1d'
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        
        close_prices.append(round(np.array(df['Close'][0: 3])[0], 3))
    historical_anual_prices = EPS_A(ticker, I_S_A, B_S_A)
    historical_anual_prices.append(close_prices)
    
    return(historical_anual_prices)


# ### Dividents

# In[15]:


def Historical_Dividends(ticker, I_S_A, B_S_A):
    T_dividends = []
    
    for l in EPS_A(ticker, I_S_A, B_S_A)[0]:
        chrome_path = Service(r"C:\Users\hybri\Downloads\chromedriver_win32\chromedriver.exe")
        driver = webdriver.Chrome(service = chrome_path, options = webdriver.ChromeOptions())

        date_A = datetime.datetime.strptime(l, '%m/%d/%Y')
        period1 = int(time.mktime(datetime.datetime(date_A.year, 1, 1).timetuple()))
        period2 = int(time.mktime(datetime.datetime(date_A.year + 1, 1, 1).timetuple()))

        query_string = f'https://finance.yahoo.com/quote/{ticker}/history?period1={period1}&period2={period2}&interval=capitalGain%7Cdiv%7Csplit&filter=div&frequency=1mo&includeAdjustedClose=true'
        driver.get(query_string)
        driver.implicitly_wait(5)

        dfs_quarter = pd.read_html(driver.page_source)
        driver.close()

        dfs_quarter = np.array(dfs_quarter)

        if(len(dfs_quarter[0]) > 1):
            dividends = dfs_quarter[0][0: len(dfs_quarter[0]) -1]

            Total_dividends = 0
            for k in range(len(dividends)):
                dividends[k][1] = dividends[k][1].replace(' Dividend', '')
                print(dividends[k][0:2])
                if(dividends[k][1] == 'Nos' or dividends[k][1] == 'No Dividends'):
                    dividends[k][0:2] = '0'
                Total_dividends = Total_dividends + float(dividends[k][1])
                Total_dividends = round(Total_dividends, 3)

        else:
            Total_dividends = 0

        T_dividends.append(Total_dividends)

    Anual_dividends = [EPS_A(ticker, I_S_A, B_S_A)[0]]
    Anual_dividends.append(T_dividends)
    
    return(Anual_dividends)


# ### PER (Trailing)

# ### $PER = \frac{Current Share Price}{Trailing 12-Month EPS}$

# In[18]:


def PER(ticker, I_S_Q, B_S_Q):
    TTM_EPS=0
    
    for EPS in EPS_Q(ticker, I_S_Q, B_S_Q)[1]:
        TTM_EPS = TTM_EPS + EPS

    PER = stock_price(ticker) / TTM_EPS
    PER = round(PER, 2)
    
    return PER


# ### ANUAL PER

# In[20]:


def ANUAL_PER(ticker, I_S_A, B_S_A):
    Historical_prices_end_year = Historical_prices_EY(ticker, I_S_A, B_S_A)
    a_PER = []
    
    for k in range(0, len(Historical_prices_end_year[0])):
        A_PER =  float(Historical_prices_end_year[2][k]) / float(Historical_prices_end_year[1][k])
        A_PER = round(A_PER, 3)
        a_PER.append(A_PER)
    
    anual_PER = [Historical_prices_end_year[0]]
    anual_PER.append(a_PER)
    
    return(anual_PER)


# ### Average PER

# In[22]:


def AVERAGE_PER(ticker, I_S_A, B_S_A):
    anual_per = ANUAL_PER(ticker, I_S_A, B_S_A)[1]
    sum_PER = 0
    
    for k in anual_per:
        sum_PER = float(sum_PER) + k
    average_PER = sum_PER/len(anual_per)
    average_PER = round(average_PER, 3)
    
    return(average_PER)


# ### Price to Book (MRQ)

# ### $PB(MRQ) = \frac{Market Price Per Share}{Book Value Per Share (Most Recent Quarter)}$

# In[1]:


def Price_Book_MRQ(ticker, B_S_Q):
    F_S = B_S_Q
    j = find(F_S, 'Common Stock Equity')
            
    k = find(F_S, 'Ordinary Shares Number')
            
    P = stock_price(ticker)

    C_S_equity = float(str(F_S[j][len(F_S[0][:]) - 1]).replace(',', ''))
    O_S_number = float(str(F_S[k][len(F_S[0][:]) - 1]).replace(',', ''))
    B_V = C_S_equity / O_S_number
    P_B = P / B_V
    P_B = round(P_B, 2)
    
    return(P_B)


# ### Debt to Equity (D/E)

# ### $DE = \frac{Total Liabilities}{Total Shareholders' Equity}$

# In[ ]:


def DE_Q(ticker, B_S_Q):
    F_S = B_S_Q
    
    j = find(F_S, 'Total Liabilities Net Minority Interest')
    
    k = find(F_S, 'Common Stock Equity')
    
    All_D_E_Q = []
    
    for l in range(1, len(F_S[0][:])):
        D_E_Q = float((F_S[j][l]).replace(',', '')) / float((F_S[k][l]).replace(',', ''))
        D_E_Q = round(D_E_Q, 2)
        All_D_E_Q.append(D_E_Q)
        
    t_info = [F_S[0][1:len(F_S[0][:])]]
    t_info.append(All_D_E_Q)
    
    return(t_info)


# In[ ]:


def DE_A(ticker, B_S_A):
    F_S = B_S_A
    
    j = find(F_S, 'Total Liabilities Net Minority Interest')
    
    k = find(F_S, 'Common Stock Equity')
    
    All_D_E_Q = []
    
    for l in range(1, len(F_S[0][:])):
        D_E_Q = float((F_S[j][l]).replace(',', '')) / float((F_S[k][l]).replace(',', ''))
        D_E_Q = round(D_E_Q, 2)
        All_D_E_Q.append(D_E_Q)
        
    t_info = [F_S[0][1:len(F_S[0][:])]]
    t_info.append(All_D_E_Q)
    
    #print('DE(Anual):')
    return(t_info)


# ### ROE

# ### $ROE = \frac{Net Income}{Average Shareholders' Equity}$

# In[ ]:


def ROE(ticker, I_S_A, B_S_A):
    tckr = ticker
    F_S = I_S_A
    F_S1 = B_S_A
    
    j = find(F_S, 'Net Income Common Stockholders')
    k = find(F_S1, 'Common Stock Equity')
    
    y = []
    
    for l in range(1, len(F_S1[0][:])):
        ROE = float((F_S[j][l]).replace(',', '')) / float((F_S1[k][l]).replace(',', ''))
        ROE = round(ROE*100, 2)
        y.append(ROE)
        
    t_info = [F_S[0][1:len(F_S1[0][:])]]
    t_info.append(y)
    
    return(t_info)


# ### Average ROE

# In[ ]:


def Average_ROE(ticker, I_S_A, B_S_A):
    
    Avrg_ROE = 0
    ROE_ = ROE(ticker, I_S_A, B_S_A)
    
    for k in ROE_[1]:
        Avrg_ROE = Avrg_ROE + (k / 100)
    
    Avrg_ROE = round(Avrg_ROE / len(ROE_[1]), 3)
    
    return(Avrg_ROE)


# ### Common Stock Equity

# In[ ]:


def CSE(ticker, B_S_A):
    F_S = B_S_A
    
    j = find(F_S, 'Common Stock Equity')
    Common_SE = []
    
    for k in range(1, len(F_S[j][:])):
        Common_SE.append(float(F_S[j][k].replace(',', '')))
    All_CSE = [F_S[0][1:len(F_S[0][:])]]
    All_CSE.append(Common_SE)
    
    return(All_CSE)


# In[ ]:


def Growth_CSE(ticker, B_S_A):
    cse = CSE(ticker, B_S_A)[1][:]
    x = np.arange(0, len(cse))
    y = cse

    from sklearn.linear_model import LinearRegression 
    regresion_lineal = LinearRegression() 
    regresion_lineal.fit(x.reshape(-1,1), y) 
    m = regresion_lineal.coef_
    m = m[0]
    m = round(m,3)
    b = regresion_lineal.intercept_
    
    return(m)


# ### Common Stock Equity per Share

# In[ ]:


def CSEpS(ticker, I_S_A, B_S_A): 
    CSE_PS = []
    
    for k in range(len(Num_Shares_A(I_S_A, B_S_A)[1][:])):
        
        cseps = CSE(ticker, B_S_A)[1][k] / float(Num_Shares_A(I_S_A, B_S_A)[1][k])
        
        cseps = round(cseps, 3)
        CSE_PS.append(cseps)
    all_CSE_PS = [CSE(ticker, B_S_A)[0]]
    all_CSE_PS.append(CSE_PS)
    return(all_CSE_PS)


# ### Average Payout Ratio

# In[ ]:


def Average_Payout_Ratio(ticker, I_S_A, B_S_A):
    EarnigsPS_A = EPS_A(ticker, I_S_A, B_S_A)
    Hist_Div = Historical_Dividends(ticker, I_S_A, B_S_A)
    
    Average_PR = 0
    
    for k in range(0,len(EarnigsPS_A[1])):
        P_R = Hist_Div[1][k] / EarnigsPS_A[1][k]
        Average_PR = Average_PR + P_R

    Average_PR = Average_PR / len(EarnigsPS_A[1])
    Average_PR = round(Average_PR, 3)
    
    return(Average_PR)


# ### Extra

# In[ ]:


def Stock_Analisis(tickers):
    P_B = []
    P_E_R = []
    A_P_E_R = []
    R_O_E = []
    D_E = []
    G_R = []

    for tckr in tickers:
        score_total = 0

        C_F_A, C_F_Q, B_S_A, B_S_Q, I_S_A, I_S_Q = All_Financial_Statements(tckr)

        print(tckr + ':')
        basic_inf(tckr)
        
        
        #CSE
        c_s_e = CSE(tckr, B_S_A)
        g_CSE = Growth_CSE(tckr, B_S_A)
        print('CSE:')
        display(pd.DataFrame(c_s_e))
        plot_bars(c_s_e, 'Common Stock Equity', '')

        
        #PB
        Price_Book = Price_Book_MRQ(tckr, B_S_Q)
        P_B.append(Price_Book)
        print('Price to Book', Price_Book)

        
        #PER
        Per = PER(tckr, I_S_Q, B_S_Q)
        A_Per = AVERAGE_PER(tckr, I_S_A, B_S_A)
        print('PER:', Per)
        P_E_R.append(Per)
        print('Average PER: ', A_Per)
        A_P_E_R.append(A_Per)

        
        #ROE
        print('ROE:')
        display(pd.DataFrame(ROE(tckr, I_S_A, B_S_A)))
        
        Avrg_ROE = Average_ROE(tckr, I_S_A, B_S_A)
        R_O_E.append(Avrg_ROE)
        print('Average ROE:', Avrg_ROE * 100, '%')

        
        #DE
        Debt_to_Equity = DE_Q(tckr, B_S_Q)[1][len(DE_Q(tckr, B_S_Q)[1]) - 1]
        D_E.append(Debt_to_Equity)
        y = []
        for elmts in DE_Q(tckr, B_S_Q)[1][:]:
            y.append(float(elmts))

        DF = pd.DataFrame({'dates': DE_Q(tckr, B_S_Q)[0][:], 'DE_Q': y})

        DF.plot(x = 'dates', y = 'DE_Q', kind = 'bar', grid = True, legend = True, use_index = True, xlabel = '')

        print('Debt to Equity (MRQ):', Debt_to_Equity)

        
        #Dividends
        dividends = Historical_Dividends(tckr, I_S_A, B_S_A)
        print('Dividends:')
        display(pd.DataFrame(dividends))
        
        plot_bars(dividends, 'Dividends', '')
     
    
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print('')
        
    #Data Scores
    inf_data = {'ticker' : tickers, 'P/B' : P_B ,'PER' : P_E_R, 'ROE' : R_O_E, 'D/E' : D_E}
    print(inf_data)
    df = pd.DataFrame(data = inf_data) 

    return(df)

