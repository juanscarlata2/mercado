# Mercapi
## Descripcion
Esta aplicación permite interactuar con los archivos de un sistema Linux por medio del protocolo HTTP, permitiendo borrar, obtener data o analizar los archivos en busca de material malicioso por medio de Virustotal.

## Requisitos 
- Un sistema operativo Linux con soporte para el gestor de servicios **_systemctl_**

## Instalación
Solo se requiere Descargar el folder **_Installer_** y ejecutar el script Setup.sh que se encuentra dentro de este:
```bash
cd Installer
sudo chmod +x Setup.sh
sudo ./Setup.sh
```

Una vez ejecutado, _Setup.sh_ solicita un usaurio y contraseña para crear la cuenta con la cual se va a administrar la API

## Gestion de la API
Una vez inatalada mercapi el servicio es iniciado, para acceder al gestor de mercapi se debe ingresar por medio del navegador a:
```sh
http://127.0.0.1:5000
```
Una vez allí, se solicita el usuario y contraseña definidos en la fase de instalación. Si la autenticación es correcta se ingresa al menú de gestion el cual consta de 3 opciones:

### Account
En este submenú es posible cambiar el usuario y contraseña para gestionar la API.
### API key
En este apartado se pueden crear las API Key para poder interactuar con mercapi, del mismo modo se pueden eliminar las API key ya creadas. Solo requiere el nombre quue se le va asignar a la API key y la aplicacion la genera. Es importante almacenar la API key, pues despues de salir de este menu no es posible obtenerla por medio de la interfaz web.

### Virus Total
Se configura la API key para poder interactuar con **_virus Total_**. 
Para poder hacer el análisis de los archivos es necesario configurar este parametro, para solicitar una key se puede seguir la siguiente guia, https://support.virustotal.com/hc/en-us/articles/115002088769-Please-give-me-an-API-key

## Descripcion de la API
## Descripcion de la API
Para poder interactuar con mercapi es necesario contar con una **_API key_** generada por medio de la interfaz web de administracion

### Autenticacion
Todos las peticiones a la mercapi deben tener el API key, esta debe ser enviada por medio de un header llamadado **_API-Key_** como se muestra en el siguiente comando de curl
```sh
    curl --request GET \
      --url http://localhost:5000/api \
      --header 'API-Key: a53MbXL4NeCW18OTZs8rEHAJlZUHfDjaCST9WCK5VK3n2qCZOdE3LIpjSMbbFHkf6q2dOzP_' \
```

### Endpoints 

#### POST /api/exec/delete
Permite eliminar una lista de archivos los cuales se envian por medio de un json en el cuerpo de la petición con el siguiente formato:`{ "files" : ["/file/to/delete/1","/file/to/delete/2]}`

##### Request
```sh
curl --request POST \
      --url http://127.0.0.1:5000/api/exec/delete \
      --header 'content-type: application/json' \
      --header 'API-Key: UNzmCzYp0AnVwJoHZO2xqbFpetaxnrls0ciBidXjgFR2mYyo58xRLgW1oTWd5XEixr52hu-7FFyd7-2TszLajQ' \
      --data '{"files":["/home/kali/test/malware.sh","/home/kali/test/malware2"]}'
```
##### Respuesta
 Si la peticion es exitosa (*Codigo 200*),  responde con el estado de la operación por cada archivo (Deleted o File does not exist):
 `{"/home/kali/test/malware.sh":"Deleted","/home/kali/test/malware2":"File does not exist"}`

####  GET /api/file
Permite traer la metadata de un archivo en espeficico, para definir el archivo se usa el parametro _path_. Entre los datos retornados se encuentran
- *permission*: incluye los permisos del archivo, el propietario y el grupo
- *SHA256*: el hash SHA256 del archivo definido
- *timestamps*: datos relacionados con el tiempo de creación y modificación, entrega el ctime, atime y mtime

##### Request
```sh
curl --request GET \
      --url http://localhost:5000/api/file?path=/home/kali/test/malware2.sh\ 
      --header 'API-Key: a53MbXL4NeCW18OTZs8rEHAJlZUHfDjaCST9WCK5VK3n2qCZOdE3LIpjSMbbFHkf6q2dOzP_'
```
##### Respuesta
 Si la petición es exitosa (*Codigo 200*)
 ```sh
 {
      "permissions": {"permission": "-rw-r--r--",
                      "user": "tilin",
                      "group": "administrator"
                      }
      "SHA256": "hash",
      "timestamps":  {"atime": "timestamp",
                      "mtime": "timestamp"
                      }
    }
```

#### POST /api/exec/scan
Crea un escaneo de un archivo en el sistema, como dato de entrada se le debe enviar un json con la ruta del archivo a escanear, `{"file":"/opt/tilin/malware.sh"}`. Como respuesta retorna el status de la creacion del escaneo, sus posibles valores son:
- Started (Codigo 201): Se creó correctamente el escaneo, adicionalmente se retorna el id del escaneo para poder consultar su estado. 
- Scanning error (Codido 503): Se presentó un problema al crear un escaneo
-File not found (Code 404): El archivo a analizar no existe

##### Request
```sh
curl --request POST \
      --url http://localhost:5000/api/exec/scan\
      --header 'API-Key: a53MbXL4NeCW18OTZs8rEHAJlZUHfDjaCST9WCK5VK3n2qCZOdE3LIpjSMbbFHkf6q2dOzP_' \
      --header 'content-type: application/json' \
      --data '{"file":"/opt/malware.sh"}'
```
##### Respuesta
 Si la petición es exitosa (*Codigo 200*)
 ###### Successfully

 ```sh
 {"id":"NTM3NmVjNzJmYTZjMzYzNjcwYmE1NTY5ODBiZmNiYTE6MTY1Njk4NjExOA==","status":"Started"}
```
###### With error
```sh
 {"status":"Scanning error"}
```
o

```sh
 {"status":"File not found"}
```

#### GET /api/exec/scan
Una vez iniciado un escaneo de forma exitosa se puede consultar el estatus del mismo con este endpoint, y una vez terminado retorna la información del escaneo, en ella se puede ver el numero de bases de datos que reportan al archivo como malicioso, entre otra información
##### Request
```sh
curl --request GET\
     --url http://localhost:5000/api/exec/scan?id=NTM3NmVjNzJmYTZjMzYzNjcwYmE1NTY5ODBiZmNiYTE6MTY1Njk4NjExOA== \
      --header 'API-Key: a53MbXL4NeCW18OTZs8rEHAJlZUHfDjaCST9WCK5VK3n2qCZOdE3LIpjSMbbFHkf6q2dOzP_' \
```
##### Respuesta
```sh
{"confirmed-timeout":0,"failure":0,"harmless":0,"malicious":0,"suspicious":0,"timeout":0,"type-unsupported":15,"undetected":57}
```
