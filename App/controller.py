import config as cf
from App import model
import datetime
import csv
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from time import process_time 
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________



def loadData(analyzer, accidentsfile):
    t1_start = process_time()
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8-sig"),
                                delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)
        
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos") 
    return analyzer



# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def AccidentsSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.AccidentsSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRange(analyzer, initialDate.date(),
                                  finalDate.date())


def getAccidentsByRangeCode(analyzer, initialDate,
                         severity):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getAccidentsByRangeCode(analyzer, initialDate.date(),
                                      severity)

def getAccidentsBySeverity (analyzer, Date): #REQUERIMIENTO 1
    
    Date= datetime.datetime.strptime(Date, '%Y-%m-%d')
    return model.getAccidentsBySeverity(analyzer, Date.date())

def getAccidentsByRangeSeverity(analyzer, initialDate, finalDate):

    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRangeSeverity(analyzer, initialDate.date(),
                                  finalDate.date())