
"""

Read csv data from the temp dir

"""

def read_file(filename:str):
    import csv
    from definitions import TEMP_DATA_PATH    

    # opening the file using "with" statement
    with open(TEMP_DATA_PATH + filename,'r') as data:
        all_data:list[str] = []

        # add every list to a single one [[],[],[]]
        for line in csv.reader(data):
            all_data.append(line)
        
        return all_data


"""

Function to read the csv files and return the data in this format

{
    names: [name,name2,name3]
    full_data: [ [data,data,data] , [data,data,data] , [data,data,data] , [data,data,data] , [data,data,data] ,[data,data,data] ]
}

"""


def csv_to_dict_of_lists(filename:str):

    full_data = read_file(filename)
        
    to_return:dict = {}

    # pop the first item (names) to new key in the dict
    to_return.update({ "names" : full_data.pop(0) })
    
    # add the rest of the data to the full_data key
    to_return.update({ "full_data" : full_data })
    return to_return


"""

Function to read the csv files and return the data in this format

[
    {name:data,name2:data,name3:data}
    {name:data,name2:data,name3:data}
    {name:data,name2:data,name3:data}
]

"""

def csv_to_list_of_dicts(filename:str):
    from csv import DictReader
    from definitions import TEMP_DATA_PATH

    # open file in read mode
    with open(TEMP_DATA_PATH + filename, 'r') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
        return list_of_dicts
