import pygame
import var

# Classe para contar pontos e erros
# ENCAPSULAMENTO 
class Contador:
    def __init__(self):
        self._valor = 0 # Dado protegido

    @property # Getter valor
    def valor(self):
        return self._valor

    @valor.setter # Setter valor
    def valor(self, novo_valor):
        self._valor = novo_valor

class ContadorErros:
    def __init__(self):
        self._valor = 0

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        self._valor = novo_valor


efeito_imgs = None

def desenhar_hud(screen, notas, imgBarraAtivacao,
             contador, contadorErros, font, tempo_passado, duracao_fase, lanes, lane_effects):
    global efeito_imgs
    if efeito_imgs is None:
        try:
            efeito_imgs = {
                pygame.K_a: pygame.transform.scale(pygame.image.load("assets/fogoverde.png").convert_alpha(), (75, 75)),
                pygame.K_s: pygame.transform.scale(pygame.image.load("assets/fogovermelho.png").convert_alpha(), (75, 75)),
                pygame.K_d: pygame.transform.scale(pygame.image.load("assets/fogoamarelo.png").convert_alpha(), (75, 75)),
                pygame.K_f: pygame.transform.scale(pygame.image.load("assets/fogoazul.png").convert_alpha(), (75, 75)),
            }
        except Exception as e:
            print(f"[ERRO] Falha ao carregar imagens de efeito: {e}")
            efeito_imgs = {}

    for nota in notas:
        nota.desenhar(screen)

    # Desenha efeitos de ativação sobre cada lane usando imagens
    for lane in lanes:
        key = lane["tecla"]
        if efeito_imgs and lane_effects[key]["active"] and key in efeito_imgs:
            screen.blit(efeito_imgs[key], (lane["x"], var.ativacaoInicial))

    screen.blit(imgBarraAtivacao, (var.barraAtv_x, var.barraAtv_y))

    texto_pontos = font.render(f"Pontos: {contador.valor}", True, (255, 255, 255))
    texto_erros = font.render(f"Erros: {contadorErros.valor}", True, (255, 0, 0))
    restante = max(0, duracao_fase - tempo_passado)
    texto_tempo = font.render(f"Tempo: {restante}s", True, (255, 255, 255))

    screen.blit(texto_pontos, (20, 20))
    screen.blit(texto_erros, (20, 50))
    screen.blit(texto_tempo, (20, 80))
