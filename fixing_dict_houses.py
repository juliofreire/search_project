from io_files import *

filename="houses_dict"

dict = load_dict_in_file(filename=filename)


def fix_as_json(dict):
    for key in dict:
        dict_element = {"quartos": "NULL", \
                    "m2_quadrado" : "NULL", \
                    "garagem": "NULL", \
                    "banheiros": "NULL", \
                    "direto com o proprietario": 0 \
                    }
        dict_in = dict[key]["house_info"]
        # print(dict_in)
        for element in dict_in:
            if "quarto" in element:
                dict_element["quartos"] = element.split(" ")[0]
            if "quadrado" in element:
                dict_element["m2_quadrado"] = element.split(" ")[0]
            if "garage" in element:
                dict_element["garagem"] = element.split(" ")[0]
            if "banheiro" in element:
                dict_element["banheiros"] = element.split(" ")[0]
            if "propri" in element:
                dict_element["direto com o proprietario"] = 1
        # dict_element["direto com o proprietario"] = \
        # 1 if any("propri" in element for element in dict_in) else 0

        dict[key]["house_info"] = dict_element

    return dict

def fix_as_csv(dict):
    dict = fix_as_json(dict)
    string = "quartos,m2_quadrado,garagem,banheiros,direto com o proprietario,preço,cidade,bairro\n"

    for key in dict:
        # string = ""
        dict_in = dict[key]
        for key_in in dict_in:
            dict_in_in = dict_in[key_in]
            if key_in == "house_info":
                for key_in_in in dict_in_in:
                    string += str(dict_in_in[key_in_in]) + ","
            if key_in == "house_price":
                string += str(dict_in[key_in]) + ","
            if key_in == "house_location":
                string += str(dict_in[key_in]) + "\n"
    return string


dict = fix_as_csv(dict)
save_csv_in_file(dict, "houses_dict.csv")
print(dict)
