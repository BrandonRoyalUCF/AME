import sys
import json

jsonString = sys.argv[1]

file = open("C:/testfile.txt", "w")

file.write(jsonString)

file.close()

jsonObject = json.loads(jsonString)

jsonObject['data'] = 'modified'



sys.stdout.write(json.dumps(jsonObject));
    