import pandas as pd


def Lançarcomprasnoestoque(CompTotal, NCompra):
    CompTotal = pd.concat([CompTotal, NCompra], ignore_index=True)
    return CompTotal
    