import sys
import json
from ufal.udpipe import Model, Pipeline, ProcessingError  # pylint: disable=no-name-in-module

model = Model.load(
        'spanish-ancora-ud-2.3-181115.udpipe')
pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
error = ProcessingError()

def udpipe_parse(text):
    if text is None:
        return ""
    processed = pipeline.process(text, error)
    if error.occurred():
        sys.stderr.write("An error occurred when running run_udpipe: ")
        sys.stderr.write(error.message)
        sys.stderr.write("\n")
        sys.exit(1)

    return processed


def udpipe_pos(processed):
    processed = processed.split('\n')
    par_id = 0
    sent_id = -1
    parse_table = []
    for line in processed:
        # ignore blank lines
        if len(line) == 0:
            continue

        # found new paragraph comment
        if line == '# newpar':
            par_id += 1

        # found new sentence comment
        if '# sent_id =' in line:
            sentence_comment = line.split('=')
            sent_id = int(sentence_comment[1].strip())

        # found actual parse token
        if line[0] != '#':
            parse_fields = line.split('\t')

            if len(parse_fields) == 10:
                parse_token = dict()
                parse_token['SentID'] = sent_id
                parse_token['ParID'] = par_id
                parse_token['Id'] = parse_fields[0]
                parse_token['Form'] = parse_fields[1]
                parse_token['Lemma'] = parse_fields[2]
                parse_token['UPosTag'] = parse_fields[3]
                parse_token['XPosTag'] = parse_fields[4]
                parse_token['Feats'] = parse_fields[5]
                parse_token['Head'] = parse_fields[6]
                parse_token['DepRel'] = parse_fields[7]
                parse_token['Deps'] = parse_fields[8]
                parse_token['Misc'] = parse_fields[9]
                parse_table.append(parse_token)

    parse_pos = {
        'PROPN': set(),
        'VERB': set(),
        'NUM': set(),
        'AUX': set(),
        'NOUN': set(),
    }

    for token in parse_table:
        for pos in parse_pos:
            if token['UPosTag'] == pos:
                parse_pos[pos].add(token['Lemma'])

    for pos in parse_pos:
        parse_pos[pos] = list(parse_pos[pos])

    return json.dumps(parse_pos)

def jacc_sim(set1, set2):
    set1 = set(set1)
    set2 = set(set2)

    set_intersection_size = len(set1 & set2)
    set_union_size = len(set1 | set2)
    if(set_union_size == 0):
        return 0

    return set_intersection_size / set_union_size
