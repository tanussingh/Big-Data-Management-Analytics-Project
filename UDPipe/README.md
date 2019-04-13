# Getting Started with UDPipe

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
