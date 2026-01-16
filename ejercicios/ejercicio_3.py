from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from lib.uoc_datasets import UOC_Dataset as uoc_ds


class Ejercicio_3:
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
		
    
    def plot_tasa_abandono(self) -> None:
        """Genera un gráfico con la evolución de la tasa de abandono media por curso académico."""

       # print(self.uoc_ds.get_dsTA_agrupado())
        print(self.uoc_ds.get_ds_fusionado())
        
      

        # claves = [
        #     "Curs Acadèmic",
        #     "Tipus universitat",
        #     "Sigles",
        #     "Tipus Estudi",
        #     "Branca",
        #     "Sexe",
        #     "Integrat S/N",
        # ]

        # combinado = df_rendimiento.merge(
        #     df_abandono[claves + ["Tasa de abandono"]],
        #     on=claves,
        #     how="inner",
        # )

        # evolucion = (
        #     combinado.groupby("Curs Acadèmic", as_index=False)["Tasa de abandono"].mean()
        #     .sort_values("Curs Acadèmic")
        # )

        # plt.figure(figsize=(10, 5))
        # plt.plot(evolucion["Curs Acadèmic"], evolucion["Tasa de abandono"], marker="o")
        # plt.title("Evolución de la tasa de abandono")
        # plt.xlabel("Curso académico")
        # plt.ylabel("Tasa de abandono (%)")
        # plt.xticks(rotation=45)
        # plt.grid(True, alpha=0.3)
        # plt.tight_layout()
        # plt.show()


