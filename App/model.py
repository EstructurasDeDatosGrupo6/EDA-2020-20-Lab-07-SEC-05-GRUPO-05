"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import linkedlistiterator as lit
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
                                      

    return analyzer
# Funciones para agregar informacion al catalogo


def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer


def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map


def addDateIndex(dateentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = dateentry['lstaccidents']
    lt.addLast(lst, accident)
    severityIndex= dateentry['dateIndex']
    severity=  m.get(severityIndex, accident['Severity'])
    if (severity is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverity'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(severity)
        lt.addLast(entry['lstseverity'], accident)
    return dateentry


def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'dateIndex': None, 'lstaccidents': None}
    entry['dateIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareseverity)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newSeverityEntry(severity, accident):
    severityentry= {'Severity':None, 'lstseverity':None}
    severityentry['Severity']= severity
    severityentry['lstseverity']=lt.newList('SINGLELINKED', compareseverity)
    return severityentry

                                    
# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================
def AccidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])


def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    return lst


def getAccidentsByRangeCode(analyzer, initialDate, severity):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    accidentdate = om.get(analyzer['dateIndex'], initialDate)
    if accidentdate['key'] is not None:
        print(accidentdate)
        severitymap = me.getValue(accidentdate)['Severity']
        numaccidents = m.get(severitymap, severity)
        if numaccidents is not None:
            return m.size(me.getValue(numaccidents)['lstseverity'])
        return 0

<<<<<<< HEAD
def getAccidentsByDate(analyzer, Date):
    
    # offenses=om.get(analyzer['offenses'], )
    accidentdate= om.get(analyzer['dateIndex'], Date)
    # severity= om.get(analyzer, accidentdate['key'])
    # print(accidentdate['key'])
    # print(serveity['Severity'])
    # if accidentdate['key'] is not None:
    #     severitymap=me.getValue(accidentdate)['offenseIndex']
    #     numaccidents= m.getValue(accidentdate)['severityIndex']
    
    #     if numaccidents is not None: 
    #         return m.size(me.getValue(numaccidents['lstseverity']))
    #     else:
    #         return 0
    return accidentdate

def getAccidentsByState(analyzer,initialDate,finalDate):
    lst_rank= lt.newList(datastructure='SINGLE_LINKED',cmpfunction=None)
    lst_keys= lt.newList(datastructure= 'SINGLE_LINKED',cmpfunction=None)
    rango = getAccidentsByRange(analyzer['dateIndex'],initialDate,finalDate)
    lt.addLast(lst_rank,rango)
    histograma = m.newMap(numelements=1000,prime=109345121,maptype='CHAINING',loadfactor=0.5,comparefunction=compareaccidents)
    iter = lit.newIterator(lst_rank)
    while lit.hasNext(iter):
        entry = lit.next(iter)
        if entry['State'] not in histograma:
            entry['State'] = 1
        else:
            entry['State'] += 1
    maximo = max(m.valueSet(lst_rank))
    keys = m.keySet(lst_rank)
    lt.addLast(lst_keys,keys)
    iter = lit.newIterator(lst_keys)
    while lit.hasNext(iter):
        key = lit.next(iter)
        if key == maximo:
            return maximo
        else: 
            return 0
    #Paso 1: completar la lista 
    #Paso 2: Crear un histograma(mapa)-> k:estados v:#accidentes
    #Paso 3: Encontrar el valor mayor 
    #Paso 4: Buscar la lista más grande de accidentes->fecha 
    #Paso 5: Retornar el valor mayor del histograma y la fecha 
=======
def getAccidentsBySeverity(analyzer, Date):

    severityCodes=lt.newList(datastructure="SINGLE_LINKED", cmpfunction=None)
    lt.addLast(severityCodes, 1)
    lt.addLast(severityCodes, 2)
    lt.addLast(severityCodes, 3)
    lt.addLast(severityCodes, 4)

    accidents=lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None)

    for severityCode in severityCodes:
        severity= getAccidentsByRangeCode(analyzer, Date, severityCode)
        lt.addLast(accidents,severity)

    return(accidents)
   
>>>>>>> 5026b7f6f1b80225ba3acdbb1f41016d52060f44


# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareseverity(severity1, severity2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    severity = me.getKey(severity2)
    if (severity1 ==severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1
    
def compareaccidents(accident1, accident2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    accident = me.getKey(accident2)
    if (accident1 ==accident):
        return 0
    elif (accident1 > accident):
        return 1
    else:
        return -1


