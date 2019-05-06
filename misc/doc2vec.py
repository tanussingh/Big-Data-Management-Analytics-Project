#this program trains a doc2vec model using the old mongodb data.

#model is saved on the disk. the file is called my_doc2vec_model
import datetime

import gensim
from bson import ObjectId
from nltk.corpus import stopwords
import json
from pymongo import MongoClient
from tqdm import tqdm
# from gensim.test.utils import get_tmpfile
from gensim.models.callbacks import CallbackAny2Vec
import time


class EpochLogger(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch", self.epoch, " started at", datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))

    def on_epoch_end(self, model):
        print("Epoch", self.epoch, "finished at", datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
        self.epoch += 1


epoch_logger = EpochLogger()

if __name__ == "__main__":
    # shouldn't need to download always
    # nltk.download('stopwords')
    stop_words = stopwords.words('spanish')

    # print("k")
    lee_train_file = "train.txt"
    lee_test_file = "test.txt"


    # The CustomJSONEncoder written by Tanu/Mavis

    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return json.JSONEncoder.default(self, o)


    # for some reason i could not get the database name as big_data so it's training2. Change it to big_data or any name of your choice
    # script to collect data from mongodb. this collects everything from the database
    database_name = 'big_data'
    client = MongoClient("localhost", 27017)
    dbArticles = client[database_name]
    collection_Article = dbArticles['spanish_articles']

    print("Reading training data from Mongo:")
    # a list for the training data
    train = []
    count = 0
    query = {"date_publish": {"$gt": datetime.datetime(2019, 1, 1)}}
    for i, story in tqdm(enumerate(collection_Article.find(query))):
        t = story['text']
        # some docs may have no text
        if t is None:
            continue
        ti = gensim.utils.simple_preprocess(t)
        ti = [word for word in ti if word not in stop_words]
        train.append(gensim.models.doc2vec.TaggedDocument(
            ti, [story['url']]))
        count += 1

    # a hack
    # this adds the 2 articles we know which talk about the same thing.
    s1 = "La madre de una estudiante china que ingresó a la Universidad de Stanford dijo que la familia le dio 6,5 millones de dólares al hombre en el centro de un fraude masivo de admisión a la universidad como una donación para becas y fondos.Cincuenta personas han sido acusadas en la estafa de admisión a universidades más grande jamás procesada en Estados Unidos. El escándalo ha atrapado a celebridades como Felicity Huffman y Lori Loughlin, ninguna de las cuales gastó tanto como la mujer de nacionalidad china.En una declaración proporcionada a través de su abogado, la mujer identificada como la señora Zhao admite haber otorgado 6,5 millones de dólares a la fundación de William “Rick” Singer, el líder de la estafa.Zhao dijo que había buscado servicios de asesoría universitaria porque no estaba familiarizada con el proceso de admisión para las universidades en Estados Unidos.Después de que su hija llegó a Stanford, según la declaración, Singer le pidió una donación a la universidad a través de su fundación. Singer le dijo que la donación era “para los sueldos del personal académico, becas, programas de atletismo y para ayudar a los estudiantes que de otra manera no podrían permitirse asistir a Stanford”, dijo Zhao.La declaración de su abogado, Vincent Law, no proporcionó su nombre de pila ni información sobre su esposo o su hija.Pero en un video de 2017 publicado en la popular plataforma china Douyu, una estudiante que se identificó como Yusi Zhao dijo que fue admitida en Stanford a través de su propio trabajo.“Este año me admitieron en Stanford. Tengo mucha suerte de decirlo”, dijo Zhao en el video de 90 minutos. “Quiero decirles a todos que gané mi admisión en Stanford a través de mi propio esfuerzo… no me estaba yendo bien académicamente cuando estaba en la escuela primaria, pero ahora puedo ir a Stanford después de trabajar duro”.Yusi Zhao es hija del multimillonario chino Zhao Tao, presidente de Shandong Buchang Pharmaceuticals, según el Stanford Daily.Zhao Tao respondió a los informes de los medios de comunicación en un comunicado publicado en el sitio web de su compañía diciendo: “El estudio de mi hija en EE.UU. es un problema personal y familiar”, y no tiene vínculos con Shandong Buchang Pharmaceuticals."
    s2 = "Desde que los fiscales estadounidenses anunciaron en marzo los cargos contra 50 personas en una amplia investigación de fraude en el sistema de admisión a las universidades, se toparon con un caso misterioso: una familia dice que le pagó a un consultor universitario 6,5 millones de dólares, mucho más que cualquiera de los padres mencionados en la investigación, para que su hija ingresara a la universidad.[Si quieres recibir los mejores reportajes de The New York Times en Español en tu correo suscríbete aquí a El Times]La estudiante es Yusi Zhao, quien fue admitida en Stanford en 2017, según una persona que conoce la investigación. Ni ella ni sus padres, que viven en Pekín, han sido acusados, y no está claro si actualmente se les investiga. Stanford rescindió la admisión de Zhao en abril y ya no estudia allí.La persona que conoce la investigación dijo que la familia de Zhao fue presentada al asesor en universidades, William Singer, por un asesor financiero de Morgan Stanley con sede en Pasadena, llamado Michael Wu. Una portavoz de Morgan Stanley dijo que Wu había sido despedido por no cooperar con una investigación interna sobre el asunto y que la firma estaba cooperando con las autoridades. Wu no respondió a una llamada telefónica.EXPLORA NYTIMES.COM/ES La sorpresa de las mujeres de La PazEn una audiencia judicial en marzo, el fiscal principal en el caso de las admisiones, Eric S. Rosen, dijo que Singer había intentado que Zhao, a quien Rosen no identificó por su nombre, fuera reclutada por Stanford y creó un perfil falso de sus supuestos logros deportivos en vela.Al final no fue reclutada pero Rosen dijo que, en parte, fue admitida en Stanford debido a esas credenciales falsas y que, luego de entrar a la universidad, Singer hizo una donación de 500.000 al programa de vela de Stanford.Singer se declaró culpable de extorsión y otros cargos, por idear un plan que los fiscales dicen que incluye trampas en los exámenes de ingreso a la universidad y sobornar a entrenadores para reclutar a estudiantes que realmente no eran atletas competitivos.El exentrenador de vela de Stanford, John Vandemoer, se declaró culpable de conspiración para cometer extorsión. Según el testimonio de Rosen en su audiencia de declaración de culpabilidad, Vandemoer no ayudó a la aplicación de Zhao “de ninguna manera material”, sino que aceptó otras donaciones de Singer a su programa con la finalidad de reservar puestos de reclutamiento para los clientes de Singer. El abogado de Vandemoer, Robert Fisher, declinó hacer comentarios.Zhao, cuya identidad fue dada a conocer por primera vez por Los Angeles Times, parece haber participado en una conferencia reciente organizada por Princeton-U.S. China Coalition. En su biografía en el sitio web del grupo dice que quiere especializarse en psicología y estudios del este de Asia y que está interesada en las políticas educativas de China. Agregó que esperaba involucrarse en el gobierno chino en el futuro.Zhao trabajó durante un verano reciente en un laboratorio de investigación de biología y química en Harvard, bajo la dirección de Daniel G. Nocera, profesor de energía en la universidad. Nocera dijo en un correo electrónico que a Zhao no se le pagaba y que trabajaba para recibir crédito académico en Stanford.El miércoles en el campus de Stanford, algunos estudiantes no parecieron perturbarse por la noticia de que una persona había pagado millones para estudiar allí. Tamara Morris, una joven de 20 años que estudia ciencia política y estudios afroamericanos, dijo que desconocía el caso Zhao.La conversación sobre el escándalo de admisión a la universidad se había calmado en las últimas semanas en el campus, dijo Morris, y agregó que la noticia no la molestó particularmente. “Yo sé cómo entré”, dijo."
    s3 = "funcionario correos autor teatro considerable éxito ámbito independiente preso político tras guerra civil humorista pionero animación españa supuesto historietista consagrado maestros cómic español debe pareja críos gamberros divertido varias generaciones lectores principios tras abandonar cárcelpor haber trabajado república revista esquellot cencerro cómic escobar dibujaba niñez facetas artísticas embargo enroló allí alumbró hermanos zapatilla convertirían célebres autores tebeos españa losse encuentran historietas mudas max und moritz dibujadas wilhelm busch mediados siglo xix rudolf dirks adaptó the katzenjammer kids tira dos gemelos gamberros publicaba new york world joseph pulitzer escobar recogió aquella idea mucha agudeza adornó unque convertía aquellos críos revoltosos personajes perfectamente identificables lectores españoles increíble parezca colegio suspensos equivalían efectivamente calabazas ello unía particular estilo heredero deque triunfaba francia bélgica ilustrador valenciano paco roca destaca trazo elegante dibujante catalán embargo punto irregular dejaba caer obras maestras mejores peculiar personaje siempre hambriento nació casi par zipi zape reflejó mejor ningún miseria posguerra española pesar ser cómico punto amargo especie chaplin comenta roca zipi zape carpanta conocidos escobar creó treintena personajes petra criada perro toby pasando doña tula suegra publicando largo medio siglo páginas bruguera escobar veterano pulgarcito revista empezó publicar historietas personajes pasarían historia cómic español mortadelo filemón agencia información partir entonces comparación par generaciones joven escobar permanente casi inevitable ambos seguirían carreras paralelas bruguera ochenta grijalbo ediciones hiciera cargo catálogo ambas memoria escobar librado alargada sombra ibáñez siquiera centenario coincide aniversario lanzamiento mortadelo filemón pese zipi zape contaba seguidores fieles paco roca destaca ternura punto aventura historietas dice seguidor encima incluso mortadelo filemón amigos pasado cómics vértice superhéroes americanos seguía zipi zipe afirma primera toma contacto género tipo cómic respeto muchísimo señala gallego alberto vázquez dibujante relativamente alejado presupuestos escobar vázquez destaca escobar cuyas historietas enseñaron códigos esenciales lenguaje cómic varias generaciones dibujantes españoles universalidad resalta especialmente si cuenta historietas escobar inspiradas contexto concreto seguían divirtiendo décadas después calabazas aceite ricino cuarto ratones obsoleto funcionaba quizás representa críos querían ser comenta roca empezaba leer zipi zape principios lenguaje personajes propio ocasiones años aunque seguidores consideran parte encanto ocupa lugar destacado aunque tiempo releo superlópez jan confiesa roca superlópez generación definitivamente moderno incluso mortadelo filemón gemelos gamberros colocaron escobar mejores cómic español"
    s1 = s1.split(" ")
    s1 = [word for word in s1 if word not in stop_words]
    s2 = s2.split(" ")
    s2 = [word for word in s2 if word not in stop_words]
    s3 = s3.split(" ")
    s3 = [word for word in s3 if word not in stop_words]

    '''
    train.append(gensim.models.doc2vec.TaggedDocument(
        s1, [count]))
    count += 1
    train.append(gensim.models.doc2vec.TaggedDocument(
        s2, [count]))
    
    print(train)
    
    '''

    # loading and training the gensim doc2vec model.
    # vector size, min count and epochs have not been changed. directly from the author of gensim
    model = gensim.models.doc2vec.Doc2Vec(vector_size=5000, min_count=2, epochs=25)

    print("building vocabulary")
    model.build_vocab(train)

    model.train(train, total_examples=model.corpus_count,
                epochs=model.epochs, callbacks=[epoch_logger])

    print("Done with model")
    # now we create an inferred vector and compute ranks for each of the documents
    # as it is from github
    ranks = []
    second_ranks = []
    for doc_id in range(len(train)):
        inferred_vector = model.infer_vector(train[doc_id].words)
        sims = model.docvecs.most_similar(
            [inferred_vector], topn=len(model.docvecs))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)

        second_ranks.append(sims[1])

    print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train[doc_id].words)))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims) // 2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' %
              (label, sims[index], ' '.join(train[sims[index][0]].words)))

    sud = model.docvecs.similarity_unseen_docs(
        model, s1, s2, alpha=None, min_alpha=None, steps=None)

    print("sud ")
    print(sud)

    fname = ("./doc2vec_2019")
    model.save(fname)
