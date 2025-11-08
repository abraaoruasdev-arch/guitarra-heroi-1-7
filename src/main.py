# Teste commit

import var  # Variaveis globais  
from menu import mostrar_menu_video, mostrar_score_video
from hud import Contador, ContadorErros, desenhar_hud
from coletaneamusicas import tocar_musica, Californication, AmericanIdiot, Dumb, FeelGood, TheEmptinessMachine, HeartShapedBox, BackInBlack, TNT
from video_utils import carregar_video, ler_frame, liberar_video
import numpy as np
import pygame
import random
import time

# region    2. Hit

class Hit:
    def __init__(self, imagem, x, yInicial, teclaHit, velocidade):
        self.imagem = imagem
        self.x = x
        self.y = yInicial
        self.teclaHit = teclaHit
        self.ativa = True
        self.pontuada = False 
        self.velocidade = velocidade
        
    
    def atualizar(self ,dt):
        if self.y < var.ALTURA_TELA:  # Verifica se a nota ainda esta na tela
            self.y += self.velocidade * dt
    
    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))
    
    def verificarHit(self, event, contador):
        if event.type == pygame.KEYDOWN and event.key == self.teclaHit:
            if self.ativa and var.ativacaoInicial < self.y < var.ativacaoFinal:
                contador.valor += 1
                self.pontuada = True     # marca como pontuada
                self.ativa = False       # desativa para não contar de novo

    def removerHit(self):
        return self.pontuada or self.y >= var.ALTURA_TELA
    
    def errou(self):
        return self.y >= var.ALTURA_TELA and not self.pontuada

# endregion

# region    3. Funcoes

    # Processa evento
def processarEventos(notas, contador):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "voltar_menu"
            # Ativa efeito branco ao pressionar a tecla
            if event.key in lane_effects:
                lane_effects[event.key]["active"] = True
                lane_effects[event.key]["color"] = (255, 255, 255)
                lane_effects[event.key]["timer"] = var.EFFECT_DURATION
            # Verifica acerto de nota
            for nota in notas:
                if nota.teclaHit == event.key:
                    antes = nota.pontuada
                    nota.verificarHit(event, contador)
                    # Se acertou a nota, muda cor do efeito para cor da lane
                    if not antes and nota.pontuada:
                        for lane in lanes:
                            if lane["tecla"] == event.key:
                                lane_effects[event.key]["color"] = lane["cor"]
                                lane_effects[event.key]["timer"] = var.EFFECT_DURATION
    return True


#   Spawn de acorde (duas notas simultâneas)
def spawn_acorde(notas, lanes, lane, chance_acorde):
    if random.random() < chance_acorde:
        outra_lane = random.choice([l for l in lanes if l != lane])
        notas.append(Hit(outra_lane["imagem"], outra_lane["x"], 0, outra_lane["tecla"], var.fallSpeed))

#   Spawn de contratempo (nota extra meia batida depois)
def spawn_contratempo(spawns_agendados, lanes, agora, meia_batida, chance_contratempo):
    if random.random() < chance_contratempo:
        spawn_time = agora + meia_batida
        lane_contratempo = random.choice(lanes)
        spawns_agendados.append((spawn_time, lane_contratempo))

# Função para processar notas agendadas (contratempos)
def processar_spawns_agendados(spawns_agendados, notas, agora):
    for spawn in spawns_agendados[:]:  # copia para evitar problemas ao remover
        tempo_spawn, lane_ct = spawn
        if agora >= tempo_spawn:
            notas.append(Hit(lane_ct["imagem"], lane_ct["x"], 0, lane_ct["tecla"], var.fallSpeed))
            spawns_agendados.remove(spawn)

#   Escolher uma lane diferente da última
def escolher_nova_lane(lanes, ultima_lane):
    return random.choice([l for l in lanes if l != ultima_lane])

# endregion

# region    4. Iniciando Jogo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((var.LARGURA_TELA, var.ALTURA_TELA))
clock = pygame.time.Clock()

# Toca trilha sonora no menu inicial
tocar_musica(var.TRILHA_SONORA_PATH, loop=True)

# endregion

# region    5. Carregando imagens

imgHitVerde = (pygame.image.load("assets/hitVerde.png").convert_alpha())
imgHitVerde = pygame.transform.scale(imgHitVerde, (75, 75))

