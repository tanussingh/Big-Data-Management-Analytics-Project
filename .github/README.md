# Data Collection and Preprocessing in Spark

Project for CS 6350 (Spring19) at The University of Texas at Dallas. 

## Project team: 
* Mavis Francia - MCF140030
* Tanushri Singh - TTS150030
* Ishan Sharma - IXS171130
* Vyaas Shenoy - VNS170230


## Installation

### Crawler

1. Setup a [venv](https://docs.python.org/3/library/venv.html) to keep your local environment clean. 
2. Install [news-please](https://github.com/fhamborg/news-please) using `pip install news-please` 

## Running

1. Crawl all your data and ensure it is brought saved as a JSON in MongoDB
2. Run readInFromMongo.py to stream data into Kafka
3. Run streamToSpark.py to stream data into Spark
4. Run doc2vec.py and mongo_processing.py to get similariy measures on articles
5. Run runningJaccSim.py to compute and run the DeDuplication algorithm 


All components are saved back to MongoDB and can be directly accessed from there.
