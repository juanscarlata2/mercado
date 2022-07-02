import hashlib
 
filename = "/root/mercado/api/test_data/borrar.txt"
with open(filename,"rb") as f:
    bytes = f.read() # read entire file as bytes
    readable_hash = hashlib.sha256(bytes).hexdigest();
    print(readable_hash)