imgHitVermelho = (pygame.image.load("assets/hitVermelho.png").convert_alpha())
imgHitVermelho = pygame.transform.scale(imgHitVermelho, (75, 75))

imgHitAmarelo = (pygame.image.load("assets/hitAmarelo.png").convert_alpha())
imgHitAmarelo = pygame.transform.scale(imgHitAmarelo, (75, 75))

imgHitAzul = (pygame.image.load("assets/hitAzul.png").convert_alpha())
imgHitAzul = pygame.transform.scale(imgHitAzul, (75, 75))

imgBarraAtivacao = (pygame.image.load("assets/barra_ativacao-r.png").convert_alpha())
imgBarraAtivacao = pygame.transform.scale(imgBarraAtivacao, (500, 75))


# endregion

# region    6. Configuracoes

lanes = [
    {"x": var.hitVerde_x,    "tecla": pygame.K_a, "imagem": imgHitVerde,    "cor": (0,255,0)},
    {"x": var.hitVermelho_x, "tecla": pygame.K_s, "imagem": imgHitVermelho, "cor": (255,0,0)},
    {"x": var.hitAmarelo_x,  "tecla": pygame.K_d, "imagem": imgHitAmarelo,  "cor": (255,255,0)},
    {"x": var.hitAzul_x,     "tecla": pygame.K_f, "imagem": imgHitAzul,     "cor": (0,128,255)},
]

# Trocar para imagens ou gifs para animacoes.
lane_effects = {
    pygame.K_a: {"active": False, "color": (255,255,255), "timer": 0},
    pygame.K_s: {"active": False, "color": (255,255,255), "timer": 0},
    pygame.K_d: {"active": False, "color": (255,255,255), "timer": 0},
    pygame.K_f: {"active": False, "color": (255,255,255), "timer": 0},
}

contador = Contador()
contadorErros = ContadorErros()
font = pygame.font.SysFont(None, 48)
notas = []
spawns_agendados = []

# endregion


# region    7. Menu Inicial

video_menu = None
musica_escolhida, dificuldade, fall_speed, intervalo_spawn = mostrar_menu_video(screen, video_menu)


# Carrega vídeo de fundo da música escolhida
video_fundo = None
if hasattr(musica_escolhida, "video_fundo") and musica_escolhida.video_fundo:
    video_fundo = carregar_video(musica_escolhida.video_fundo)

# Toca música escolhida pelo jogador durante a fase
if hasattr(musica_escolhida, "arquivo"):
    pygame.mixer.music.load(musica_escolhida.arquivo)
    pygame.mixer.music.play()
else:
    pass

# Define parâmetros de tempo conforme música e dificuldade
tempo_batida = 60 / musica_escolhida.bpm
meia_batida = tempo_batida / 2

# Define duração da fase e inicializa tempos
duracao_fase = var.duracaoMusicas
var.fallSpeed = fall_speed
intervalo_base = intervalo_spawn
inicio_fase = time.time()
ultimo_spawn = time.time()
ultima_lane = None

# endregion

