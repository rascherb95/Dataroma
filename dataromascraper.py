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
        df['Ticker'] = df['Ticker'].str.split('-', expand=True)
        df['Weight'] = df['Weight'].astype(float)/100
        #df['Company'] = df['Stock'].str.rsplit('-')
        df = df.drop(columns = [0,1])
        return df
        
        
#to get our chosen investor's portfolio
def get_specific(arg):
    i=0
    found = False
    while i < len(x):
        for _ in x:
            if arg in x[i].name:  #basic string search (unique last name only)
                found = True
                inv_num = i      #stored to then retrieve the portfolio
                i+=1        
            else:
                i+=1
    if found:
        print("-"*100)
        print(x[inv_num].name)
        print("-"*100)
        print(x[inv_num].get_portfolio())
    else:
        print("-"*100)
        print("{} not found".format(arg))


x = get_investors()

#for i in x:
#    print(i.name)


print('Fund manager last name:')
chosen_investor = (input())
chosen_investor = chosen_investor.capitalize()

 

#runs everything
get_specific(chosen_investor)


