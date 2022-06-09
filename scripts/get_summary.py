from os import error
import wikipedia
import json
import os

parent_dir = "/Users/shreyabanga/Desktop/iSeaTree_EOL_Images/missing_images/"

f = open('species1.json')
data = json.load(f)

for i in data:

    if i['FULL_PIC'] == "":

        
        try:
            directory = i['ID'] + "/wikimedia_commons"#+ '/info.json'
            path = os.path.join(parent_dir,directory)
            os.mkdir(path)
            # g = open(path, 'w')
            # g.write("{\n[\n\"URL\": \"\",\n]\n}")
            # g.close()
                # os.mkdir(path)
            # print(wikipedia.summary(i['SCIENTIFIC'].replace(" ","_"))+'\n\n')
        except:
            # continue
            print("fail")
# g = open(parent_dir)
# dataa = json.load(g)
# print(dataa)
# g.close()
f.close()

# finding result for the search
# sentences = 2 refers to numbers of line

# printing the result
