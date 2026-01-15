import os
import pandas as pd

"""
    Rendimiento estudiantes
    --------------------------------------
    0   Curs Acadèmic                  14117 non-null  object 
    1   Tipus universitat              14117 non-null  object 
    2   Universitat                    14117 non-null  object 
    3   Sigles                         14117 non-null  object 
    4   Unitat                         14117 non-null  object 
    5   Tipus Estudi                   14117 non-null  object 
    6   Branca                         14117 non-null  object 
    7   Codi Estudi                    14117 non-null  object 
    8   Estudi                         14117 non-null  object 
    9   Sexe                           14117 non-null  object 
    10  Integrat S/N                   14117 non-null  object 
    11  Crèdits ordinaris superats     14117 non-null  float64
    12  Crèdits ordinaris matriculats  14117 non-null  float64
    13  Taxa rendiment                 14117 non-null  float64

    Tasa de abandono
    --------------------------------------
    0   Curs Acadèmic                       10875 non-null  object 
    1   Naturalesa universitat responsable  10875 non-null  object 
    2   Universitat Responsable             10875 non-null  object 
    3   Sigles                              10875 non-null  object 
    4   Unitat                              10875 non-null  object 
    5   Tipus Estudi                        10875 non-null  object 
    6   Branca                              10875 non-null  object 
    7   Estudi                              10875 non-null  object 
    8   Sexe Alumne                         10875 non-null  object 
    9   Tipus de centre                     10875 non-null  object 
    10  % Abandonament a primer curs        10838 non-null  float64


"""

class UOCDataset:
    def __init__(self, path: str) -> None:
        self.ds = None
        if not os.path.isfile(path):
            print("La ruta proporcionada no es un archivo válido")
            return

        if not path.endswith('.xlsx'):
            print("El archivo debe ser un archivo .xlsx válido")
            return

        try:
            self.ds : pd.DataFrame = pd.read_excel(path)
        except Exception as error:
            print(f"No se pudo leer el archivo: {error}")
            

    def get_df(self) -> pd.DataFrame:
        return self.ds
    


    def agrupar_dataset(self, df : pd.DataFrame, columnas_groupby : list, columna_media : str) -> pd.DataFrame:
        """
           Agrupar todas las filas que compartan las mismas características (excepto el nombre del estudio) para ambos datasets. 
                La función debe devolver un nuevo dataset con:
                    - Una fila por cada combinación únicas de las columnas ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N']
                    - Una columna con el rendimiento medio, en el caso del dataset de rendimiento y con la tasa media de abandono en el caso del dataset de abandono.
        """
        # ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N']
        return df.groupby(columnas_groupby,as_index=False)[columna_media].mean()
      