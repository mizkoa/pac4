import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from lib.uoc_datasets import UOC_Dataset as uoc_ds
from scipy.stats import pearsonr, linregress


class Ejercicio_4:
    """
       Análisis estadístico automatizado
    """ 
    def __init__(self) -> None:
        """
            Inicializamos la clase UOCDataset para manejar el dataset
        """ 

        self.uoc_ds : uoc_ds = uoc_ds()
        self.df_fusionado: Optional[pd.DataFrame] = self.uoc_ds.get_ds_fusionado()

    def analyze_dataset(self, show_json : bool = False) -> None:
        """
        Ejercicio 4: Análisis estadístico automatizado
            Realizar un análisis estadístico completo del dataset fusionado que obtuviste en el ejercicio 2. El objetivo es calcular diferentes métricas y estadísticas que nos permitan entender mejor el comportamiento del rendimiento y el abandono universitario, y guardar todos estos resultados en un archivo JSON bien estructurado.
            Estructura del análisis JSON:
            El archivo JSON que debes generar (src/report/analisi_estadistic.json) debe contener los siguientes apartados. Observa cómo está organizado en secciones lógicas que van de lo general (metadata y estadísticas globales) a lo específico (análisis por rama).
        """
        resultado = {
            "metadata": self.get_metadata(),
            "estadisticas_globales": self.get_estadisticas_globales(),
            "analisis_por_ramas": self.analisis_por_ramas(),
            "ranking_ramas": self.rankins()
        }
        resultado = self.redondeo_de_floats(resultado, 2)
        if show_json:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
        # Guardar el resultado en un archivo JSON
        output_dir : str = "src/report"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "analisi_estatisc.json")
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(resultado, file, ensure_ascii=False, indent=2)

   
    def redondeo_de_floats(self, data : object, decimales: int):
        """
            Redondea todos los valores float en una estructura de datos anidada 
            Compruba si es un diccionario, una lista o un float y aplica el redondeo recursivamente para todos los elementos del diciconario principal
        """
        if isinstance(data, dict):
            return {key: self.redondeo_de_floats(value, decimales) for key, value in data.items()}
        if isinstance(data, list):
            return [self.redondeo_de_floats(item, decimales) for item in data]
        if isinstance(data, float):
            return round(data, decimales)
        return data
    
   
    def get_metadata(self) -> dict:
        """
            4.1. Sección Metadata:

            Esta sección debe contener información básica sobre el análisis que estás realizando. Piensa en ella como la "ficha técnica" de tu análisis:

                fecha_analisis: La fecha actual en formato ISO (YYYY-MM-DD). Usa datetime.now().strftime("%Y-%m-%d") para obtenerla automáticamente.
                num_registros: El número total de registros en tu dataset fusionado. Simplemente usa len(merged_df).
                periodo_temporal: Una lista ordenada con todos los cursos académicos únicos que aparecen en tus datos. Puedes obtenerla con sorted(merged_df['Curs Acadèmic'].unique()).
        """

        return {
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d"), # fecha del análisis:
            "num_registros": int(len(self.df_fusionado)),
            "periodo_temporal": sorted(self.df_fusionado['Curs Acadèmic'].unique())
        }
    
    def get_estadisticas_globales(self) -> dict:
        """
            4.2. Estadísticas Globales:
                Aquí calcularás las métricas que resumen el comportamiento general de todo el sistema universitario catalán, sin diferenciar por ramas:
                abandono_medio: La tasa media de abandono en primer curso, calculada como la media de la columna '% Abandonament a primer curs'.
                rendimiento_medio: La tasa media de rendimiento, calculada como la media de la columna 'Taxa rendiment'.
                correlacion_abandono_rendimiento: Este es un valor muy interesante que nos indica si existe relación entre el abandono y el rendimiento. 
                Para calcularlo, debes usar la correlación de Pearson de scipy
        """

        corr, p_value = pearsonr(
            self.df_fusionado['Tasa de abandono'].dropna(),
            self.df_fusionado['Tasa de rendimiento'].dropna()
             
        )
  
        return {
            "abandono_medio": self.df_fusionado['Tasa de abandono'].mean(),
            "rendimiento_medio": self.df_fusionado['Tasa de rendimiento'].mean(),
            "correlacion_abandono_rendimiento": {
                "correlacion_pearson": corr,
                "p_value": p_value
            }  
            
        }
    def analisis_por_ramas(self)-> dict:
        """
            4.3 Análisis por Ramas:
                Estadísticas descriptivas básicas:
                    - Media y desviación estándar del porcentaje de abandono
                    - Media y desviación estándar de la tasa de rendimiento
                    - Detección de tendencias temporales
        """ 
        resutados_ramas : dict = {}

        # Agrupar por rama
        for rama in self.df_fusionado['Branca'].unique():
            datos_rama : pd.DataFrame  = self.df_fusionado[self.df_fusionado['Branca'] == rama]
                     
            # Cálculo de las estadísticas descriptivas
            abandono_media = datos_rama['Tasa de abandono'].mean()
            abandono_desviacion = datos_rama['Tasa de abandono'].std()
            rendimiento_media = datos_rama['Tasa de rendimiento'].mean()
            rendimiento_desviacion = datos_rama['Tasa de rendimiento'].std()

            # Detección de tendencias temporales:

            branch_by_year : pd.DataFrame = datos_rama.groupby('Curs Acadèmic').agg(
                {'Tasa de abandono': 'mean'
            }).reset_index()
            years : list = branch_by_year['Curs Acadèmic'].tolist()
            valores_abandono : list = branch_by_year['Tasa de abandono'].tolist()
            slope, intercept, r_value, p_value, std_err = linregress(
                range(len(years)),  # Posiciones: 0, 1, 2, 3...
                valores_abandono
            )

            #  Interpretación de la pendiente
            if slope > 0.01:
                tendencia : str = "creciente"
            elif slope < -0.01:
                tendencia : str = "decreciente"
            else:
                tendencia : str = "estable" 

            # Guardar los resultados de la rama:
            resutados_ramas[rama] = {
                "abandono_media": abandono_media,
                "abandono_desviacion": abandono_desviacion,
                "rendimiento_media": rendimiento_media,
                "rendimiento_desviacion": rendimiento_desviacion,
                "tendencia_abandono": tendencia
            }

        return resutados_ramas

    def rankins(self) -> dict:
        """
        4.4 dentifica qué ramas tienen los mejores y peores resultados. 
            Rama con mejor rendimiento (tasa más alta)
            Rama con peor rendimiento (tasa más baja)
            Rama con mayor abandono (porcentaje más alto)
            Rama con menor abandono (porcentaje más bajo) 
        """ 

        return {
            "rama_mejor_rendimiento": {
                "rama": self.df_fusionado.loc[self.df_fusionado['Tasa de rendimiento'].idxmax(), 'Branca'],
                "universidad": self.df_fusionado.loc[self.df_fusionado['Tasa de rendimiento'].idxmax(), 'Tipus universitat']
            },
            "rama_peor_rendimiento": {
                "rama": self.df_fusionado.loc[self.df_fusionado['Tasa de rendimiento'].idxmin(), 'Branca'],
                "universidad": self.df_fusionado.loc[self.df_fusionado['Tasa de rendimiento'].idxmin(), 'Tipus universitat']
            },
            "rama_mayor_abandono": {
                "rama": self.df_fusionado.loc[self.df_fusionado['Tasa de abandono'].idxmax(), 'Branca'],
                "universidad": self.df_fusionado.loc[self.df_fusionado['Tasa de abandono'].idxmax(), 'Tipus universitat']
            },
            "rama_menor_abandono": {
                "rama": self.df_fusionado.loc[self.df_fusionado['Tasa de abandono'].idxmin(), 'Branca'],
                "universidad": self.df_fusionado.loc[self.df_fusionado['Tasa de abandono'].idxmin(), 'Tipus universitat']
            }
            # NOTA: Añado el Tipus de universitat porque para el máximo y mínimo me daba el mismo valor de rama, y al analizar el dataset veo que hay  universidades públicas y privadas con la misma rama y distinto rendimiento/abandono
        }
       