import pandas as pd 



def Lançarvendasnoestoque(VendasT, NVenda): 
    VendasT = pd.concat([VendasT,NVenda], ignore_index=True)
    return VendasT