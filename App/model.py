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
from DISClib.DataStructures import listiterator as it
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


def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    severityIndex= datentry['severityIndex']
    severity=  m.get(severityIndex, accident['Severity'])
    if (severity is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverity'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(severity)
        lt.addLast(entry['lstseverity'], accident)
    return datentry


def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareseverity)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newSeverityEntry(severity, accident):
    severityentry= {'severity':None, 'lstseverity':None}
    severityentry['severity']= severity
    severityentry['lstseverity']=lt.newList('SINGLELINKED', compareseverity)
    return severityentry

                                    

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
        severitymap = me.getValue(accidentdate)['severityIndex']
        numoffenses = m.get(severitymap, severity)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstseverity'])
        return (numoffenses)


def getAccidentsByState(analyzer,initialDate,finalDate):
    rango = om.values(initialDate,finalDate)
    
    histograma_estado = {'Estado':None,'accidents':None}
    
    histograma_fecha = {'Fecha':None,'accidents':None}
    
    iter = lit.newIterator(histograma_estado)
    while lit.hasNext(iter):
        entry = lit.next(iter)
        if entry['State'] not in histograma_estado:
            histograma_estado['Estado'] = 1
        else:
            histograma_estado['Estado'] += 1
    
    iter = lit.newIterator(histograma_fecha)
    while lit.hasNext(iter):
        date = lit.next(iter)
        if date['dateIndex'] not in histograma_fecha:
            histograma_fecha['Fecha'] = 1
        else: 
            histograma_fecha['Fecha'] += 1

    maximo_estado = max(histograma_estado.values)
    llaves_estado = list(histograma_estado.keys)
    iter = lit.newIterator(llaves_estado)
    while lit.hasNext(iter):
        state = lit.next(iter)
        if histograma_estado[llaves_estado] == maximo_estado:
            respuesta_estado = llaves_estado.index(maximo_estado)
    
    maximo_fecha = max(histograma_fecha.values)
    llaves_fecha = list(histograma_fecha.keys)
    iter = lit.newIterator(llaves_estado)
    while lit.hasNext(iter):
        fecha = lit.next(iter)
        if histograma_fecha[llaves_fecha] == maximo_fecha:
            respuesta_fecha = llaves_fecha.index(maximo_fecha)
    
    return ("El estado con mayores accidentes en el rango dado es: "+str(respuesta_estado)+"\n"
            "La fecha con mayores accidentes es: "+str(respuesta_fecha))

<<<<<<< HEAD
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

def getAccidentsByHour(analyzer, initialhour, finalhour):
=======
def getAccidentsByHour(analyzer, initialhour, finalhour): 
>>>>>>> e94e4f615b316773a300d5d0bbb923ce0634218a
    lst = om.values(analyzer['dateIndex'])
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate,'%H:%M:%S')
    map_horas = om.newMap(omaptype='BST',comparefunction=compareHours)
    om.put(map_horas,accidentdate.hour(),lst)
    return om.values(map,initialhour,finalhour)
   

def getAccidentsBySeverity(analyzer, date): #REQUERIMIENTO 1 

    accidentdate = om.get(analyzer['dateIndex'], date)
    severidad1=getAccidentsByRangeCode(analyzer, date, "1")
    severidad2=getAccidentsByRangeCode(analyzer, date, "2")
    severidad3=getAccidentsByRangeCode(analyzer, date, "3")
    severidad4=getAccidentsByRangeCode(analyzer, date, "4")

    if severidad1==None:
        severidad1=0
    if severidad2==None:
        severidad2=0
    if severidad3==None:
        severidad3=0
    if severidad4==None:
        severidad4=0

    TotalAccidentes=severidad1+severidad2+severidad3+severidad4
    print("\nFECHA: " + str(date))
    print("SEVERIDAD"+"\t"+"NUM. ACCIDENTES")
    print("--------------------------------------")
    print("1"+"\t"+"\t"+str(severidad1))
    print("2"+"\t"+"\t"+str(severidad2))
    print("3"+"\t"+"\t"+str(severidad3))
    print("4"+"\t"+"\t"+str(severidad4))
    print("TOTAL DE ACCIDENTES:"+ str(TotalAccidentes))

    return(accidentdate) 

        
def getAccidentsByRangeSeverity(analyzer, initialDate, finalDate): #REQUERIMIENTO 3
    accidentdate=getAccidentsByRange(analyzer, initialDate, finalDate)
    
    i=0
    tamanio= lt.size(accidentdate)
    j=1
    # print(accidentdate)
    while i <tamanio:
        fecha=(lt.getElement(accidentdate, i))
        
        while j<=4:
            if j==1:
                severidad1= getAccidentsByRangeCode(analyzer, fecha, "1")
                if severidad1==None:
                    severidad1=0
            if j==2:
                severidad2=getAccidentsByRangeCode(analyzer, fecha, "2")
                if severidad2==None:
                    severidad2=0
            if j==3:
                severidad3=getAccidentsByRangeCode(analyzer, fecha, "3")
                if severidad3==None:
                    severidad3=0
            if j==4:
                severidad4=getAccidentsByRangeCode(analyzer,fecha, "4")
                if severidad4==None:
                    severidad4=0
            
            j+=1
        i+=1 
        TotalAccidentes=severidad1+severidad2+severidad3+severidad4   
    

  
    print("\nRANGO FECHAS: " + str(initialDate)+ "- "+ str(finalDate))
    print("SEVERIDAD"+"\t"+"NUM. ACCIDENTES")
    print("--------------------------------------")
    print("1"+"\t"+"\t"+str(severidad1))
    print("2"+"\t"+"\t"+str(severidad2))
    print("3"+"\t"+"\t"+str(severidad3))
    print("4"+"\t"+"\t"+str(severidad4))
    print("\nTOTAL DE ACCIDENTES:"+ str(TotalAccidentes))
    
        
       
    
    
  

    
    
    
    
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
def compareHours(hour1,hour2):

    if (hora1 == hora2):
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
    



