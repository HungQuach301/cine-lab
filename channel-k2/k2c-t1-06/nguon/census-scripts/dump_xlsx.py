import sys; sys.path.insert(0, sys.argv[1]); import openpyxl
b=openpyxl.load_workbook(sys.argv[2], data_only=True, read_only=True)
for ws in b.worksheets:
    rows=list(ws.iter_rows(values_only=True))
    print("== SHEET", ws.title, len(rows))
    head=int(sys.argv[3]); tail=int(sys.argv[4])
    for i,r in enumerate(rows):
        if i<head or i>=len(rows)-tail: print(i+1, r)
