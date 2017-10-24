import json


finalAttendanceDictionary = {111 : True, 222 : True, 333 : False, 444 : True}


json_string = '{attendance:['

for key, val in finalAttendanceDictionary.items():
    json_string = json_string + '{\\"student_id\\":' + str(key) + ',\\"present\\":' + str(val) + '},'

json_string = json_string[:-1]
json_string = json_string + ']}'
print(json_string)

finalJson = json.dumps('{attendance:[' + str(finalAttendanceDictionary) + ']}')
#print(finalJson)