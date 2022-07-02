import vt
import time
from .file_manager import File_Manager

class VirusTotal():
    def __init__(self, api_key):
        self.api_key=api_key
        self.client=vt.Client(api_key)

    def star_scan_file(self, file):
        file_obj=File_Manager(file)
        if file_obj.is_valid:
            try:
                with open(file, "rb") as f:
                    analysis = self.client.scan_file(f)
            except Exception as err:
                return "error" 
            else:
                return analysis.id
        
        return False
        

    def scan_stus(self,id):
        try:
            analysis = self.client.get_object("/analyses/{}", id)
        except Exception as err:
            print(str(err))
        else:
            status=analysis.status
            if status=="completed":
                report=analysis.stats
                return report

            return {"status":status}
        
        return False

"""
test=VirusTotal(api_key=api_key)
id=test.star_scan_file("/root/mercado/api/test_data/linpeas.sh")
print(f"the scan has the id {id}")
while 1:
    status=test.scan_stus(id=id)
    print(status)
    time.sleep(30)




client = vt.Client(api_key)
with open("/root/mercado/api/test_data/linpeas.sh", "rb") as f:
    analysis = client.scan_file(f)

while True:
    analysis = client.get_object("/analyses/{}", analysis.id)
    print(analysis.status)
    if analysis.status == "completed":
        break
    time.sleep(30)
print(analysis.stats)
"""