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
Para facilitar la tarea se puede uasar la siguiente Key:
```sh
2f6f90a1af62e060eb41dafa14a9b1b6210c2511455088ecb823adbcc9f22d2c
```
## Descripcion de la API
Para poder interactuar con mercapi es necesario contar con una API key generada por medio de
