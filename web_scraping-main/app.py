from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')

row = table.find_all('th', attrs={'class':'font-semibold text-center'}) 
row_length = len(row)
row_length

row = table.find_all('td', attrs={'class':'text-center'}) 
row_length2 = len(row)
row_length2

date = []
market_cap = []
volume = []
open = []
close = []

   #getdate
for i in range(0, row_length):
    Date = table.find_all('th', attrs={'class':'font-semibold text-center'})[i].text
    date.append(Date)  #to remove excess white space
    
    #get marketcap
for i in range(0, row_length2,4):
    Market_Cap = table.find_all('td', attrs={'class':'text-center'})[i].text
    Market_Cap = Market_Cap.strip() #to remove excess white space
    market_cap.append(Market_Cap)
    
    #get volume
for i in range(1, row_length2,4):
    volumee = table.find_all('td', attrs={'class':'text-center'})[i].text
    volumee = volumee.strip() #to remove excess white space
    volume.append(volumee)
    
     #get open
for i in range(2, row_length2,4):
    openn = table.find_all('td', attrs={'class':'text-center'})[i].text
    openn = openn.strip() #to remove excess white space
    open.append(openn)
    
     #get close
for i in range(3, row_length2,4):   
    closee = table.find_all('td', attrs={'class':'text-center'})[i].text
    closee = closee.strip() #to remove excess white space
    close.append(closee)

#change into dataframe
etc = pd.DataFrame({
    'Date': date,
    'Market Cap': market_cap,
    'Volume' : volume,
    'Open' : open,
    'Close' : close
}, columns=['Date', 'Market Cap', 'Volume', 'Open', 'Close'])

#insert data wrangling here
eth = etc[['Date', 'Volume']]
def delete_dollar(x):
  for i in x:
    xx =  i.split('$')
    return int(xx[1].replace(',',''))
eth['Volume'] = eth[['Volume']].apply(delete_dollar,axis=1)
eth = eth[::-1].set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{eth}' #be careful with the " and ' 
	

	# generate plot
	ax = eth.plot() 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)