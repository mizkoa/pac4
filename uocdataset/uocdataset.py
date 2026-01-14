import os
import pandas as pd

class UOCDataset:
    def __init__(self, path: str) -> None:
        print (f"Cargando dataset desde la ruta: {path}")
        if not os.path.isfile(path): 
            raise ValueError("La ruta proporcionada no es un archivo válido")
        elif not path.endswith('.xlsx'): raise ValueError("El archivo debe ser un archivo .xlsx válido")
        else:
            self.ds = pd.read_excel(path)
            print(self.ds.head(2))
        print("end")    
        

    
    def info(self):
        print(self.ds.head(2))