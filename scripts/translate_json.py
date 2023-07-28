import json

output_list = list()
path = "path/to/src"
filenames = [
    # add all json there
]

try: 
    for filename in filenames:
        with open(path + filename) as fin:
            text = json.load(fin)
            for num , element in enumerate(text):
            
                if num % 2 == 0:
                    conversition = dict()
                    conversition["instruction"] = element["say"]
                elif num % 2 == 1:
                    conversition["input"] = ""
                    conversition["output"] = element["say"]
                    
                    if num == 1:
                        conversition["history"] = ""
                    else :
                        history = list()
                        history.append(output_list[-1]["instruction"])
                        history.append(output_list[-1]["output"])
                        conversition["history"] = [history]

                    output_list.append(conversition)
                
except: 
    print("Error with open", filename)

with open("path/to/outfile/chathistory.json", "w", encoding='utf-8') as fout:
   json.dump(output_list , fout, ensure_ascii=False)

