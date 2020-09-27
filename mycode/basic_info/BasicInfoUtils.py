'''
   @author: HeQingsong
   @date: 2020-09-20 13:37
   @filename: BasicInfoUtils.py
   @project: huobi_Python
   @python version: 3.7 by Anaconda
   @description: 
'''
from huobi.client.generic import GenericClient

generic_client = GenericClient()


def get_all_symbol():
    ret_list = []
    list_obj = generic_client.get_exchange_symbols()
    if len(list_obj):
        for row in enumerate(list_obj):
            ret_list.append(row[1].symbol)
    return ret_list


if __name__ == '__main__':
    print(get_all_symbol())
