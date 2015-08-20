# mini-projects on data mining

1) UNC-Duke-Game(Mar 7 2015) - twitter
- tools: python, library-twitter, matplotlib, numpy, json, pandas, folium
- twitter API, search with sets of hashtags representing two schools
- fetch data (actual data from ~Mar 1 to Mar 8 morning), preprocessed with only text, hashtags, location and geo information
- extract data between 8pm Mar 7 til 1am Mar 8
- compare # of tweets vs time (two schools)
- track the change of tweets number during the game
- display top 10 popular hashtags for two schools-
- parse the location information from users who tweets for individual school
    - by matching state names
    - by matching city name to state name
    - the final " state: #of tweets" information was exported to school_name.csv file
- （future direction) process and display location/geo information, track number of tweets(daily)


2) CART-Therapy-Biotech-Stock_Tracking(2 year) - Yahoo finance
- tools: python, pandas, matplotlib, yahoo-finance
- yahoo-finance API as data source, focusing on companies involving CAR-T immunotherapy, analyzing their performance against average biotech industry
- extract data from Oct 2013 (when JUNO went IPO) till Aug 1, 2015
- Compare stock price, market share changes of the certain companies
- Compare the performance of the companies against mean of the whole biotech industry
- Analyzing the influence of the releases of clinical trial data on stock price
