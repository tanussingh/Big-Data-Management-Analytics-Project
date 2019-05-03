import sys
import re
import json
from ufal.udpipe import Model, Pipeline, ProcessingError  # pylint: disable=no-name-in-module

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
text = "Resultados NBA del viernes: Indiana 118 Portland 113\nOrlando 103 Oklahoma City 102\nLA Lakers 112 Philadelphia 98 Cleveland 115 Washington 113 Boston 99 Sacramento 89 Detroit 111 Brooklyn 95 Pelicans 98 - Timberwolves 91 NY Knicks 117 Denver 90 Dallas 103 Utah 81\nEsta vez sí, el veterano base canadiense Steve Nash reivindicó su condición de líder y jugó su mejor partido en lo que va de temporada con Los Ángeles Lakers a los que guió al triunfo a domicilio (98-112) ante Sixers.\nNash, aunque sólo jugó 28 minutos, se encargó de encarrilar el partido en el segundo cuarto al conseguir un parcial de 29-35 y los Lakers sentenciaron en el cuarto (13-25), mientras que el veterano base lograba 19 puntos (8-15, 0-2, 3-4) --mejor marca de la temporada-- repartió cinco asistencias y capturó cuatro rebotes.\nOtros cinco jugadores de los Lakers, incluidos tres titulares, también tuvieron números de dos dígitos, con el alero Wesley Johnson y el pívot reserva Chris Kaman, que aportaron 17 puntos cada uno.\nKaman hizo una excelente labor bajo los aros al capturar ocho rebotes, los mismos que tuvo el ala-pivot novato Ryan Kelly, que también anotó 15 puntos, y Johnson recuperó cinco balones y puso tres tapones.\nEl base Steve Blake se encargó de dirigir el juego y logró 14 tantos, ocho asistencias, cuatro rebotes y dos recuperaciones de balón.\nA pesar de las bajas de sus mejores encestadores, el ala-pívot español Pau Gasol, el escolta Kobe Bryant y el escolta-alero Nick Young, todos lesionados, los Lakers jugaron su mejor baloncesto de equipo al conseguir un 51 (45-89) por ciento de acierto en los tiros de campo y el 44 (8-18) de triples.\nLa victoria, segunda consecutiva que consiguen los Lakers (18-32) después de siete derrotas seguidas, no evita que sigan en el último lugar de la División Pacífico.\nLos Sixers dominaron a los Lakers en los balones por alto al capturar 50 rebotes por 40, pero no tuvieron la misma eficacia encestadora y ahí estuvo la diferencia final en el marcador.\nDerrota sobre la bocina de Thunder El alero Tobías Harris se convirtió en el protagonista de la canasta que permitió a los Magic de Orlando vencer 103-102 a los Thunder de Oklahoma City cuando sonaba la bocina final del partido. Los árbitros tuvieron que revisar la jugada y asegurarse de que el balón salió de la mano de Harris antes de que sonase la bocina y confirmaron que la canasta fue válida. Los Thunder tuvieron la posibilidad de haber conseguido la victoria si Durant no hubiese fallado 2,9 segundos antes el tiro el suspensión que el rebote fue capturado por el escolta novato Vitor Oladipo, que pasó el balón al alero Maurice Harkless y en el saque rápido se lo dio a Harris, máximo encestador del equipo con 18 tantos. El pívot suizo Nikola Vucevic fue el líder en el juego bajo los aros al conseguir un doble-doble de 10 puntos, 10 rebotes y dos asistencias, que ayudaron a los Magic a romper una racha de cinco derrotas consecutivas que tenían en los duelos contra los Thunder. Una vez más, el alero Kevin Durant, a pesar de fallar el tiro que dio la oportunidad a los Magic de conseguir la victoria, volvió a ser el líder del ataque de los Thunder al aportar un doble-doble de 29 puntos, 12 asistencias, cinco rebotes y perdió seis balones. Durant se convirtió en el cuarto jugador que esta temporada logra al menos 25 puntos y 10 asistencias y empató su mejor marca como profesional al dar 12 pases de anotación, que estableció el 1 de diciembre del 2013 ante los Timberwolves de Minnesota. El ala-pívot congoleño, nacionalizado español, Serge Ibaka, volvió a mostrar el gran momento de juego ofensivo por el que atraviesa al aportar 26 puntos y capturar seis rebotes, incluido cinco defensivos, después de disputar 40 minutos. Ibaka anotó 10 de 13 tiros de campo, incluido un triple, encestó 5 de 6 desde la línea de personal, dio una asistencia e impuso su poder bajo los aros al poner cinco tapones. Pero no fueron suficientes a la hora de evitar la derrota (40-12), que les rompió la racha de dos triunfos consecutivos, y fue la segunda en los últimos 10 partidos disputados. Los Thunder siguen como líderes de la División Noroeste.\nCalderón dirigió el ataque en la victoria de Dallas Excelenta labor de equipo la que realizaron los Mavericks de Dallas que tuvieron al escolta Monta Ellis y al ala-pívot alemán Dirk Nowitzki como los líderes encestadores y al base español José Manuel Calderón de director del juego que los guió al triunfo fácil de 103-81 ante los Jazz de Utah. Ellis anotó 22 puntos y Nowitzki, aunque jugó sólo 26 minutos, logró otros 20 que los dejaron al frente de la lista de cuatro jugadores titulares que tuvieron números de dos dígitos, entre ellos Calderón que aportó 12, los mismos que tuvo el pívot haitiano Samuel Dalembert. Calderón, que jugó 33 minutos, encestó 4 de 11 tiros de campo, incluidos cuatro triples en siete intentos, y no fue a la línea de personal. El base de Villanueva de la Serena se encargó también de dirigir el ataque de los Mavericks y repartió siete asistencias --líder del equipo en esa faceta del juego--, capturó cuatro rebotes, y recupero dos balones. La victoria fue la cuarta consecutiva que lograron los Mavericks (30-21) y les permitió empatar la mejor racha ganadora en lo que va de temporada, además de ponerse por primera vez nueve juegos arriba del par de la marca, algo que sólo ha conseguido por dos veces desde la temporada del 2010-11 cuando ganaron el título de campeones de liga. El ala-pivote Marvin Williams surgió con 21 puntos, incluidos cinco triples, y cinco rebotes, pero no fueron suficientes a la hora de evitar la cuarta derrota consecutiva que sufrieron los Jazz (16-33) que ya están en la lista de los equipos de lotería.\nLos Pelicans se imponen a los 'Wolves' El ala-pivote Anthony Davis vivió una jornada completa al ser el jugador que sustituya a Kobe Bryant (lesionado) en el equipo de la Conferencia Oeste para el Partido de las Estrellas y los Pelicans de Nueva Orleans lograron el triunfo(98-91) ante los Timberwolves de Minnesota. Davis respondió como líder indiscutible de los Pelicans al conseguir un doble-doble de 26 puntos y 10 rebotes, incluidos ocho defensivos, que fueron claves en la victoria de los Pelicans (22-27). El acierto ofensivo de Davis permitió a los Pelicans remontar una desventaja de 10 tantos. Los Pelicans, que anotaron 13 de 20 tiros de campo en el cuarto periodo, superaron a los Timberwolves con parcial de 37-20, que cambió la historia del partido. El ala-pivote estrella de los Timberwolves, Kevin Love, no perdió el duelo individual con Davis al conseguir un doble-doble de 26 puntos, 19 rebotes y tres asistencias, pero tampoco pudo evitar la derrota de su equipo, la segunda consecutiva que sufrieron. El base español Ricky Rubio no estuvo acertado en los tiros a canasta y aportó 11 puntos en los 33 minutos que disputó. Rubio anotó 3 de 10 tiros de campo, incluido un triple en dos intentos, y estuvo perfecto desde la línea de personal al encestar 4 de 4. Además de repartir seis asistencias, capturar cinco rebotes, incluidos cuatro defensivos, recuperó un balón, perdió tres y puso un tapón."
text = re.sub(r'\n+', '\n\n', text)
# text = ''.join(sys.stdin.readlines())

# Process data
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

print(parse_table)
print(parse_pos)
