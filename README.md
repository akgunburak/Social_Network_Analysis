# Instagram Social Network Analysis
&nbsp;&nbsp;&nbsp;This project is the second project of my internship at International Political Analytics and Strategy. The project aims to analyze any given Instagram page. Objectives are to find the most commented posts, the most common word in the post, the social network graph of the user, and the most influential people in the network.  
&nbsp;&nbsp;&nbsp;In the scraping step I used Selenium to collect the necessary data from Instagram. In the class that I built, I created a couple of methods to scrape different data. In order to use the script, one needs an Instagram account. (I suggest not to use personal accounts)  
&nbsp;&nbsp;&nbsp;I utilized the NLTK library to process text data. I listed the most common words and plotted a WordCloud.  
&nbsp;&nbsp;&nbsp;I wanted to prevent my accounts from being banned, for this reason, I scraped the relations of only a limited number of people. After getting the data, I plotted a network graph using the Networkx library. These kinds of graphs are interactive, so you can zoom in, zoom out, or drag the nodes.  
&nbsp;&nbsp;&nbsp;At the end of the project, I used different calculations such as centrality, betweenness, and page rank to find the most important people in the network. 
[**Click here to view full project.**](https://akgunburak.github.io/Social_Network_Analysis/)

&nbsp;

## Technologies Used
* **Language and version:** Python - 3.8.8
* **Packages:** Pandas, Selenium, NLTK, Matplotlib, Networkx, Pyvis


