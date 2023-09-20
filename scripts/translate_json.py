import json

output_list = list()
src_path = "/home/vcp/Mudu/Web_Application_Project/scripts/"
out_path = "/home/vcp/Mudu/Web_Application_Project/scripts/"


src_filenames = [
    # add all json there
    "conversation_chatgpt12.json",
]

## to test if the next level is dict
def isdict_next_level(test_list):
    for level_element in test_list:
        if type(level_element) is list:
            return False
        elif type(level_element) is dict:
            return True
        else:
            return TypeError


## to combine the json form like: list[ list[ dict{} ] ]
def combine(uncombine_list):
    if isdict_next_level(uncombine_list) is True:
        return uncombine_list
                
    elif isdict_next_level(uncombine_list) is False:
        combine_list = list()
        for test_list in uncombine_list:
            combine_list.append(test_list)
        return combine_list

## form json
def form_json(load_json, output_list):
    res=0
    for num , element in enumerate(load_json):
                if num % 2 == 0:
                    conversition = dict()
                    conversition["instruction"] = element["content"]
                elif num % 2 == 1:
                    conversition["input"] = ""
                    conversition["output"] = element["content"]
                    if element["content"] == "我是一名小学作文的辅导老师":
                        conversition.clear()
                        continue
                    elif conversition["instruction"] == "我只是一名小学生，需要回答老师的问题并且多问一些关于这个作文题目的问题.在这里不要出现老师的回答。student_question的格式应该为:'...'\n。":
                        conversition.clear()
                        continue
                    elif num == 1 or res ==0:
                        conversition["history"] = ""
                        res = 1
                    else :
                        history = list()
                        history.append(output_list[-1]["instruction"])
                        history.append(output_list[-1]["output"])
                        conversition["history"] = [history]

                    output_list.append(conversition)
    return output_list


## main
if __name__ == "__main__":
    
    for filename in src_filenames:
        with open(src_path + filename) as fin:
            text = json.load(fin)
            form_json(text, output_list)
            
    with open(out_path + "conversation_chatgpt12_form.json", "w", encoding='utf-8') as fout:
        json.dump(output_list , fout, ensure_ascii=False)

