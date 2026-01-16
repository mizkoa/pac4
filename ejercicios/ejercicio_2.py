from typing import Optional
import pandas as pd
from lib.uoc_datasets import UOC_Dataset as uoc_ds

class Ejercicio_2:
    """
    Se pretende hacer un análisis de los dos datasets que se proporcionan. Para ello, lo primero que queremos hacer es limpiar y unir los datasets. Como habrás podido comprobar en el EDA, los datasets tienen estructuras similares pero no completamente iguales. 
    Los objetivos de este ejercicio son:
        Homogeneizar ambos datasets: implica que las columnas tengan el mismo nombre y que los datos que se muestren tengan el mismo origen
        Actualmente cada línea de datos muestra la información de un estudio en concreto por curso académico y sexo (para diferenciar los resultados entre hombres y mujeres). Para simplificar el análisis posterior, queremos agrupar los estudios por rama (Branca), de tal forma que tengamos una línea por curso académico y rama de estudio, donde la tasa de rendimiento y el % de abandono sea la media de los estudios que contienen esa rama.
        Finalmente queremos crear un dataset fusionado a partir de ambos datasets
    """ 
    def __init__(self) -> None:
        """
            pass
        """ 

        self.uoc_ds : uoc_ds = uoc_ds()

            
 
    def apartado_1(self) -> None:
        """
            2.1. Renombrar las columnas del dataset taxa_abandonament.xlsx para que coincida con el dataset rendiment_estudiants.xlsx
                
                Analizando los nombres de las columnas de ambos datasets, se pueden observar las siguientes diferencias entre Taaxa_abandonament y Rendiment_estudiants:
                    - "Naturalesa universitat responsable" --> "Tipus universitat"
                    - "Universitat Responsable" --> "Universitat"
                    - "Sexe Alumne" --> "Sexe"
                    - "Tipus de centre" --> "Integrat S/N" 
        """      
       
        self.uoc_ds.renombrar_dsTA()
        print(self.uoc_ds.get_dsTA().info())


    def apartado_2(self) -> None:
        """ 
            2.2. Eliminar las columnas:
                - "Universitat", "Unitat" en ambos dataframes
                - "Crèdits ordinaris superats" y "Crèdits ordinaris matriculats" en el caso del dataset de rendimiento.
        """ 
       
        
        self.uoc_ds.eliminar_columnas_dsRE()
        self.uoc_ds.eliminar_columnas_dsTA()

        print(self.uoc_ds.get_dsRE().info())
        print(self.uoc_ds.get_dsTA().info())

   
    def apartado_3(self) -> None:
        """
            2.3. Crear y aplicar a los datasets una función que agrupe todas las filas que compartan las mismas características (excepto el nombre del estudio) para ambos datasets. 
                La función debe devolver un nuevo dataset con:
                    - Una fila por cada combinación únicas de las columnas ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N']
                    - Una columna con el rendimiento medio, en el caso del dataset de rendimiento y con la tasa media de abandono en el caso del dataset de abandono.
        """ 
        self.uoc_ds.agrupar_dataset(
            self.uoc_ds.get_dsRE(),
            ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'],
            'Taxa rendiment'
        ).rename(columns={"Taxa rendiment": "Tasa de rendimiento"}) 

        self.uoc_ds.agrupar_dataset(
            self.uoc_ds.get_dsTA(),
            ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'],
            '% Abandonament a primer curs'
        ).rename(columns={"% Abandonament a primer curs": "Tasa de abandono"})
        
        print(self.uoc_ds.get_dsRE_agrupado())
        print(self.uoc_ds.get_dsTA_agrupado())
    
    def apartado_4(self) -> None:
        """
            2.4. Crear una función para fusionar ambos datasets. El dataset resultante solo debe contener las filas coincidentes entre ambos datasets. A partir de ahora utilizaréis este datasets en los ejercicios futuros.
            Nota: Para agrupar los datasets podéis utilizar el método groupby de pandas, y para fusionar ambos datasets, el método merge con la propiedad inner.
        """ 
        self.uoc_ds.merge_datasets(
            self.uoc_ds.get_dsRE_agrupado(),
            self.uoc_ds.get_dsTA_agrupado(),
            ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N']
        )   
        print(self.uoc_ds.get_ds_fusionado())

