import pandas as pd
from lib.uoc_datasets import UOC_Dataset as uoc_ds

class Ejercicio_2:
    """
 
        2.4. Crear una función para fusionar ambos datasets. El dataset resultante solo debe contener las filas coincidentes entre ambos datasets. A partir de ahora utilizaréis este datasets en los ejercicios futuros.
        Nota: Para agrupar los datasets podéis utilizar el método groupby de pandas, y para fusionar ambos datasets, el método merge con la propiedad inner.
    """ 
    def __init__(self) -> None:
        """
            pass
        """ 
        # rendimiento estudiantes
        self.dsRE = uoc_ds().open_xlsx("data/rendiment_estudiants.xlsx")
        # tasa de abandono
        self.dsTA = uoc_ds().open_xlsx("data/taxa_abandonament.xlsx")   
        # dataset agrupado
        self.dsRE_agrupado = None
        self.dsTA_agrupado = None   


        # dataset fusionado
        self.dsFusionado = None
            
    





    def apartado_1(self) -> None:
        """
            2.1. Renombrar las columnas del dataset taxa_abandonament.xlsx para que coincida con el dataset rendiment_estudiants.xlsx
                Analizando los nombres de las columnas de ambos datasets, se pueden observar las siguientes diferencias entre Taaxa_abandonament y Rendiment_estudiants:
                    - "Naturalesa universitat responsable" --> "Tipus universitat"
                    - "Universitat Responsable" --> "Universitat"
                    - "Sexe Alumne" --> "Sexe"
                    - "Tipus de centre" --> "Integrat S/N" 
        """      
        self.dsTA.rename(columns={
           'Naturalesa universitat responsable': 'Tipus universitat',
           'Universitat Responsable': 'Universitat',
           'Sexe Alumne': 'Sexe',
           'Tipus de centre': 'Integrat S/N'
        }, inplace=True)  # inplace=True modifica el DataFrame original y no crea una copia^ 

        print(self.dsRE.info())
        print(self.dsTA.info())



    def apartado_2(self) -> None:
        """ 
            2.2. Eliminar las columnas:
                - "Universitat", "Unitat" en ambos dataframes
                - "Crèdits ordinaris superats" y "Crèdits ordinaris matriculats" en el caso del dataset de rendimiento.
        """ 
        columnas_a_eliminar_RE = ["Universitat", "Unitat", "Crèdits ordinaris superats", "Crèdits ordinaris matriculats"]
        columnas_a_eliminar_TA = ["Universitat", "Unitat"]
        
        self.dsRE.drop(columns=columnas_a_eliminar_RE, inplace=True)
        self.dsTA.drop(columns=columnas_a_eliminar_TA, inplace=True)

        print(self.dsRE.info())
        print(self.dsTA.info())


    def apartado_3(self) -> None:
        """
            2.3. Crear y aplicar a los datasets una función que agrupe todas las filas que compartan las mismas características (excepto el nombre del estudio) para ambos datasets. 
                La función debe devolver un nuevo dataset con:
                    - Una fila por cada combinación únicas de las columnas ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N']
                    - Una columna con el rendimiento medio, en el caso del dataset de rendimiento y con la tasa media de abandono en el caso del dataset de abandono.
        """ 
      
       # mean lo convierte en una serie, por lo que hay que resetear el index (convirtiéndolo de nuevo en un Dataset) y renombrar la columna resultante para que apareza el nombre correcto 
        self.dsRE_agrupado = self.dsRE.groupby(['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'])['Taxa rendiment'].mean().reset_index(name="Tasa de rendimiento")
        self.dsTA_agrupado = self.dsTA.groupby(['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'])['% Abandonament a primer curs'].mean().reset_index(name='Tasa Media de Abandono')

        print(self.dsRE_agrupado)  
        print(self.dsTA_agrupado)
    
    def apartado_4(self) -> None:
        """
            2.4. Crear una función para fusionar ambos datasets. El dataset resultante solo debe contener las filas coincidentes entre ambos datasets. A partir de ahora utilizaréis este datasets en los ejercicios futuros.
            Nota: Para agrupar los datasets podéis utilizar el método groupby de pandas, y para fusionar ambos datasets, el método merge con la propiedad inner.
        """ 
        self.dsFusionado = pd.merge(self.dsRE_agrupado, self.dsTA_agrupado, on=['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'], how='inner')
        print(self.dsFusionado)

