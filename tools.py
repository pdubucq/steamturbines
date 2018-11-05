# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 10:00:15 2018

Gist to show how to write to an excel file without deleting its contents

@author: Pascal Dubucq
    """

import pandas as pd
import numpy as np
from openpyxl import load_workbook

def update_excel(df, filename, sheet_name):
    book = load_workbook(filename)
    writer = pd.ExcelWriter(filename, engine='openpyxl') 
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    
    
    df.to_excel(writer, sheet_name)
    
    writer.save()

if __name__ == "__main__":
    #%%
    df=pd.DataFrame(np.random.normal(size=(100,1))).cumsum()

    update_excel(df, 'test.xlsx', 'python_output')