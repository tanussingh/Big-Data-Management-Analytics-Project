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

### UDPipe

Download a Universal Dependencies model for Spanish. Here are two different ones:
* [AnCora](https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2898/spanish-ancora-ud-2.3-181115.udpipe?sequence=75&isAllowed=y)
* [GSD](https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2898/spanish-gsd-ud-2.3-181115.udpipe?sequence=74&isAllowed=y)

You can find a full list of models [here](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-2898).

Install the ufal.udpipe library by running: `pip install ufal.udpipe`. You can read more about this library [here](https://pypi.org/project/ufal.udpipe/).

Here is the format for running the example program (from the official page):

```
python run_udpipe.py input_format(tokenize|conllu|horizontal|vertical) output_format(conllu) model_file
```

Here is an example usage:
```
python run_udpipe.py tokenize conllu spanish-ancora-ud-2.3-181115.udpipe
```

Type (or paste) some text into the terminal after the message `Loading model: done`. (You can input multiple lines.)
Then press <kbd>⌘</kbd> + <kbd>D</kbd> to finish reading. The program will then output the UD parse.


## Running

1. Crawl all your data and ensure it is brought saved as a JSON in MongoDB
2. Run readInFromMongo.py to stream data into Kafka
3. Run streamToSpark.py to stream data into Spark
4. Run doc2vec.py and mongo_processing.py to get similariy measures on articles
5. Run runningJaccSim.py to compute and run the DeDuplication algorithm 


All components are saved back to MongoDB and can be directly accessed from there.
