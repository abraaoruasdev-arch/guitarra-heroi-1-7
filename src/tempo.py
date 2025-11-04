#       Define velocidade das notas
def calcular_bpm_dificuldade(dificuldade, bpm):
    if dificuldade == "facil":
        return bpm/2
    elif dificuldade == "medio":
        return bpm
    elif dificuldade == "dificil":
        return bpm*2
    else:
        raise ValueError("Dificuldade inválida. Use 'facil', 'medio' ou 'dificil'.")

#       Define fall speed
def calcular_fall_speed(bpm, batidas_antes, y_inicial, y_hit):
    tempo_batida = 60 / bpm
    tempo_ate_hit = tempo_batida * batidas_antes
    distancia = y_hit - y_inicial
    return distancia / tempo_ate_hit

#       Define tempo de spawn da nota
def calcular_intervalo_spawn(bpm, notas_por_batida):
    tempo_batida = 60 / bpm
    return tempo_batida / notas_por_batida

#   Calculo para cada musica

