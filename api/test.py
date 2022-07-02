from routes.file_manager import File_Manager

file=File_Manager('/root/mercado/api/test_data/borrar.txt')
print(file.get_metadata())