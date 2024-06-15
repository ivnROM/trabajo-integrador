import os
import formula


def limpiar_pantalla() -> None:
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def main() -> None:
    ecuacion = formula.Ecuacion(0.1, 50)
    while True:
        print("Elija una opción: ")
        ans = int(input("(1) Mostrar datos calculados\n(2) Ingresar una coordenada para el cálculo de error\n(3) Mostrar historial de coordenadas y error\n(4) Buscar un dato en la lista ingresando el tiempo\n(5) Buscar un dato en la lista ingresando la variable dependiente o su valor más cercano\n(6) Salir del programa\n"))
        match ans:
            case 1: 
                limpiar_pantalla()
                ecuacion.mostrar_datos()
            case 2:
                limpiar_pantalla()
                print("2")
            case 3:
                limpiar_pantalla()
                print("3")
            case 4:
                limpiar_pantalla()
                print("4")
            case 5:
                limpiar_pantalla()
                print("5")
            case 6:
                limpiar_pantalla()
                break
            case _:
                limpiar_pantalla()
                print("Opción invalida")




main()
