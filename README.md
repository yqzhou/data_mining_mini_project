# mini-projects on data mining

UNC-Duke-Game(Mar 7 2015) - twitter data
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
