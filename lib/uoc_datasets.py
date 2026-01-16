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
        self.ds_arg: Optional[pd.DataFrame] = None # Introducido via argumento al ejecutar el script
        self.dsTA_agrupado: Optional[pd.DataFrame] = None # Dataset de tasa de abandono agrupado
        self.dsRE_agrupado: Optional[pd.DataFrame] = None # Dataset de rendimiento de estudiantes agrupado
        self.ds_fusionado: Optional[pd.DataFrame] = None # Dataset fusionado de abandono y rendimiento

        self.flag_dsTA_renombrado : bool = False
        self.flag_dsRE_limpio : bool = False
        self.flag_dsTA_limpio : bool = False
 
    
    def get_dsTA(self) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset de tasa de abandono - Si no ha sido cargado, lo abrimos desde el archivo
            returns: pd.DataFrame o None si no se pudo cargar el archivo.
        """
        if self.dsTA is None:
            self.dsTA = self.open_xlsx("data/taxa_abandonament.xlsx")
            if not self.flag_dsTA_renombrado: 
                self.dsTA.rename(columns={
                    'Naturalesa universitat responsable': 'Tipus universitat',
                    'Universitat Responsable': 'Universitat',
                    'Sexe Alumne': 'Sexe',
                    'Tipus de centre': 'Integrat S/N'
                    }, inplace=True)  # inplace=True modifica el DataFrame original y no crea una copia
            if not self.flag_dsTA_limpio:
                self.dsTA.drop(columns=["Universitat", "Unitat"], inplace=True) # inplace=True modifica el DataFrame original y no crea una copia
                self.flag_dsTA_limpio = True
        return self.dsTA    
   

    def get_dsRE(self) -> Optional[pd.DataFrame]:
        """
            Obtener el dataset de rendimiento de estudiantes - Si no ha sido cargado, lo abrimos desde el archivo
            returns: pd.DataFrame o None si no se pudo cargar el archivo.
        """
        if self.dsRE is None:
            self.dsRE = self.open_xlsx("data/rendiment_estudiants.xlsx")
            if not self.flag_dsRE_limpio:
                self.dsRE.drop(columns=["Universitat", "Unitat", "Crèdits ordinaris superats", "Crèdits ordinaris matriculats"], inplace=True) # inplace=True modifica el DataFrame original y no crea una copia
                self.flag_dsRE_limpio = True
        return self.dsRE 
  
    def get_otroDS(self, path: str) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset cargado via argumento al ejecutar el script
            returns: pd.DataFrame o None si no se pudo cargar el archivo.
        """ 
        if self.ds_arg is None:
            self.ds_arg = self.open_xlsx(path)
        return self.ds_arg   
    
    def renombrar_dsTA(self) -> None:
        """
        Renombrar las columnas del dataset taxa_abandonament.xlsx para que coincida con el dataset rendiment_estudiants.xlsx
        """      
        if self.dsTA is None:   
            self.dsTA = self.open_xlsx("data/taxa_abandonament.xlsx")
        self.dsTA.rename(columns={
           'Naturalesa universitat responsable': 'Tipus universitat',
           'Universitat Responsable': 'Universitat',
           'Sexe Alumne': 'Sexe',
           'Tipus de centre': 'Integrat S/N'
        }, inplace=True)  # inplace=True modifica el DataFrame original y no crea una copia 
        self.flag_dsTA_renombrado = True
    
    def eliminar_columnas_dsTA(self) -> None:
        """
        Eliminar las columnas indicadas del dataset de tasa de abandono
            arguments: columnas_a_eliminar: list - Lista de columnas a eliminar
        """ 
        if self.dsTA is None:   
            self.dsTA = self.open_xlsx("data/taxa_abandonament.xlsx")
        self.dsTA.drop(columns=["Universitat", "Unitat"], inplace=True) # inplace=True modifica el DataFrame original y no crea una copia 
        self.flag_dsTA_limpio = True

    def eliminar_columnas_dsRE(self) -> None:
        """
        Eliminar las columnas indicadas del dataset de rendimiento de estudiantes
            arguments: columnas_a_eliminar: list - Lista de columnas a eliminar
        """ 
        if self.dsRE is None:
            self.dsRE = self.open_xlsx("data/rendiment_estudiants.xlsx")
        self.dsRE.drop(columns=["Universitat", "Unitat", "Crèdits ordinaris superats", "Crèdits ordinaris matriculats"], inplace=True) # inplace=True modifica el DataFrame original y no crea una copia        
        self.flag_dsRE_limpio = True

    def get_dsRE_agrupado(self) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset de rendimiento de estudiantes agrupado
            returns: pd.DataFrame o None si no se ha agrupado ningún dataset.
        """ 
        if (self.dsRE_agrupado is None):
            self.dsRE_agrupado = self.agrupar_dataset(
                self.get_dsRE(),
                ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'],
                'Taxa rendiment'
            ).rename(columns={"Taxa rendiment": "Tasa de rendimiento"}) 
        return self.dsRE_agrupado   
    
    def get_dsTA_agrupado(self) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset de tasa de abandono agrupado
            returns: pd.DataFrame o None si no se ha agrupado ningún dataset.
        """ 
        if (self.dsTA_agrupado is None):
            self.dsTA_agrupado = self.agrupar_dataset(
                self.get_dsTA(),
                ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'],
                '% Abandonament a primer curs'
            ).rename(columns={"% Abandonament a primer curs": "Tasa de abandono"})
        return self.dsTA_agrupado

    def get_ds_fusionado(self) -> Optional[pd.DataFrame]:
        """
        Obtener el dataset fusionado de abandono y rendimiento
            returns: pd.DataFrame o None si no se ha fusionado ningún dataset.
        """ 
        if (self.ds_fusionado is None):
            self.merge_datasets(
                self.get_dsRE_agrupado(),
                self.get_dsTA_agrupado(),
                ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N']
        )  
        return self.ds_fusionado
    
    # def set_dsTA(self, df: pd.DataFrame) -> None:
    #     """
    #     Establecer el dataset de tasa de abandono
    #         arguments: df: pd.DataFrame - El DataFrame a establecer como dataset de tasa de abandono
    #     """
    #     self.dsTA = df
    
    # def set_dsRE(self, df: pd.DataFrame) -> None:
    #     """
    #     Establecer el dataset de rendimiento de estudiantes
    #         arguments: df: pd.DataFrame - El DataFrame a establecer como dataset de rendimiento de estudiantes
    #     """
    #     self.dsRE = df
    

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
    


    # def agrupar_dataset(self, tipo : str ) -> None:   
    #     """
    #        Agrupar todas las filas que compartan las mismas características (excepto el nombre del estudio) para ambos datasets. 
    #     """
    #     if tipo == "RE":
    #         self.dsRE_agrupado = self.dsRE.groupby(
    #             ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'],as_index=False
    #         )['Taxa rendiment'].mean().rename(columns={"Taxa rendiment": "Tasa de rendimiento"})  # as_index=False mantiene las columnas de agrupación como columnas normales en el DataFrame resultante y así podemos renombrar la columna Taxa rendiment;
    #     elif tipo == "TA":
    #         self.dsTA_agrupado = self.dsTA.groupby(
    #             ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'],as_index=False
                
    #         )['% Abandonament a primer curs'].mean().rename(columns={"% Abandonament a primer curs": "Tasa de abandono"})  # as_index=False mantiene las columnas de agrupación como columnas normales en el DataFrame resultante y así podemos renombrar la columna Taxa rendiment;  




    def agrupar_dataset(self, df : pd.DataFrame, columnas_groupby : list, columna_media : str) -> pd.DataFrame:
        """
        Agrupar el dataset por las columnas indicadas y calcular la media de la columna indicada
            arguments:
                df: pd.DataFrame - El DataFrame a agrupar
                columnas_groupby: list - Las columnas por las que agrupar
                columna_media: str - La columna de la que calcular la media
            returns: pd.DataFrame - El DataFrame agrupado
        """
        return df.groupby(columnas_groupby,as_index=False)[columna_media].mean() # as_index=False mantiene las columnas de agrupación como columnas normales en el DataFrame resultante y así podemos renombrar la columna Taxa rendiment;
    



    def merge_datasets(self, df1: pd.DataFrame, df2: pd.DataFrame, columnas: list) -> None:
        """
           Fusionar dos datasets por las columnas indicadas
               arguments:
                   df1: pd.DataFrame - El primer DataFrame a fusionar
                   df2: pd.DataFrame - El segundo DataFrame a fusionar
                   on: list - Las columnas por las que fusionar
                   how: str - El tipo de fusión (default: 'inner')
               returns: pd.DataFrame - El DataFrame fusionado
        """
        self.ds_fusionado = pd.merge(df1, df2, on=columnas, how='inner') 