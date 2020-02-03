# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""
import pyodbc

global cursor
global conn

module = GetParams("module")

if module == "connectionBDPostgres":

    server = GetParams('server')
    database = GetParams('database')
    username = GetParams('user')
    password = GetParams('password')
    port = GetParams('port')
    

    print(server, database, username, password, port)
    driver = "{PostgreSQL Unicode}"
    
    print(driver)
    try:

        if username and password is not None:

            conn = pyodbc.connect(
                'DRIVER=' + driver + ';SERVER=' + server + ';PORT='+ port + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        else:

            conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT='+ port + ';DATABASE=' + database + ';UID=' + username)
        
        
        conn.setencoding(encoding='utf-8')
        cursor = conn.cursor()
        #Exeception as e raise e me imprime la excepcion en la web de rocketbot
    except Exception as e:
        PrintException()
        raise e

if module == 'QueryBD':

    query = GetParams('query')
    print(query)
    var_ = GetParams('var')
    

    try:

        cursor.execute(query)
            #busco el por que valor comienza el query
        if query.lower().lstrip().startswith("select"):
            typeresult = GetParams("typer")
            data = []
            columns = [column[0] for column in cursor.description]
            
            
            if typeresult.lower() == "json":
                              
                data.append(columns)
                for row in cursor:
                    ob_ = {}
                    t = 0
                    for r in row:
                        ob_[columns[t]] = str(r).strip() + ""
                        t = t + 1
                    data.append(ob_)
            elif typeresult == "array":
                data.append(columns)
                tmp = cursor.fetchall()
                data2 = []
                for r in tmp:
                    tmp2 = []
                    for b in r:
                        tmp2.append(str(b).strip())
                    data2.append(tmp2)
                
                data= data + data2
                
                               

        elif query.lower().startswith(("drop","create",'insert')):
        
             data = True

        else:
            conn.commit()
            data = cursor.rowcount, 'registros afectados'

        conn.commit()
        SetVar(var_, data)

    except Exception as e:
        PrintException()
        raise e
    
