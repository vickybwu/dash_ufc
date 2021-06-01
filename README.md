This is my second UFC APP. I built the first one in RShiny with ggplot2 and had it run locally.

This time I built it in Dash and used Plotly for graphing. I deployed the APP on Heroku.

View the APP here: https://ufcdashboardvickywu.herokuapp.com/


The App has an Overview section and a Title Bouts section. 
In the Overview section, you can see the total number of fights for each male/female weight class throughout 2010 - 2021. You can also see the average profit per 100 unit bet (betting on red fighter vs. betting on blue fighter) over the years. 
You can filter the data by selecting the Radio Button, and by double clicking the circle legends next to the graph.
In the Title Bouts section, you can pick a title fight from the dropdown menu, it will show you how each fighter performed in the fight and their physical stats. 

I used two datasets for th graphs:

(1) ufc.csv 
https://github.com/vickybwu/Myfiles/blob/main/ufc.csv
I scraped this dataset from http://ufcstats.com/statistics/fighters. This dataset has physical attributes for all currently active UFC fighters. 

(2) ufc_master.csv 
I downloaded this dataset from Kaggle https://www.kaggle.com/mdabbert/ultimate-ufc-dataset. This dataset contains all the UFC fights held from 2010 to 2021




