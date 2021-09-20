from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import matplotlib.pyplot as plt

base_url = 'https://www.dataroma.com'
yahoo_base = 'https://finance.yahoo.com/quote/'


#to create a list of our investors
def get_investors():

    investors_scrape = []
    req = Request(base_url , headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
    html = urlopen(req,data=None)
    soup = BeautifulSoup(html.read(),'lxml')

    for link in soup.find('span',{'id':'port_body'}).find_all('a'):
        investors_scrape.append((Investor(link.getText(),link.get('href'))))
    return (investors_scrape)

#investor class
class Investor():
   
    def __init__(self,name,investor_url):
        self.name = name
        self.url = base_url + investor_url

    def get_portfolio(self):
        Investor_req = Request(self.url,headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
        html = urlopen(Investor_req) # request needs to have user:agent to avoid 403 error

        soup = BeautifulSoup(html.read(),'lxml')

        portfolio = []
        tbody = soup.tbody
        tr = tbody.find_all('tr')

        for t in tr:
            portfolio.append(t.text.split('\n'))
            df = pd.DataFrame(portfolio)
        

#reformatting the dataframe
        df.columns = [0,1,'Ticker','Weight','Shares','Action','Price','Rounded Value','True value']
        df['Ticker'] = df['Ticker'].str.split('-', expand=True)  #self note to update split to make 2 columns, ticker + company
        df['Weight'] = df['Weight'].astype(float)/100
        df['Shares'] = df['Shares'].str.replace(',','').astype(int)
        df['Price']  = df['Price'].str.replace('$','').astype(float)
        df['True value'] = df['Shares'] * df['Price']
        #df['Company'] = df['Stock'].str.rsplit('-')
        df = df.drop(columns = [0,1])

        df.to_excel('output.xlsx',index=False)

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






