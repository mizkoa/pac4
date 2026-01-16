
from typing import Optional
from lib.uoc_datasets import UOC_Dataset as uoc_ds
import pandas as pd

class Ejercicio_1:
    """
    Crear una función que acepte una ruta de archivo como argumento opcional. Si se proporciona la ruta, la función debe leer el fichero correspondiente. Si no se proporciona ninguna entrada, la función debe preguntar al usuario qué dataset de los dos disponibles desea cargar. Esta función se deberá reutilizar en los siguientes ejercicios.
    Exploración del dataset. Para el dataset que el usuario seleccione, se debe:
        1.1. Mostrar las 5 primeras filas.
        1.2. Mostrar las columnas del dataframe.
        1.3. Mostrar la información (info())
    """
   
    def __init__(self) -> None:
        """
        Inicializar la clase y cargar el dataset según la entrada del usuario.
        Si se proporciona una ruta de archivo, se carga ese dataset.
        Si no se proporciona ninguna ruta, se pregunta al usuario qué dataset desea cargar.
        """
        self.uoc_ds : uoc_ds = uoc_ds()
        self.ds : Optional[pd.DataFrame] = self.uoc_ds.open_desde_consola() # Cargar el dataset según la entrada del usuario.


    def apartado_1(self) -> None:
        """
            1.1. Mostrar las 5 primeras filas.
        """
        if self.ds is not None:
            print(self.ds.head())
        
    def apartado_2(self) -> None:
        """
            1.2. Mostrar las columnas del dataframe.
        """
        if self.ds is not None:
            print(self.ds.columns.to_list())    

    def apartado_3(self) -> None:
        """
            1.3. Mostrar la información (info())
        """
        if self.ds is not None:      
            print(self.ds.info())

