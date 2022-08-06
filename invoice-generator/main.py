import os
import docx

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


if __name__ == "__main__" :
    # Get current working dir path
    cwd = os.getcwd()
    data = cwd + "\\static\\data\\details.xlsx"

    wb = load_workbook(data)
    ws = wb.active

    data_range = ws[]

    print(wb.active)
