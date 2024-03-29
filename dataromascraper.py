from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import matplotlib.pyplot as plt

base_url = 'https://www.dataroma.com'
yahoo_base = 'https://finance.yahoo.com/quote/'
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


#to create a list of our investors
def get_investors():

    investors_scrape = []
    req = Request(base_url , headers = headers)
    html = urlopen(req,data=None)
    soup = BeautifulSoup(html.read(),'lxml')

    for link in soup.find('span',{'id':'port_body'}).find_all('a'):
        investors_scrape.append((Investor(link.getText(),link.get('href'))))
    return (investors_scrape)

class Investor():
   
    def __init__(self,name,investor_url):
        self.name = name
        self.url = base_url + investor_url

    def get_portfolio(self):
        Investor_req = Request(self.url,headers = headers)
        html = urlopen(Investor_req) # request needs to have user:agent to avoid 403 error

        soup = BeautifulSoup(html.read(),'lxml')

        portfolio = []
        #portfolio_date = soup.find_all('p',{'id' : 'p2'})      OPEN to add in porfolio date as DF column
        
        tbody = soup.tbody
        tr = tbody.find_all('tr')

        for t in tr:
            portfolio.append(t.text.split('\n'))
            df = pd.DataFrame(portfolio)

        df.columns = [0,'Ticker','Yahoo','Weight','Shares','Action','Price','Reported Value','Actual value']

        #The data is 9 items so 9 columns. 'Yahoo' column is imported as a list of [Ticker, Company name]. 
        #The re-ordering of yahoo into ticker below is for formatting & ordering purposes
        ###OPEN to explode the list into two columns 'Ticker' & 'Full Name'

        df['Ticker'] = df['Yahoo'].str.split('-', expand=True) 
        df['Yahoo'] = yahoo_base + df['Ticker']
        df['Weight'] = df['Weight'].astype(float)/100
        df['Shares'] = df['Shares'].str.replace(',','').astype(int)
        df['Price']  = df['Price'].str.replace('$','').astype(float)
        df['Actual value'] = df['Shares'] * df['Price']
        #df['Company'] = df['Stock'].str.rsplit('-')
        df = df.drop(columns = [0])   

        df.to_excel(f'{chosen_investor}.xlsx')
       # print(f'the portfolio date is {portfolio_date[1]}')

        return df

             
#to get our chosen investor's portfolio
def get_specific(arg):
    for i in investor_list: #for each investor in our investor list (investor_scrape dict)
        if arg in i.name: #if name is in investor.name,
            print("-"*100)
            print(i.name)
            print("-"*100)
            print(i.get_portfolio())
            break
    else:
        print("-"*100)
        print("{} not found".format(arg)) 
    

investor_list = get_investors()


#to print out the list of available filings
for i in investor_list:
    print(i.name)

print('Fund manager last name:')
chosen_investor = (input())
chosen_investor = chosen_investor.capitalize()

#runs everything
get_specific(chosen_investor)
#export_portfolio(chosen_investor)






