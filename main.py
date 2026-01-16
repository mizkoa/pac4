import ejercicios as sol

def main() -> None:
  
   
   ejercicio_1 : sol.Ejercicio_1 = sol.Ejercicio_1()
   ejercicio_1.apartado_1()
   ejercicio_1.apartado_2()
   ejercicio_1.apartado_3()


   ejercicio_2 : sol.Ejercicio_2 = sol.Ejercicio_2()
   ejercicio_2.apartado_1()
   ejercicio_2.apartado_2()
   ejercicio_2.apartado_3()
   ejercicio_2.apartado_4()

   ejercicio_3 : sol.Ejercicio_3 = sol.Ejercicio_3()
   ejercicio_3.apartado_1(show_graph=False)
   ejercicio_3.apartado_2()

   ejercicio_4 : sol.Ejercicio_4 = sol.Ejercicio_4()
   ejercicio_4.analyze_dataset(show_json=True)



       
if __name__ == "__main__":
	main()
