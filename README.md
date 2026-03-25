# Parallel GPU Calculator

Calculadora de matrizes em paralelo que detecta automaticamente 1 ou 2 GPUs.

## Descrição do repositório

```
Calculadora de matrizes usando ArrayFire com detecção automática de GPUs. Roda em paralelo em 1 ou 2 placas de vídeo via OpenCL.
```

## O que faz

- Detecta quantas GPUs existem no computador
- Cria matrizes com números aleatórios
- Multiplica as matrizes na GPU (muito mais rápido que na CPU)
- Mostra o resultado final

## Requisitos

- Python 3
- ArrayFire
- GPU com suporte a OpenCL

## Instalação

```bash
pip install arrayfire
```

## Como rodar

```bash
python paralelgpu.py
```

## Variável de teste

No topo do código tem uma variável pra forçar o modo de teste:

```python
# Mude para True para testar com 1 GPU só
TESTAR_1_GPU = True
```

| Valor | O que acontece |
|-------|----------------|
| `True` | Força modo 1 GPU (pra testar no seu PC) |
| `False` | Detecta quantas GPUs tem normalmente |

## Exemplo de saída

```
Detectando GPUs...
GPUs encontradas: 2
MODO TESTE: Forçando 1 GPU
Iniciando...
Modo: 1 GPU só
[GPU_0] Pronto! Resultado = 131266.44

--- RESULTADO ---
  GPU_0: 131266.44
  TOTAL: 131266.44
-----------------
```

## Explicação do código

### PARTE 1 - Configuração

```python
import arrayfire as af
import threading

TESTAR_1_GPU = True

try:
    af.set_backend(af.BACKEND_OPENCL)
except:
    pass
```

- `arrayfire` - Biblioteca pra fazer cálculos na GPU
- `threading` - Pra rodar funções ao mesmo tempo (paralelo)
- `TESTAR_1_GPU` - Variável booleana pra forçar modo de teste
- `set_backend` - Tenta usar OpenCL (padrão AMD)

### PARTE 2 - Função da GPU

```python
def tarefa_gpu(numero_gpu, nome_gpu):
    af.set_device(numero_gpu)       # Escolhe qual GPU usar
    matriz1 = af.randu(1024, 512)   # Cria matriz aleatória
    matriz2 = af.randu(1024, 512)   # Cria outra matriz
    resultado = matriz1 * matriz2   # Multiplica as matrizes
    af.sync()                       # Espera a GPU terminar
    total = af.sum(resultado)       # Soma todos os elementos
    af.sync()                       # Espera de novo
    resultados.append(...)          # Guarda o resultado
```

- `set_device` - Seleciona qual GPU usar (0 ou 1)
- `randu` - Cria matriz com números aleatórios entre 0 e 1
- `*` - Multiplicação elemento a elemento
- `sync` - Espera a GPU terminar antes de continuar
- `sum` - Soma todos os elementos em um único número

### PARTE 3 - Detecção de GPUs

```python
num_gpus = af.get_device_count()    # Conta quantas GPUs tem

if TESTAR_1_GPU:                    # Se True, força 1 GPU
    num_gpus = 1
```

- `get_device_count` - Retorna quantas GPUs o ArrayFire encontrou
- Se `TESTAR_1_GPU = True`, ignora a detecção e usa 1 GPU

### PARTE 4 - Execução

```python
if num_gpus >= 2:                   # Tem 2 GPUs
    thread_1 = threading.Thread(target=tarefa_gpu, args=(0, "GPU_0"))
    thread_2 = threading.Thread(target=tarefa_gpu, args=(1, "GPU_1"))
    thread_1.start()                # Dispara thread 1
    thread_2.start()                # Dispara thread 2
    thread_1.join()                 # Espera thread 1 terminar
    thread_2.join()                 # Espera thread 2 terminar

elif num_gpus == 1:                 # Tem 1 GPU
    tarefa_gpu(0, "GPU_0")          # Roda tudo nessa GPU

else:                               # Não tem GPU
    print("Nenhuma GPU encontrada!")
```

- `Thread` - Cria uma thread (tarefa paralela)
- `start` - Dispara a thread
- `join` - Espera a thread terminar
- Se tem 2 GPUs: roda em paralelo
- Se tem 1 GPU: roda tudo nela
- Se tem 0 GPUs: mostra erro e para

### PARTE 5 - Resultado

```python
soma_final = 0
for r in resultados:
    print(f"  {r['nome']}: {r['valor']:.2f}")
    soma_final += r['valor']

print(f"  TOTAL:   {soma_final:.2f}")
```

- Percorre a lista de resultados
- Mostra o valor de cada GPU
- Soma tudo no total final

## Resumo visual

```
┌─────────────────────────────────────────────┐
│           PARTE 1: Configuração             │
│  Importa bibliotecas, define TESTAR_1_GPU   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         PARTE 2: Função da GPU              │
│  Cria matrizes, multiplica, soma, guarda    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        PARTE 3: Detecção de GPUs            │
│  Conta GPUs, aplica TESTAR_1_GPU se True    │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼────┐        ┌─────▼─────┐
    │ 1 GPU   │        │ 2 GPUs    │
    │ Seque-  │        │ Paralelo  │
    │ cial    │        │ Threads   │
    └────┬────┘        └─────┬─────┘
         │                   │
         └─────────┬─────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          PARTE 5: Resultado                 │
│  Mostra valor de cada GPU e total final     │
└─────────────────────────────────────────────┘
```

## Arquivos

- `paralelgpu.py` - Código principal
- `README.md` - Este arquivo
- `.gitignore` - Arquivos que não vão pro GitHub

## Licença

MIT