# region    8. LOOP PRINCIPAL
running = True
frame_fundo = None
while running:
    dt = clock.tick(60) / 1000.0  # segundos
    evento = processarEventos(notas, contador)
    if evento == False:
        break
    if evento == "voltar_menu":
        # Para a música da fase
        pygame.mixer.music.stop()
        # Inicia trilha sonora do menu
        tocar_musica(var.TRILHA_SONORA_PATH, loop=True)
        # Volta para tela inicial de escolha de música e dificuldade
        musica_escolhida, dificuldade, fall_speed, intervalo_spawn = mostrar_menu_video(screen, video_menu)
        tempo_batida = 60 / musica_escolhida.bpm
        meia_batida = tempo_batida / 2
        duracao_fase = var.duracaoMusicas
        var.fallSpeed = fall_speed
        intervalo_base = intervalo_spawn
        notas = []
        spawns_agendados = []
        contador.valor = 0
        contadorErros.valor = 0
        inicio_fase = time.time()
        ultimo_spawn = time.time()
        tempo_passado = 0
        ultima_lane = None
        # Reinicia vídeo de fundo da música
        if video_fundo:
            liberar_video(video_fundo)
        if hasattr(musica_escolhida, "video_fundo") and musica_escolhida.video_fundo:
            video_fundo = carregar_video(musica_escolhida.video_fundo)
        # Toca música escolhida pelo jogador
        if hasattr(musica_escolhida, "arquivo"):
            pygame.mixer.music.load(musica_escolhida.arquivo)
            pygame.mixer.music.play()
        continue

    agora = time.time()
    tempo_passado = int(agora - inicio_fase)
    if tempo_passado >= duracao_fase:
        # Toca trilha sonora na tela final
        tocar_musica(var.TRILHA_SONORA_PATH, loop=True)
        pontos = contador.valor
        erros = contadorErros.valor
        acertos = pontos
        total = acertos + erros
        aproveitamento = (acertos / total * 100) if total > 0 else 0.0
        acao = mostrar_score_video(screen, acertos, erros, aproveitamento)
        if acao == "replay":
            # Reinicia variáveis principais para nova partida
            notas = []
            spawns_agendados = []
            contador.valor = 0
            contadorErros.valor = 0
            inicio_fase = time.time()
            ultimo_spawn = time.time()
            tempo_passado = 0
            # Reinicia vídeo de fundo da música
            if video_fundo:
                liberar_video(video_fundo)
            if hasattr(musica_escolhida, "video_fundo") and musica_escolhida.video_fundo:
                video_fundo = carregar_video(musica_escolhida.video_fundo)
            # Toca música escolhida novamente
            if hasattr(musica_escolhida, "arquivo"):
                pygame.mixer.music.load(musica_escolhida.arquivo)
                pygame.mixer.music.play()
            continue
        elif acao == "novo":
            # Volta para tela inicial de escolha de música e dificuldade
            musica_escolhida, dificuldade, fall_speed, intervalo_spawn = mostrar_menu_video(screen, video_menu)
            tempo_batida = 60 / musica_escolhida.bpm
            meia_batida = tempo_batida / 2
            duracao_fase = var.duracaoMusicas
            var.fallSpeed = fall_speed
            intervalo_base = intervalo_spawn
            notas = []
            spawns_agendados = []
            contador.valor = 0
            contadorErros.valor = 0
            inicio_fase = time.time()
            ultimo_spawn = time.time()
            tempo_passado = 0
            ultima_lane = None
            # Reinicia vídeo de fundo da música
            if video_fundo:
                liberar_video(video_fundo)
            if hasattr(musica_escolhida, "video_fundo") and musica_escolhida.video_fundo:
                video_fundo = carregar_video(musica_escolhida.video_fundo)
            # Toca música escolhida pelo jogador
            if hasattr(musica_escolhida, "arquivo"):
                pygame.mixer.music.load(musica_escolhida.arquivo)
                pygame.mixer.music.play()
            continue
        else:
            break

    # Atualiza frame do vídeo de fundo
    if video_fundo:
        frame_fundo = ler_frame(video_fundo, var.LARGURA_TELA, var.ALTURA_TELA)
        screen.blit(frame_fundo, (0, 0))
    else:
        # fallback: cor sólida
        screen.fill((0, 0, 0))

    if agora - ultimo_spawn >= intervalo_base:
        lane = escolher_nova_lane(lanes, ultima_lane)
        ultima_lane = lane
        notas.append(Hit(lane["imagem"], lane["x"], 0, lane["tecla"], var.fallSpeed))
        spawn_acorde(notas, lanes, lane, musica_escolhida.chance_acorde)
        spawn_contratempo(spawns_agendados, lanes, agora, meia_batida, musica_escolhida.chance_contratempo)
        ultimo_spawn = agora
        intervalo_base = tempo_batida

    processar_spawns_agendados(spawns_agendados, notas, agora) # Verifica se é hora de criar notas agendadas

    for nota in notas:
        nota.atualizar(dt)
    for key in lane_effects:
        if lane_effects[key]["active"]:
            lane_effects[key]["timer"] -= dt
            if lane_effects[key]["timer"] <= 0:
                lane_effects[key]["active"] = False

    novas = []
    for nota in notas:
        if nota.removerHit():
            if nota.errou():
                contadorErros.valor += 1
        else:
            novas.append(nota)
    notas = novas
    desenhar_hud(screen, notas, imgBarraAtivacao,
             contador, contadorErros, font, tempo_passado, duracao_fase, lanes, lane_effects)
    pygame.display.flip()
# endregion
if video_fundo:
    liberar_video(video_fundo)
if 'video_menu' in locals():
    liberar_video(video_menu)
pygame.quit()