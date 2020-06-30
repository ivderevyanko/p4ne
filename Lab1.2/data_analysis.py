from matplotlib import pyplot
from openpyxl import load_workbook

wb = load_workbook('data_analysis_lab.xlsx')

sheet = wb['Data']

sheet['A'][1:]
#sheet['B'][1:]
#sheet['C'][1:]

def getvalue(x):
    return x.value

map(getvalue, sheet['A'][1:])

pyplot.plot(list_x, list_y, label="Метка")

pyplot.show()