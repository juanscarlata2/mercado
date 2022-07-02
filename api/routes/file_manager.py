from pathlib import Path
import datetime
from pstats import Stats
import pwd
import grp
import os
import stat
import hashlib



class File_Manager():
    def __init__(self, file_name):
        self.file_name=file_name
        self.path = Path(file_name)
        self.is_valid=self.file_exist()

    def file_exist(self):
        if self.path.is_file():
            return True
        else:
            return False


    def delete_file(self):
        if self.is_valid:
            try:
                self.path.unlink()
            except Exception as err:
                print(f"Error while trying to delete the file {self.file_name}: {err}")
                return False
            else:
                return True
        else:
            return False

    def get_metadata(self):
        if self.is_valid:
            stats=self.path.stat()
            
            creation_time=self.__time_converter(stats.st_ctime)
            mod_time=self.__time_converter(stats.st_mtime)
            access_time=self.__time_converter(stats.st_atime)
            time_stamps= {"ctime":creation_time, "atime": access_time, "mtime": mod_time}

            permission=self.__get_permission()
            user,group=self.__get_user_info(stats.st_uid,stats.st_gid)
            permissions={"permission": permission, "user": user,"group": group}

            sha256_hash=self.__get_sha256_hash()

            file_data={
            "permissions":permissions,
            "SHA256":sha256_hash,
            "timestamps":time_stamps
            }

            return file_data
        else:
            return False

    def __get_user_info(self,uid,gid):
        user = pwd.getpwuid(uid)[0]
        group = grp.getgrgid(gid)[0]
        return user,group

    def __get_permission(self):
        st = os.stat(self.file_name)
        return stat.filemode(st.st_mode)

    def __time_converter(self, date):
        format_time=datetime.datetime.fromtimestamp(date)
        return str(format_time)

    def __get_sha256_hash(self):
        with open(self.file_name,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest();
        return readable_hash




            

