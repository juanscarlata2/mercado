from crypt import methods
from importlib.resources import path
from readline import append_history_file
from unittest import result
from flask import Flask, render_template, request, current_app
from . import routes
from .file_manager import File_Manager
from .virustotal import VirusTotal

def api_auth(request):
    valid_keys=current_app.config['keys']
    req_key=request.headers.get('API-Key')
    if req_key in valid_keys:
        return True
    else:
        return False


@routes.route('/api/')
def docu():
    if api_auth(request):
        return "Dcocumentacion"
    else:
         return {"error":"Unauthorized"},401


@routes.route('/api/exec/delete', methods=["POST"])
def delete():
    if api_auth(request):
        content=request.json
        if "files" in content:
            files=content["files"]
            if isinstance(files, list):
                results={}
                for file in files:
                    file_obj=File_Manager(file)
                    if file_obj.delete_file():
                        results[file]="Deleted"
                    else:
                        results[file]="File does not exist"
                return results

            else:
                 return {"error":"Bad request, files must be a list"}

        else:
            return {"error":"Bad request, no files"}
    else:
         return {"error":"Unauthorized"},401
    return {"error":"Bad request"}

@routes.route('/api/file', methods=["GET"])
def file():
    if api_auth(request):
        if "path" in request.args:
            file_name=request.args.get('path')
            file=File_Manager(file_name)
            data=file.get_metadata()
            if data:
                return data,200
            else:
                return {"error":"File not found"},404
        else:
            return {"error":"path parameter is not set"},400
    else:
         return {"error":"Unauthorized"},401

@routes.route('/api/exec/scan', methods=["GET", "POST"])
def virus():
    if api_auth(request):
        virus_key=current_app.config['virus_key']
        if virus_key:
            if request.method == 'POST':
                content=request.json
                if "file" in content:
                    file=str(content["file"])
                    virus=VirusTotal(current_app.config['virus_key']) # Get current Virus Total key
                    id=virus.star_scan_file(file)
                    if id:
                        return {"status":"Started", "id":id},201
                    elif id=="error":
                        return {"status":"Scanning error"},503
                    else:
                        return {"status":"File not found"},404
                else:
                    return {"error":"Bad request, no file attribute found"}
            else:
                if "id" in request.args:
                    virus=VirusTotal(current_app.config['virus_key'])
                    id=request.args.get('id')
                    status=virus.scan_stus(id)
                    return status,200
                else:
                    return {"error":"id parameter is not set"},400
        else:
            return {"error":"Virustotal API key has not been configured, please contact the administrator. "},503

    else:
         return {"error":"Unauthorized"},401