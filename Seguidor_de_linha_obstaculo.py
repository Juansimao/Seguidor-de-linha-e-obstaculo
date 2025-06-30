from machine import Pin, time_pulse_us
import time

# Motores
motor_esq_A = Pin(18, Pin.OUT)
motor_esq_B = Pin(19, Pin.OUT)
motor_dir_A = Pin(22, Pin.OUT)
motor_dir_B = Pin(23, Pin.OUT)

# Sensores de linha
sensor_esq = Pin(26, Pin.IN)
sensor_dir = Pin(27, Pin.IN)

# Sensor ultrassônico
trig = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)

# Variável de controle de estado
variavelx = False

# Função para medir distância
def medir_distancia():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duracao = time_pulse_us(echo, 1, 30000)
    if duracao < 0:
        return -1

    distancia = (duracao / 2) / 29.1
    return distancia

# Movimentos básicos
def parar():
    motor_esq_A.value(0)
    motor_esq_B.value(0)
    motor_dir_A.value(0)
    motor_dir_B.value(0)

def frente():
    motor_esq_A.value(1)
    motor_esq_B.value(0)
    motor_dir_A.value(1)
    motor_dir_B.value(0)

def curva_direita():
    motor_esq_A.value(1)
    motor_esq_B.value(0)
    motor_dir_A.value(0)
    motor_dir_B.value(1)

def curva_esquerda():
    motor_esq_A.value(0)
    motor_esq_B.value(1)
    motor_dir_A.value(1)
    motor_dir_B.value(0)

def todos_para_tras():
    motor_esq_A.value(0)
    motor_esq_B.value(1)
    motor_dir_A.value(0)
    motor_dir_B.value(1)

# Loop principal
while True:
    esq = sensor_esq.value()
    dir = sensor_dir.value()
    distancia = medir_distancia()

    print("Esq:", esq, "Dir:", dir, "Distância:", distancia, "cm", "Estado:", variavelx)

    if variavelx == False:
        # Modo normal - seguir linha
        if distancia >= 0 and distancia <= 13:
            print("Obstáculo detectado, entrando no modo desvio!")
            variavelx = True
            parar()
            time.sleep(0.2)
            continue

        # Seguidor de linha normal
 
        if esq == 0 and dir == 0:
            frente()
        elif esq == 1:
            curva_esquerda()
            if esq == 1 and dir == 1:
                frente()
                time.sleep(0.1)
        elif dir == 1:
            curva_direita()
            if esq == 1 and dir == 1:
                frente()
                time.sleep(0.1)

        else:
            parar()

    else:
        # Modo desvio
        print("Executando manobra de desvio...")
        parar()
        time.sleep(1)

        todos_para_tras()
        time.sleep(0.3)
        
        parar()
        time.sleep(0.2)

        curva_direita() #primeira virada direita
        time.sleep(0.80)
        parar()
        time.sleep(0.2)

        frente()	#primeira reta direta
        time.sleep(0.6)
        parar()
        time.sleep(0.2)

        curva_esquerda() #alinhar em paralelo ao objeto
        time.sleep(0.70)
        parar()
        time.sleep(0.2)
        
        frente() #andar paralelo ao objeto
        time.sleep(0.7)
        parar()
        time.sleep(0.2)
        
        curva_esquerda() #girar para voltar 
        time.sleep(0.40)
        parar()
        time.sleep(0.2)
        
        frente()  #ir reto para voltar 
        time.sleep(0.62)
        parar()
        time.sleep(0.5)
        

        variavelx = False  # volta ao modo normal

    time.sleep(0.01)





