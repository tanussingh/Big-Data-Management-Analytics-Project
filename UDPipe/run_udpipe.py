import sys

from ufal.udpipe import Model, Pipeline, ProcessingError # pylint: disable=no-name-in-module

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
text = 'El Consejo de Estado suspendió temporalmente los efectos del laudo arbitral que obliga a Metrocali a pagar $110.000 millones al operador GIT Masivo, por las pérdidas que ha sufrido dicho concesionario durante la operación del MÍO.\n\nA través de un auto interlocutorio, que fue notificado el jueves pasado, el tribunal supremo resolvió aceptar la demanda de nulidad parcial que el ente gestor del MÍO puso contra el laudo, proferido el 29 de noviembre del 2018 por el tribunal de arbitramento de la Cámara de Comercio de Cali, constituido para dirimir las controversias contractuales entre Metrocali y GIT.\n\n“Nuestra estrategia jurídica fue interponer un recurso de anulación a este laudo, encontramos unas bases en las cuales evidenciamos que esa sentencia de ese tribunal no estaba sujeta propiamente a derecho... los efectos de ese laudo están suspendidos hasta que el Consejo de Estado decida si esa sentencia de ese tribunal corresponde o no en derecho”, dijo Francisco Borrero, secretario general de Asuntos Jurídicos de Metrocali.\n\nEl funcionario indicó que esperan que en un término no mayor a siete meses el Consejo de Estado se pronuncie nuevamente. Asimismo, indicó que están iniciando una acción de tutela con apoyo del equipo jurídico de la Alcaldía de la Defensa Nacional Judicial, con el fin de revertir los efectos del laudo del tribunal de arbitramento.\n\n“Es importante indicar que esto no afecta el servicio que estamos prestando, en los últimos dos años Metrocali logró un acuerdo con los cuatro operadores para mejorar el sistema y recuperar la flota, incluyendo a GIT Masivo”, afirmó Borrero. \n\nEl País intentó contactar a Enrique Wolf, gerente de GIT Masivo, para conocer su opinión, pero no hubo respuesta.\n\nLea además: Tribunal de arbitramento obliga a Metrocali a pagar $110.000 millones a GIT Masivo'

# Process data
processed = pipeline.process(text, error)
if error.occurred():
    sys.stderr.write("An error occurred when running run_udpipe: ")
    sys.stderr.write(error.message)
    sys.stderr.write("\n")
    sys.exit(1)
sys.stdout.write(processed)
