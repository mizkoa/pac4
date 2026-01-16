import os
import argparse
import pandas as pd
from typing import Optional


class UOC_Dataset:
    """ 
    Clase para manejar los datasets de la UOC: Rendimiento de estudiantes y Tasa de abandono:
    
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

    def __init__(self) -> None:
        """
            Constructor de la clase UOC_Dataset
                Inicializa los atributos de la clase
        """
        self.dsTA: Optional[pd.DataFrame] = None # Dataset de tasa de abandono
        self.dsRE: Optional[pd.DataFrame] = None # Dataset de rendimiento de estudiantes
        self.otroDS: Optional[pd.DataFrame] = None # Introducido via argumento al ejecutar el script
        self.merged_ds: Optional[pd.DataFrame] = None # Dataset fusionado de abandono y rendimiento
 
    
    def get_dsTA(self) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset de tasa de abandono - Si no ha sido cargado, lo abrimos desde el archivo
            returns: pd.DataFrame o None si no se pudo cargar el archivo.
        """
        if self.dsTA == None:
            self.dsTA = self.open_xlsx("data/taxa_abandonament.xlsx")
        return self.dsTA    
   

    def get_dsRE(self) -> Optional[pd.DataFrame]:
        """
            Obtener el dataset de rendimiento de estudiantes - Si no ha sido cargado, lo abrimos desde el archivo
            returns: pd.DataFrame o None si no se pudo cargar el archivo.
        """
        if self.dsRE == None:
            self.dsRE = self.open_xlsx("data/rendiment_estudiants.xlsx")
        return self.dsRE 
  
    def get_otroDS(self, path: str) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset cargado via argumento al ejecutar el script
            returns: pd.DataFrame o None si no se pudo cargar el archivo.
        """ 
        if self.otroDS == None:
            self.otroDS = self.open_xlsx(path)
        return self.otroDS   
    
    def open_xlsx(self, path: str) -> Optional[pd.DataFrame]:
        """
        Abrir un archivo .xlsx y cargar su contenido en un DataFrame de pandas
            arguments:  path: str - La ruta del archivo .xlsx a abrir
            returns: pd.DataFrame o None si no se pudo cargar el archivo. Optional[pd.DataFrame] significa que puede devolver o bien un DataFrame o None
        """
        
        if not os.path.isfile(path):
            print("La ruta proporcionada no es un archivo válido")
            return None

        if not path.endswith('.xlsx'):
            print("El archivo debe ser un archivo .xlsx válido")
            return None
        try:
            return pd.read_excel(path)
        except Exception as error:
            print(f"No se pudo leer el archivo: {error}")
            return None

    def open_desde_consola(self) -> Optional[pd.DataFrame]:
        """
        Abrir un archivo .xlsx desde la consola o elegir uno de los datasets disponibles
            arguments:  path: str - La ruta del archivo .xlsx a abrir (opcional)
            returns: pd.DataFrame o None si no se pudo cargar el archivo. 
        """
        opciones_datasets : list = ["Rendimiento estudiantes", "Tasa de abandono"]
        parser = argparse.ArgumentParser(
            description="Introducir una ruta del archivo a procesar o elegir uno de los disponibles"
        )
                    
        parser.add_argument("dataSet", nargs="?", help="Elegir uno de los data sets disponibles") # nargs="?" permite que el argumento posicional aparezca cero o una vez. Sin él, argparse exigiría exactamente un valor; con él, el argumento se vuelve opcional.
        args = parser.parse_args()

        # Se ha introducido una ruta como argumento
        if args.dataSet: 
            return self.get_otroDS(args.dataSet)
        
        # No se ha introducido una ruta como argumento   
        while True:
            for n, opcion in enumerate(opciones_datasets, start=1):
                print(f"{n}. {opcion}")
            opcion_elegida = input("Seleccione uno de los data sets disponibles (introduzca 1 o 2): ")
            if opcion_elegida not in ["1","2"]:
                print("Opción inválida. Por favor, introduzca 1 o 2.")
                continue
            if opcion_elegida == "1": # rendimiento estudiantes
                return self.get_dsRE()
            elif opcion_elegida == "2": # tasa de abandono
                return self.get_dsTA()
            break
    


    
    def agrupar_dataset(self, df : pd.DataFrame, columnas_groupby : list, columna_media : str) -> pd.DataFrame:
        """
        Agrupar el dataset por las columnas indicadas y calcular la media de la columna indicada
            arguments:
                df: pd.DataFrame - El DataFrame a agrupar
                columnas_groupby: list - Las columnas por las que agrupar
                columna_media: str - La columna de la que calcular la media
            returns: pd.DataFrame - El DataFrame agrupado
        """
        return df.groupby(columnas_groupby,as_index=False)[columna_media].mean()
    



    def merge_datasets(self, df1: pd.DataFrame, df2: pd.DataFrame, on: list, how: str = 'inner') -> pd.DataFrame:
        """
           Fusionar dos datasets por las columnas indicadas
               arguments:
                   df1: pd.DataFrame - El primer DataFrame a fusionar
                   df2: pd.DataFrame - El segundo DataFrame a fusionar
                   on: list - Las columnas por las que fusionar
                   how: str - El tipo de fusión (default: 'inner')
               returns: pd.DataFrame - El DataFrame fusionado
       """
        return pd.merge(df1, df2, on=on, how=how) 