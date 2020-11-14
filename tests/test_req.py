import requests

BASE = "http://127.0.0.1:5000/"

query_response_1 = requests.get(BASE + "query/9-21-1998")
query_response_2 = requests.get(BASE + "query/10-13-2020")
query_response_3 = requests.get(BASE + "query/1-1-1970")



file1 = {'FILE_NAME': ('file1.txt', open('/mnt/d/UTA FALL_2020/Senior Design/Backend/identiDoc/uploads/file1.txt', 'rb')),
}

file2 = {
    'FILE_NAME': ('file2.txt', open('/mnt/d/UTA FALL_2020/Senior Design/Backend/identiDoc/uploads/file2.txt', 'rb')),
}


file3 = {
    'FILE_NAME': ('file3.txt', open('/mnt/d/UTA FALL_2020/Senior Design/Backend/identiDoc/uploads/file3.txt', 'rb')),
}


upload_response_1 = requests.post(BASE + "upload", files=file1)
upload_response_2 = requests.post(BASE + "upload", files=file2)
upload_response_3 = requests.post(BASE + "upload", files=file3)






print(query_response_1.json())
print(query_response_2.json())
print(query_response_3.json())

print(upload_response_1.json())
print(upload_response_2.json())
print(upload_response_3.json())
