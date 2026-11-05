
# Nombre: [Omar Reyes Gonzalez]
# Matrícula: [202216]


import time
import sys

# Acotamiento del tiempo de ejecución para algoritmos recursivos
sys.setrecursionlimit(3000)

# Definición de la entrada constante de precios
PRECIOS = (0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30)

def obtener_precio(p: tuple, i: int) -> int:
    """Función auxiliar para manejar precios más allá del tamaño base PRECIOS."""
    if i < len(p):
        return p[i]
    # Extensión lógica si n > 10 basada en bloques
    return p[10] * (i // 10) + p[i % 10]


# 1. Implementacion Recursiva Pura Con Cortes

def cut_rod_recursive(p: tuple, n: int) -> tuple[int, list[int]]:
    """
    Función recursiva para calcular el máximo ingreso y sus cortes.
    """
    if n == 0:
        return 0, []
    q = -1
    best_cuts = []
    for i in range(1, n + 1):
        precio_i = obtener_precio(p, i)
        rem_rev, rem_cuts = cut_rod_recursive(p, n - i)
        if precio_i + rem_rev > q:
            q = precio_i + rem_rev
            best_cuts = [i] + rem_cuts
    return q, best_cuts


# 2. Implementacion de memorizacion  (Con Cortes)

def cut_rod_memoized(p: tuple, n: int) -> tuple[int, list[int]]:
    """
    Función recursiva con caché (memoización) y reconstrucción de cortes.
    """
    r = [-1] * (n + 1)
    s = [0] * (n + 1)
    
    def memo_aux(n):
        if r[n] >= 0:
            return r[n]
        if n == 0:
            q = 0
        else:
            q = -1
            for i in range(1, n + 1):
                precio_i = obtener_precio(p, i)
                val = precio_i + memo_aux(n - i)
                if val > q:
                    q = val
                    s[n] = i
        r[n] = q
        return q
    
    max_rev = memo_aux(n)
    
    #  cortes óptimos
    cuts = []
    temp_n = n
    while temp_n > 0:
        c = s[temp_n]
        cuts.append(c)
        temp_n -= c
    return max_rev, cuts


# 3. Implementacion con tabulacion  (Con Cortes)

def cut_rod_tabulation(p: tuple, n: int) -> tuple[int, list[int]]:
    """
    Función iterativa utilizando tabulación (Bottom-Up) y reconstrucción de cortes.
    """
    r = [0] * (n + 1)
    s = [0] * (n + 1)
    
    for j in range(1, n + 1):
        q = -1
        for i in range(1, j + 1):
            precio_i = obtener_precio(p, i)
            if q < precio_i + r[j - i]:
                q = precio_i + r[j - i]
                s[j] = i
        r[j] = q
        
    # cortes óptimos
    cuts = []
    temp_n = n
    while temp_n > 0:
        c = s[temp_n]
        cuts.append(c)
        temp_n -= c
        
    return r[n], cuts


# BENCHMARK 

def ejecutar_benchmark():
    longitudes = [5, 10, 15, 20, 25, 28, 30]
    
    print(f"{'Longitud':<10} | {'Recursivo (s)':<15} | {'Memoizado (s)':<15} | {'Tabulación (s)':<15} | {'Ingreso':<8} | {'Cortes'}")
    print("-" * 90)
    
    for n in longitudes:
        # 1. Recursivo (limitado a n <= 10 por su complejidad exponencial O(2^n))
        if n <= 10:
            inicio = time.perf_counter()
            _, _ = cut_rod_recursive(PRECIOS, n)
            t_rec = f"{time.perf_counter() - inicio:.6f}"
        else:
            t_rec = "Inviable (O(2^n))"
            
        # 2. Memoización
        inicio = time.perf_counter()
        memo_val, memo_cortes = cut_rod_memoized(PRECIOS, n)
        t_memo = f"{time.perf_counter() - inicio:.6f}"
        
        # 3. Tabulación
        inicio = time.perf_counter()
        tab_val, tab_cortes = cut_rod_tabulation(PRECIOS, n)
        t_tab = f"{time.perf_counter() - inicio:.6f}"
        
        print(f"{n:<10} | {t_rec:<15} | {t_memo:<15} | {t_tab:<15} | ${memo_val:<7} | {memo_cortes}")

# Ejecutar benchmark si se corre directamente
if __name__ == "__main__":
    ejecutar_benchmark()