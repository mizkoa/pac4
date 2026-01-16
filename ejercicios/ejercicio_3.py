import os
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd
from lib.uoc_datasets import UOC_Dataset as uoc_ds


class Ejercicio_3:
    """
       Generación de Gráficos de Series Temporales
    """ 
    def __init__(self) -> None:
        """
            Inicializamos la clase UOCDataset para manejar el dataset
        """ 

        self.uoc_ds : uoc_ds = uoc_ds()
        self.figura : Optional[plt.Figure] = None
		
   
    def apartado_1(self, show_graph : bool = False) -> None:
        """
           3.1. Generación de Gráficos de Series Temporales

                Crear una función que genere visualizaciones de series temporales con las siguientes características:

                Crear dos gráficos (subplots) en una misma figura:

                Gráfico 1: Evolución del % de Abandonamiento por curso académico
                Gráfico 2: Evolución de la Tasa de Rendimiento por curso académico
                Cada gráfico debe mostrar:

                Una línea diferente para cada rama de estudio (Branca)
                Leyenda identificando cada rama
                Grid para facilitar la lectura
                Etiquetas de ejes apropiadas
                Título descriptivo
        """
  
        if self.uoc_ds.get_ds_fusionado() is None:
            print("Ha habído algún problema al fusionar los datasets")
            return

        # Agrupar por 'Curs Acadèmic' y 'Branca', calculando la Tasa de Abandono media (para % lo multiplkicamos por 100)
        tasa_abandono_media = self.uoc_ds.get_ds_fusionado().sort_values("Curs Acadèmic").groupby(['Curs Acadèmic', 'Branca'])['Tasa de abandono'].mean() * 100
        tasa_abandono_media = tasa_abandono_media.unstack() # Convertir 'Branca' en columnas
        
        tasea_rendimiento_media = self.uoc_ds.get_ds_fusionado().sort_values("Curs Acadèmic").groupby(['Curs Acadèmic', 'Branca'])['Tasa de rendimiento'].mean() * 100
        tasea_rendimiento_media = tasea_rendimiento_media.unstack()

        # Creamos figura y los subplots y los colores de paleta
        fig, sp = plt.subplots(2, 1, figsize=(14, 10))
        colores_paleta : tuple = plt.cm.tab10.colors


        # Grafico 1: Evolución del % de Abandonamiento por curso académico
        for i, branca in enumerate(tasa_abandono_media.columns):
            sp[0].plot(tasa_abandono_media.index, tasa_abandono_media[branca], label=branca, color=colores_paleta[i % len(colores_paleta)]) 
        sp[0].set_title('Evolución de la Tasa de Abandono por Branca y Año Académico')
        sp[0].set_xlabel('Curso Académico')
        sp[0].set_ylabel('Tasa de Abandono (%)')
        sp[0].grid(True)  # Añadir grid
        sp[0].legend(title='Branca')
        sp[0].tick_params(axis='x', rotation=45)  # Rotar etiquetas del eje X 
        
        # Grafico 2: Evolución de la Tasa de Rendimiento por curso académico
        for i, branca in enumerate(tasea_rendimiento_media.columns):
            sp[1].plot(tasea_rendimiento_media.index, tasea_rendimiento_media[branca], label=branca, color=colores_paleta[i % len(colores_paleta)]) 
        sp[1].set_title('Evolución de la Tasa de Rendimiento por Branca y Año Académico')
        sp[1].set_xlabel('Curso Académico')
        sp[1].set_ylabel('Tasa de Rendimiento (%)')
        sp[1].grid(True)  # Añadir grid
        sp[1].legend(title='Branca')
        sp[1].tick_params(axis='x', rotation=45)  # Rotar

        fig.suptitle('Análisis Académico', fontsize=16)
        plt.tight_layout()  # Ajustar el diseño para evitar solapamientos
        
        if show_graph:
            plt.show()
        
        self.figura = fig
    
    def apartado_2(self) -> None:
        """
            3.2. Guardar las Visualizaciones
                Guardar la figura generada en el directorio src/img/
                Nombre del archivo: evolucion_nombre_alumno.png
                Resolución recomendada: 300 dpi
                Crear el directorio si no existe
        """
        output_dir : str = "src/img"
        os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe
        file_path = os.path.join(output_dir, "evolucion_mario_rodriguez_izcoa.png")
        self.figura.savefig(file_path, dpi=300)  # Guardar la figura con 300 dpi


            
            
       
       
       
       
       

       
       



