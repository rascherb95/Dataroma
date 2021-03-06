from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt

base_url = 'https://www.dataroma.com'


#to create a list of our investors
def get_investors():

    investors = []
    html = urlopen(base_url)
    soup = BeautifulSoup(html.read(),'lxml')

    for link in soup.find('span',{'id':'port_body'}).find_all('a'):
        investors.append((Investor(link.getText(),link.get('href'))))
    return (investors)

#investor class
class Investor():
   
    def __init__(self,name,investor_url):
        self.name= name
        self.url = base_url + investor_url

    def get_portfolio(self):
        html = urlopen(self.url)
        soup = BeautifulSoup(html.read(),'lxml')

        portfolio = []
        tbody= soup.tbody
        tr = tbody.find_all('tr')

        for t in tr:
            portfolio.append(t.text.split('\n'))
            df = pd.DataFrame(portfolio)

#reformatting the dataframe
        df.columns = [0,1,'Ticker','Weight','Shares','Action','Price','Value','']
        df['Ticker'] = df['Ticker'].str.split('-', expand=True)  #to update split to make 2 columns, ticker + company
        df['Weight'] = df['Weight'].astype(float)/100
        #df['Company'] = df['Stock'].str.rsplit('-')
        df = df.drop(columns = [0,1])
        return df
        
        
#to get our chosen investor's portfolio
def get_specific(arg):
    for i in x:
        if arg in i.name:
            print("-"*100)
            print(i.name)
            print("-"*100)
            print(i.get_portfolio())
            break
    else:
        print("-"*100)
        print("{} not found".format(arg)) 

#should be renamed investor_list for easier readability
x = get_investors()


# to print out the list of available filings. could add prompt (See available portfolios? Y/N)
#for i in x:
#    print(i.name)

print('Fund manager last name:')
chosen_investor = (input())
chosen_investor = chosen_investor.capitalize()


#runs everything
get_specific(chosen_investor)


