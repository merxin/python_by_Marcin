import pandas as pd
from os import listdir
import numpy as np
import os
from openpyxl import load_workbook

def concatenate_files():
        a="\\f\\"
        b=a.replace('\\', '\\\\')
        print(a)
        print(b)
        folder = input("enter folder name containing the files to concatenate  ").replace('\\', '\\\\')
        print(folder)
        loc_data = input("where would you like to save the updated file?").replace('\\', '\\\\')

        try:

                files = [f for f in listdir(folder)]
                all_data = pd.DataFrame()
                for file in files:
                        current_data = pd.read_excel(folder+"\\"+file)
                        all_data = pd.concat([all_data, current_data])
        except OSError:
                print("Please provide correct location")
        os.chdir(loc_data)
        all_data.to_excel("consolidated_file.xlsx")
        print(all_data.head(10))


def move_columns_to_rows():
        input_data = input("which file would you like to transform? moving column "
                           "headers to rows... Please provide the path to the file ").replace('\\', '\\\\')
        loc_data = input("where would you like to save the updated file?").replace('\\', '\\\\')
        in_data = pd.read_excel(input_data)
        #print(in_data.head())
        try:
                # check of column titles
                all_data = pd.DataFrame(in_data)
                columns=[]
                for col in all_data.columns:
                        columns.append(col)
                print(columns)


                print(all_data.head())
                ab= all_data.melt(value_name="Values", id_vars=columns[0],var_name="Customer")
                ab.sort_values(by="Values", ascending=False, inplace = True)
                columns=[]
                for pol in ab.columns:
                        columns.append(pol)
                print(columns)
                os.chdir(loc_data)
                #name of the new file
                ab.to_excel("newfile.xlsx")

                path = loc_data +"\\"+"newfile.xlsx"

                book = load_workbook(path)
                writer = pd.ExcelWriter(path, engine='openpyxl')
                writer.book = book
                table = ab.groupby(by=[columns[0], columns[1]], dropna=False).sum()
                table.to_excel(writer, sheet_name='pivot')
                writer.save()
                writer.close()
        except OSError:
                 print("Please provide correct location")

func = input("select: \n1 to concatenate data\n2 to transform data - unpivot\n\n")
if func =="1":
        concatenate_files()
elif func =="2":
        move_columns_to_rows()
