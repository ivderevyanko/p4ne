from matplotlib import pyplot
from openpyxl import load_workbook

wb = load_workbook('data_analysis_lab.xlsx')

sheet = wb['Data']

sheet['A'][1:]
sheet['B'][1:]
sheet['C'][1:]

def getvalue(x):
    return x.value

year = list(map(getvalue, sheet['A'][1:]))
temper = list(map(getvalue, sheet['B'][1:]))
act = list(map(getvalue, sheet['C'][1:]))

pyplot.plot(year, temper, label="Метка")
pyplot.plot(year, act, label="Метка")

pyplot.show()