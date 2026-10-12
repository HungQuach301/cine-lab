import sys; sys.path.insert(0, sys.argv[1]); import xlrd
b=xlrd.open_workbook(sys.argv[2])
for sh in b.sheets():
    print("== SHEET", sh.name, sh.nrows, sh.ncols)
    lim=int(sys.argv[3]) if len(sys.argv)>3 else 15
    for r in range(min(sh.nrows,lim)):
        print(r, [sh.cell_value(r,c) for c in range(sh.ncols)])
