import sys
import re
import json
from ufal.udpipe import Model, Pipeline, ProcessingError  # pylint: disable=no-name-in-module

def udpipe_parse(text):
    processed = pipeline.process(text, error)
    if error.occurred():
        sys.stderr.write("An error occurred when running run_udpipe: ")
        sys.stderr.write(error.message)
        sys.stderr.write("\n")
        sys.exit(1)

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

    return parse_table, parse_pos

def jacc_sim(set1, set2):
    set1 = set(set1)
    set2 = set(set2)

    print(set1 & set2)

    set_intersection_size = len(set1 & set2)
    set_union_size = len(set1 | set2)

    return set_intersection_size / set_union_size




if __name__ == '__main__':
    # In Python2, wrap sys.stdin and sys.stdout to work with unicode.
    if sys.version_info[0] < 3:
        import codecs
        import locale
        encoding = locale.getpreferredencoding()
        sys.stdin = codecs.getreader(encoding)(sys.stdin)
        sys.stdout = codecs.getwriter(encoding)(sys.stdout)

    if len(sys.argv) < 4:
        sys.stderr.write('Usage: %s input_format(tokenize|conllu|horizontal|vertical) output_format(conllu) model_file\n' % sys.argv[0])
        sys.exit(1)

    sys.stderr.write('Loading model: ')
    model = Model.load(sys.argv[3])
    if not model:
        sys.stderr.write("Cannot load model from file '%s'\n" % sys.argv[3])
        sys.exit(1)
    sys.stderr.write('done\n')

    pipeline = Pipeline(model, sys.argv[1], Pipeline.DEFAULT, Pipeline.DEFAULT, sys.argv[2])
    error = ProcessingError()

    # Read whole input
    text = "Desde que los fiscales estadounidenses anunciaron en marzo los cargos contra 50 personas en una amplia investigación de fraude en el sistema de admisión a las universidades, se toparon con un caso misterioso: una familia dice que le pagó a un consultor universitario 6,5 millones de dólares, mucho más que cualquiera de los padres mencionados en la investigación, para que su hija ingresara a la universidad.\n[Si quieres recibir los mejores reportajes de The New York Times en Español en tu correo suscríbete aquí a El Times]\nLa estudiante es Yusi Zhao, quien fue admitida en Stanford en 2017, según una persona que conoce la investigación. Ni ella ni sus padres, que viven en Pekín, han sido acusados, y no está claro si actualmente se les investiga. Stanford rescindió la admisión de Zhao en abril y ya no estudia allí.\nLa persona que conoce la investigación dijo que la familia de Zhao fue presentada al asesor en universidades, William Singer, por un asesor financiero de Morgan Stanley con sede en Pasadena, llamado Michael Wu. Una portavoz de Morgan Stanley dijo que Wu había sido despedido por no cooperar con una investigación interna sobre el asunto y que la firma estaba cooperando con las autoridades. Wu no respondió a una llamada telefónica.\nEn una audiencia judicial en marzo, el fiscal principal en el caso de las admisiones, Eric S. Rosen, dijo que Singer había intentado que Zhao, a quien Rosen no identificó por su nombre, fuera reclutada por Stanford y creó un perfil falso de sus supuestos logros deportivos en vela.\nAl final no fue reclutada pero Rosen dijo que, en parte, fue admitida en Stanford debido a esas credenciales falsas y que, luego de entrar a la universidad, Singer hizo una donación de 500.000 al programa de vela de Stanford.\nSinger se declaró culpable de extorsión y otros cargos, por idear un plan que los fiscales dicen que incluye trampas en los exámenes de ingreso a la universidad y sobornar a entrenadores para reclutar a estudiantes que realmente no eran atletas competitivos.\nEl exentrenador de vela de Stanford, John Vandemoer, se declaró culpable de conspiración para cometer extorsión. Según el testimonio de Rosen en su audiencia de declaración de culpabilidad, Vandemoer no ayudó a la aplicación de Zhao “de ninguna manera material”, sino que aceptó otras donaciones de Singer a su programa con la finalidad de reservar puestos de reclutamiento para los clientes de Singer. El abogado de Vandemoer, Robert Fisher, declinó hacer comentarios.\nZhao, cuya identidad fue dada a conocer por primera vez por Los Angeles Times, parece haber participado en una conferencia reciente organizada por Princeton-U.S. China Coalition. En su biografía en el sitio web del grupo dice que quiere especializarse en psicología y estudios del este de Asia y que está interesada en las políticas educativas de China. Agregó que esperaba involucrarse en el gobierno chino en el futuro.\nZhao trabajó durante un verano reciente en un laboratorio de investigación de biología y química en Harvard, bajo la dirección de Daniel G. Nocera, profesor de energía en la universidad. Nocera dijo en un correo electrónico que a Zhao no se le pagaba y que trabajaba para recibir crédito académico en Stanford.\nEl miércoles en el campus de Stanford, algunos estudiantes no parecieron perturbarse por la noticia de que una persona había pagado millones para estudiar allí. Tamara Morris, una joven de 20 años que estudia ciencia política y estudios afroamericanos, dijo que desconocía el caso Zhao.\nLa conversación sobre el escándalo de admisión a la universidad se había calmado en las últimas semanas en el campus, dijo Morris, y agregó que la noticia no la molestó particularmente. “Yo sé cómo entré”, dijo."
    text = re.sub(r'\n+', '\n\n', text)

    text2 = "La madre de una estudiante china que ingresó a la Universidad de Stanford dijo que la familia le dio 6,5 millones de dólares al hombre en el centro de un fraude masivo de admisión a la universidad como una donación para becas y fondos.\nCincuenta personas han sido acusadas en la estafa de admisión a universidades más grande jamás procesada en Estados Unidos. El escándalo ha atrapado a celebridades como Felicity Huffman y Lori Loughlin, ninguna de las cuales gastó tanto como la mujer de nacionalidad china.\nEn una declaración proporcionada a través de su abogado, la mujer identificada como la señora Zhao admite haber otorgado 6,5 millones de dólares a la fundación de William “Rick” Singer, el líder de la estafa.\nZhao dijo que había buscado servicios de asesoría universitaria porque no estaba familiarizada con el proceso de admisión para las universidades en Estados Unidos.\nDespués de que su hija llegó a Stanford, según la declaración, Singer le pidió una donación a la universidad a través de su fundación. Singer le dijo que la donación era “para los sueldos del personal académico, becas, programas de atletismo y para ayudar a los estudiantes que de otra manera no podrían permitirse asistir a Stanford”, dijo Zhao.\nLa declaración de su abogado, Vincent Law, no proporcionó su nombre de pila ni información sobre su esposo o su hija.\nprinceton-campus\nPero en un video de 2017 publicado en la popular plataforma china Douyu, una estudiante que se identificó como Yusi Zhao dijo que fue admitida en Stanford a través de su propio trabajo.\n“Este año me admitieron en Stanford. Tengo mucha suerte de decirlo”, dijo Zhao en el video de 90 minutos. “Quiero decirles a todos que gané mi admisión en Stanford a través de mi propio esfuerzo… no me estaba yendo bien académicamente cuando estaba en la escuela primaria, pero ahora puedo ir a Stanford después de trabajar duro”.\nYusi Zhao es hija del multimillonario chino Zhao Tao, presidente de Shandong Buchang Pharmaceuticals, según el Stanford Daily.\nZhao Tao respondió a los informes de los medios de comunicación en un comunicado publicado en el sitio web de su compañía diciendo: “El estudio de mi hija en EE.UU. es un problema personal y familiar”, y no tiene vínculos con Shandong Buchang Pharmaceuticals.\nLa madre dice que fue víctima de la estafa\nAunque la compañía de Singer proporcionó “servicios de asesoría educativa”, dijo, no garantizaba la admisión en ninguna escuela. Su hija tiene un historial de “buen rendimiento académico y logros extracurriculares”, y recibió ofertas de varias universidades de Estados Unidos, dijo.\n“Desde que se informaron ampliamente los asuntos relacionados con el señor Singer y su fundación, la señora Zhao notó que la han engañado, se han aprovechado su generosidad y su hija ha sido víctima de estafa”, se lee en la declaración.\nEl exasesor de Morgan Stanley Michael Wu dijo que refirió a los padres a Singer.\n“El Sr. Wu fue presentado a Rick Singer a través de Morgan Stanley como una fuente confiable. Singer, en un esfuerzo por llenar sus propios bolsillos con millones de dólares de un cliente de Morgan Stanley, dijo en un correo electrónico, antes de realizar cualquier pago, que el dinero se pagaría a la Universidad de Stanford “para dotar a los sueldos y becas del personal” y “para financiar los programas especiales de atletismo y los programas de proyección de la universidad para ayudar a los necesitados a que puedan asistir a Stanford”, dijo Wu en una declaración a través de su abogado.\nUna portavoz de Morgan Stanley le dijo a CNN que la compañía está cooperando con los investigadores y dijo que Wu había sido despedido de su trabajo.\nEn un comunicado, la Universidad de Stanford dijo que no recibió los millones de dólares y que no lo sabía antes de que se informara ampliamente.\n“Es importante aclarar que Stanford no recibió $ 6,5 millones de Singer, o de la familia de un estudiante que trabaja con Singer”, dijo. “Stanford no estaba al tanto de este pago de $ 6,5 millones de la familia a Singer”.\nLa estudiante, sus padres y el hombre que los presentó no han sido acusados en el escándalo.\nLos fiscales denuncian a 50 personas\nDe las 50 personas acusadas, 33 son padres. Se les acusa de conspirar para usar su riqueza para obtener una ventaja en el sistema de admisión a la universidad. Un total de 17 padres adinerados, incluida Loughlin, presentaron formalmente declaraciones de culpabilidad en un tribunal federal de Boston esta semana.\nLos fiscales alegan que la actriz y su esposo, Mossimo Giannulli, pagaron medio millón de dólares a una caridad falsa para que sus dos hijas fueran admitidas en la Universidad del Sur de California, designándolas falsamente como reclutas de sus equipos deportivos.\nLa actriz de “Full House” es la figura de más alto perfil atrapada en un escándalo que ha involucrado a docenas de padres adinerados, entrenadores universitarios y administradores de exámenes estandarizados.\nHuffman estuvo entre más de una docena de padres que se declararon culpables de un cargo de conspiración para cometer fraude el mes pasado. A cambio de la declaración de culpabilidad, los fiscales dijeron que recomendarán el encarcelamiento en el “extremo bajo” del rango de sentencia y no presentarán más cargos contra ella.\nSinger se declaró culpable y está cooperando con el gobierno.\nEl plan maestro de la universidad obtuvo 25 millones de dólares\nSinger era dueño de un negocio de preparación y asesoramiento universitario, y se desempeñó como presidente ejecutivo de Key Worldwide Foundation, la organización benéfica conectada a este.\nA través de esas organizaciones, supuestamente facilitó las trampas en las pruebas estandarizadas y sobornó a los entrenadores y administradores de la universidad para que designaran falsamente a los niños como atletas reclutados, incluso si no practicaban ese deporte.\nLas estrellas de Hollywood, los directores ejecutivos principales, los entrenadores universitarios y los administradores de exámenes estandarizados supuestamente participaron en el esquema para engañar a los exámenes y admitir a los estudiantes en instituciones líderes como atletas, independientemente de sus habilidades. Al menos ocho universidades, entre ellas Stanford y la Universidad del Sur de California, se mencionan en una acusación federal y una denuncia penal.\nLos padres pagaron a Singer alrededor de 25 millones de dólares como parte del plan, dijo Andrew Lelling, el abogado de Estados Unidos para Massachusetts. Parte de ese dinero fue a los administradores de pruebas y entrenadores involucrados en la estafa, dijeron los fiscales."
    text2 = re.sub(r'\n+', '\n\n', text2)
    # text = ''.join(sys.stdin.readlines())

    # Process data
    parse_table, parse_pos = udpipe_parse(text)

    print(parse_pos['PROPN'])

    parse_table2, parse_pos2 = udpipe_parse(text2)

    print(parse_pos2['PROPN'])

    propn_sim = jacc_sim(parse_pos['PROPN'], parse_pos2['PROPN'])
    print(propn_sim)

