import pygame
import var
from tempo import calcular_fall_speed, calcular_intervalo_spawn, calcular_bpm_dificuldade
from coletaneamusicas import Californication, AmericanIdiot, Dumb, FeelGood, TheEmptinessMachine, HeartShapedBox, BackInBlack, TNT


# Menu inicial
def mostrar_menu_video(screen, video_cap):
    import pygame
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)
    musicas = [
        Californication(),
        AmericanIdiot(),
        Dumb(),
        FeelGood(),
        TheEmptinessMachine(),
        HeartShapedBox(),
        BackInBlack(),
        TNT()
    ]

    # Carregar imagem do título
    try:
        titulo_img = pygame.image.load(var.TITULO_IMG_PATH).convert_alpha()
        titulo_img = pygame.transform.scale(titulo_img, (var.TITULO_IMG_LARGURA, var.TITULO_IMG_ALTURA))
    except Exception as e:
        print(f"[ERRO] Falha ao carregar imagem do título: {var.TITULO_IMG_PATH} - {e}")
        titulo_img = None

    # Carregar imagens das musicas no menu
    menu_imgs = []
    for path, (x, y, w, h) in zip(var.MENU_IMG_PATHS, var.MENU_IMG_DIMENSOES):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (w, h))
            menu_imgs.append(img)
        except Exception as e:
            print(f"[ERRO] Falha ao carregar imagem do menu: {path} - {e}")
            menu_imgs.append(None)
    clock = pygame.time.Clock()
    musica_escolhida = None
    dificuldade = None
    etapa = 'musica'  # ou 'dificuldade'
    difs = {
        pygame.K_1: "facil",
        pygame.K_2: "medio",
        pygame.K_3: "dificil"
    }
    while True:
        # Preenche o fundo da tela inicial com a cor RGB (0, 0, 1)
        screen.fill((0, 0, 1))
        # Desenha opções sobre o vídeo
        if etapa == 'musica':
            # Imagem do título
            if titulo_img:
                screen.blit(titulo_img, (var.TITULO_IMG_X, var.TITULO_IMG_Y))
            # Apenas imagens e números
            for idx, img in enumerate(menu_imgs):
                x, y, w, h = var.MENU_IMG_DIMENSOES[idx]
                # Número à esquerda da imagem, centralizado verticalmente
                num_text = small_font.render(f"[{idx+1}]", True, (255,255,255))
                num_rect = num_text.get_rect()
                num_y = y + (h - num_rect.height)//2
                screen.blit(num_text, (x - num_rect.width - 10, num_y))
                if img:
                    screen.blit(img, (x, y))
                else:
                    pygame.draw.rect(screen, (255,0,0), (x, y, w, h), 2)
            screen.blit(small_font.render("Pressione 1-8 para escolher", True, (255,255,255)), (220, 550))
        elif etapa == 'dificuldade':
            # Limpa a área das opções de música desenhando um retângulo opaco sobre ela
            # (ajuste a área conforme necessário para cobrir todas as opções)
            min_x = min([x for (x, y, w, h) in var.MENU_IMG_DIMENSOES]) - 60
            min_y = min([y for (x, y, w, h) in var.MENU_IMG_DIMENSOES]) - 20
            max_x = max([x + w for (x, y, w, h) in var.MENU_IMG_DIMENSOES]) + 60
            max_y = max([y + h for (x, y, w, h) in var.MENU_IMG_DIMENSOES]) + 40
            pygame.draw.rect(screen, (0, 0, 0), (min_x, min_y, max_x - min_x, max_y - min_y))
            # Carregar e mostrar imagem de seleção de dificuldade
            try:
                escolhadif_img = pygame.image.load("assets/escolhadif.png").convert_alpha()
                escolhadif_img = pygame.transform.scale(escolhadif_img, (var.LARGURA_IMG_DIF, var.ALTURA_IMG_DIF))
                screen.blit(escolhadif_img, (var.X_IMG_DIF, var.Y_IMG_DIF))
            except Exception as e:
                print(f"[ERRO] Falha ao carregar imagem de dificuldade: assets/escolhadif.png - {e}")
                # Desenhar um retângulo reserva no lugar da imagem caso falhe
                pygame.draw.rect(screen, (200,200,200), (var.X_IMG_DIF, var.Y_IMG_DIF, var.LARGURA_IMG_DIF, var.ALTURA_IMG_DIF), 2)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if etapa == 'musica' and event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    idx = event.key - pygame.K_KP1
                else:
                    idx = None
                if idx is not None and 0 <= idx < len(musicas):
                    musica_escolhida = musicas[idx]
                    etapa = 'dificuldade'
            elif etapa == 'dificuldade' and event.type == pygame.KEYDOWN and event.key in difs:
                dificuldade = difs[event.key]
                # Calcular parâmetros
                bpm_dif = calcular_bpm_dificuldade(dificuldade, musica_escolhida.bpm)
                fall_speed = calcular_fall_speed(bpm_dif, 2, 0, var.ativacaoInicial)
                intervalo_spawn = calcular_intervalo_spawn(bpm_dif, 1)
                if dificuldade == "facil":
                    intervalo_spawn *= 2
                    musica_escolhida.chance_acorde = 0
                    musica_escolhida.chance_contratempo = 0.1
                return musica_escolhida, dificuldade, fall_speed, intervalo_spawn
        clock.tick(30)

# Tela de score (Final)
# Espera acao do usuario
def mostrar_score_video(screen, acertos, erros, aproveitamento):
    import pygame
    small_font = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()
    # Carregar imagens final
    try:
        img_final = pygame.image.load("assets/final.png").convert_alpha()
        img_final = pygame.transform.scale(img_final, (600, 450))

        img_titulo_final = pygame.image.load("assets/game_over.png").convert_alpha()
        img_titulo_final = pygame.transform.scale(img_titulo_final, (600, 450))
    except Exception as e:
        print(f"[ERRO] Falha ao carregar imagem final: assets/final.png - {e}")
        img_final = None


    while True:
        # Fundo preto
        screen.fill((0, 0, 1))
        # Desenha imagem final centralizada na parte inferior
        if img_final:
            screen.blit(img_final, (var.LARGURA_TELA_FINAL, var.ALTURA_TELA_FINAL))
            screen.blit(img_titulo_final, (100, -75))
        # Opções sobre o fundo
        screen.blit(small_font.render(f"Notas acertadas: {acertos}", True, (0,255,0)), (200, 320))
        screen.blit(small_font.render(f"Notas erradas: {erros}", True, (255,0,0)), (200, 360))
        screen.blit(small_font.render(f"Aproveitamento: {aproveitamento:.1f}%", True, (255,255,0)), (200, 400))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()
                if event.key == pygame.K_r:
                    return "replay"
                if event.key == pygame.K_n:
                    return "novo"
        clock.tick(30)
