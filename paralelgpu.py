import arrayfire as af
import threading

# ==========================================
# PARTE 1: CONFIGURAÇÃO
# ==========================================

# Mude para True para testar com 1 GPU só
TESTAR_1_GPU = True

# Tenta usar OpenCL (padrão AMD)
try:
    af.set_backend(af.BACKEND_OPENCL)
except:
    pass

# Lista onde cada GPU vai guardar seu resultado
resultados = []

# ==========================================
# PARTE 2: FUNÇÃO QUE CADA GPU EXECUTA
# ==========================================

def tarefa_gpu(numero_gpu, nome_gpu):
    """
    Essa função roda em cada GPU.
    Faz: cria duas matrizes, multiplica, e guarda o total.
    """

    # Escolhe qual GPU usar
    af.set_device(numero_gpu)

    # Cria duas matrizes com números aleatórios (1024 linhas x 512 colunas)
    matriz1 = af.randu(1024, 512)
    matriz2 = af.randu(1024, 512)

    # Multiplica as duas matrizes
    resultado = matriz1 * matriz2

    # Espera a GPU terminar
    af.sync()

    # Soma todos os números do resultado em um só
    total = af.sum(resultado)
    af.sync()

    # Guarda o resultado na lista
    resultados.append({'nome': nome_gpu, 'valor': float(total)})

    print(f"[{nome_gpu}] Pronto! Resultado = {float(total):.2f}")

# ==========================================
# PARTE 3: DETECTAR QUANTAS GPUs TEM
# ==========================================

print("Detectando GPUs...")
num_gpus = af.get_device_count()
print(f"GPUs encontradas: {num_gpus}")

if TESTAR_1_GPU:
    print("MODO TESTE: Forçando 1 GPU")
    num_gpus = 1

# ==========================================
# PARTE 4: RODAR NAS GPUs DISPONÍVEIS
# ==========================================

print("Iniciando...")

if num_gpus >= 2:
    # Tem 2 GPUs - roda em paralelo
    print("Modo: 2 GPUs paralelas")

    thread_1 = threading.Thread(target=tarefa_gpu, args=(0, "GPU_0"))
    thread_2 = threading.Thread(target=tarefa_gpu, args=(1, "GPU_1"))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

elif num_gpus == 1:
    # Tem 1 GPU - roda tudo nela
    print("Modo: 1 GPU só")

    tarefa_gpu(0, "GPU_0")

else:
    print("Nenhuma GPU encontrada!")
    exit()

# ==========================================
# PARTE 5: MOSTRAR O RESULTADO FINAL
# ==========================================

print("")
print("--- RESULTADO ---")

soma_final = 0
for r in resultados:
    print(f"  {r['nome']}: {r['valor']:.2f}")
    soma_final += r['valor']

print(f"  TOTAL:   {soma_final:.2f}")
print("-----------------")
