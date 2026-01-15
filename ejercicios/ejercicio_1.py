
import argparse
import os
from helpers.uocdataset import UOCDataset as uoc_ds

class Ejercicio_1:
   
    def __init__(self) -> None:

        opciones_datasets = ["Rendimiento estudiantes", "Tasa de abandono"]
        parser = argparse.ArgumentParser(
            description="Introducir una ruta del archivo a procesar o elegir uno de los disponibles"
        )
	
        # nargs="?": allows that positional argument to appear zero or one time. Without it, argparse would demand exactly one value; with it, the argument becomes optional.
        parser.add_argument("dataSet", nargs="?", help="Elegir uno de los data sets disponibles")
        args = parser.parse_args()

        # Se ha introducido una ruta como argumento
        if args.dataSet: 
            self.ds = uoc_ds(args.dataSet).get_df()
            return
        # No se ha introducido una ruta como argumento   
        while True:
            for n, opcion in enumerate(opciones_datasets, start=1):
                print(f"{n}. {opcion}")
            opcion_elegida = input("Seleccione uno de los data sets disponibles (introduzca 1 o 2): ")
            if opcion_elegida not in ["1","2"]:
                print("Opción inválida. Por favor, introduzca 1 o 2.")
                continue
            if opcion_elegida == "1": # rendimiento estudiantes
                self.ds = uoc_ds("data/rendiment_estudiants.xlsx").get_df()
            elif opcion_elegida == "2": # tasa de abandono
                self.ds = uoc_ds("data/taxa_abandonament.xlsx").get_df()
            break
    
    def apartado_1(self) -> None:
        if self.ds is not None:
            print(self.ds.head())


    def apartado_2(self) -> None:
        if self.ds is not None:
            print(self.ds.columns.to_list())    

    def apartado_3(self) -> None:
        if self.ds is not None:
            print(self.ds.info())

