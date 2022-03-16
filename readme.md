

File runs off the CoinMarketCap API - 
Need to get an API key from CoinMarketCap[https://coinmarketcap.com/]. There are limitations to the number of calls on a daily and monthly basis. 
Plug API KEY variable into a api_key.py file. 

Other components to build out:
1) When adding symbol, loop through for duplicates; a) Either add totals together (sum in pandas df), or b) don't add; build out logic
2) Option to delete symbol and/or specific amoutns of crypto
3) Cleanup chart structure so the layout or legend is tighter and easier to read
