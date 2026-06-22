import random
import string
import time

import matplotlib.pyplot as plt


SEMILLA_ALEATORIA = 42
LARGO_MINIMO = 5
LARGO_MAXIMO = 15
REPETICIONES = 1
NOMBRE_GRAFICO = "grafico_tiempos_scm.png"


def generar_texto_aleatorio(largo):
    """Genera un texto aleatorio con letras minusculas inglesas."""
    return "".join(random.choice(string.ascii_lowercase) for _ in range(largo))


def scm_division_conquista(x, y, i, j):
    """Calcula el largo de la SCM usando recursion pura."""
    if i == 0 or j == 0:
        return 0

    if x[i - 1] == y[j - 1]:
        return 1 + scm_division_conquista(x, y, i - 1, j - 1)

    quitar_de_x = scm_division_conquista(x, y, i - 1, j)
    quitar_de_y = scm_division_conquista(x, y, i, j - 1)
    return max(quitar_de_x, quitar_de_y)


def scm_programacion_dinamica(x, y):
    """Calcula el largo de la SCM usando una tabla de programacion dinamica."""
    filas = len(x) + 1
    columnas = len(y) + 1
    dp = [[0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(1, filas):
        for j in range(1, columnas):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[len(x)][len(y)]


def medir_tiempo(funcion, argumentos, repeticiones):
    """Ejecuta una funcion y retorna su resultado y tiempo promedio."""
    if repeticiones < 1:
        raise ValueError("La cantidad de repeticiones debe ser al menos 1.")

    tiempo_total = 0.0
    resultado = None

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado_actual = funcion(*argumentos)
        fin = time.perf_counter()

        if resultado is None:
            resultado = resultado_actual
        elif resultado != resultado_actual:
            raise ValueError("La funcion produjo resultados inconsistentes.")

        tiempo_total += fin - inicio

    return resultado, tiempo_total / repeticiones


def ejecutar_experimento():
    """Genera datos, ejecuta ambos algoritmos y guarda sus resultados."""
    random.seed(SEMILLA_ALEATORIA)
    resultados = []

    for n in range(LARGO_MINIMO, LARGO_MAXIMO + 1):
        x = generar_texto_aleatorio(n)
        y = generar_texto_aleatorio(n)

        resultado_dc, tiempo_dc = medir_tiempo(
            scm_division_conquista,
            (x, y, len(x), len(y)),
            REPETICIONES,
        )
        resultado_dp, tiempo_dp = medir_tiempo(
            scm_programacion_dinamica,
            (x, y),
            REPETICIONES,
        )

        if resultado_dc != resultado_dp:
            mensaje_error = (
                "Error: los algoritmos entregaron resultados distintos.\n"
                f"n: {n}\n"
                f"X: {x}\n"
                f"Y: {y}\n"
                f"Division y conquista: {resultado_dc}\n"
                f"Programacion dinamica: {resultado_dp}"
            )
            raise ValueError(mensaje_error)

        resultados.append(
            {
                "n": n,
                "x": x,
                "y": y,
                "scm": resultado_dc,
                "tiempo_division_conquista": tiempo_dc,
                "tiempo_programacion_dinamica": tiempo_dp,
            }
        )

    return resultados


def ejecutar_pruebas_conocidas():
    """Valida ambos algoritmos con casos conocidos de SCM."""
    casos = [
        ("ABCBDAB", "BDCABA", 4),
        ("abcde", "ace", 3),
        ("abc", "def", 0),
        ("abc", "abc", 3),
    ]

    for x, y, esperado in casos:
        resultado_dc = scm_division_conquista(x, y, len(x), len(y))
        resultado_dp = scm_programacion_dinamica(x, y)

        if resultado_dc != esperado or resultado_dp != esperado:
            raise AssertionError(
                f"Fallo con X={x}, Y={y}. "
                f"Esperado={esperado}, "
                f"Division y conquista={resultado_dc}, "
                f"Programacion dinamica={resultado_dp}"
            )


def mostrar_resultados(resultados):
    """Muestra una tabla ordenada con los resultados del experimento."""
    encabezado = (
        f"{'n':>2}  {'X':<15}  {'Y':<15}  {'SCM':>3}  "
        f"{'Tiempo division y conquista':>29}  "
        f"{'Tiempo programacion dinamica':>30}"
    )
    separador = "-" * len(encabezado)

    print(encabezado)
    print(separador)

    for fila in resultados:
        print(
            f"{fila['n']:>2}  "
            f"{fila['x']:<15}  "
            f"{fila['y']:<15}  "
            f"{fila['scm']:>3}  "
            f"{fila['tiempo_division_conquista']:>29.10f}  "
            f"{fila['tiempo_programacion_dinamica']:>30.10f}"
        )


def graficar_resultados(resultados):
    """Grafica los tiempos de ejecucion y guarda la imagen PNG."""
    tamanos = [fila["n"] for fila in resultados]
    tiempos_dc = [fila["tiempo_division_conquista"] for fila in resultados]
    tiempos_dp = [
        fila["tiempo_programacion_dinamica"] for fila in resultados
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(
        tamanos,
        tiempos_dc,
        color="tab:red",
        marker="o",
        label="Division y conquista",
    )
    plt.plot(
        tamanos,
        tiempos_dp,
        color="tab:blue",
        marker="s",
        label="Programacion dinamica",
    )

    plt.title("Comparacion de tiempos de ejecucion para SCM")
    plt.xlabel("Tamano de entrada (n)")
    plt.ylabel("Tiempo de ejecucion (segundos, escala log)")
    plt.yscale("log")
    plt.xticks(tamanos)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(NOMBRE_GRAFICO, dpi=300)
    plt.show()


def main():
    ejecutar_pruebas_conocidas()
    resultados = ejecutar_experimento()
    mostrar_resultados(resultados)
    graficar_resultados(resultados)
    print(f"\nGrafico guardado como: {NOMBRE_GRAFICO}")


if __name__ == "__main__":
    main()
