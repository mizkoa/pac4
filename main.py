import argparse
import os
from uocdataset.uocdataset import UOCDataset as uoc_ds

def main() -> None:
    opciones_datasets = ["Rendimiento estudiantes", "Tasa de abandono"]
    parser = argparse.ArgumentParser(
        description="Introducir una ruta del archivo a procesar o elegir uno de los disponibles"
    )
	
    # nargs="?": allows that positional argument to appear zero or one time. Without it, argparse would demand exactly one value; with it, the argument becomes optional.
    parser.add_argument("dataSet", nargs="?", help="Elegir uno de los data sets disponibles")
    args = parser.parse_args()

    # Se ha introducido una ruta como argumento
    if args.dataSet:
         # Comprobamos que la ruta de origen existe y es un archivo
        if not os.path.exists(args.dataSet) or not os.path.isfile(args.dataSet):
            print(f"La ruta de origen {args.dataSet} no existe o no es un archivo")
            return
        else:
            uoc_obj = uoc_ds(args.dataSet)
            print(args.dataSet)
            return
    # No se ha introducido una ruta como argumento   
    while True:
        for n, opcion in enumerate(opciones_datasets, start=1):
            print(f"{n}. {opcion}")
        opcion_elegida = input("Seleccione uno de los data sets disponibles (introduzca 1 o 2): ")

        if opcion_elegida not in ["1","2"]:
            print("Opción inválida. Por favor, introduzca 1 o 2.")
            continue
        if opcion_elegida == "1":
            # Rendimiento estudiantes"
            print("Rendimiento estudiantes")
           # uoc_ds("/data/rendiment_estudiants.xlsx")
            uoc_obj = uoc_ds(os.path.join(os.path.dirname(__file__), "data", "rendiment_estudiants.xlsx"))
            # uoc_obj.info()


        elif opcion_elegida == "2":
            print("Tasa de abandono")
        
        print (f"Ha seleccionado la opción {opcion_elegida}")
        break
       
if __name__ == "__main__":
	main()
