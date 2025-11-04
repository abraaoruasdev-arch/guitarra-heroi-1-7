# Configuração da imagem do título do menu inicial
TITULO_IMG_PATH = "assets/titulo.png"
TITULO_IMG_X = 80
TITULO_IMG_Y = 60
TITULO_IMG_LARGURA = 600
TITULO_IMG_ALTURA = 200

# Configuracao imagem dificulade
LARGURA_IMG_DIF, ALTURA_IMG_DIF, X_IMG_DIF,Y_IMG_DIF = 600, 600, 100, 0

# Configuracao tela final
LARGURA_TELA_FINAL = 100
ALTURA_TELA_FINAL = 300

# Constantes
LARGURA_TELA = 800
ALTURA_TELA = 600
EFFECT_DURATION = 0.15
TRILHA_SONORA_PATH = "assets/musicas/trilha_sonora.mp3"

    # Config do menu inicial
largura_img = 300
altura_img = 61
espaco_x = 60
espaco_y = 30
col1_x = 80
col2_x = 80 + largura_img + espaco_x
linha1_y = 200
MENU_IMG_DIMENSOES = [
	(col1_x, linha1_y, largura_img, altura_img),  # 1
	(col2_x, linha1_y, largura_img, altura_img),  # 2
	(col1_x, linha1_y + (altura_img + espaco_y), largura_img, altura_img),  # 3
	(col2_x, linha1_y + (altura_img + espaco_y), largura_img, altura_img),  # 4
	(col1_x, linha1_y + 2*(altura_img + espaco_y), largura_img, altura_img),  # 5
	(col2_x, linha1_y + 2*(altura_img + espaco_y), largura_img, altura_img),  # 6
	(col1_x, linha1_y + 3*(altura_img + espaco_y), largura_img, altura_img),  # 7
	(col2_x, linha1_y + 3*(altura_img + espaco_y), largura_img, altura_img),  # 8
]
# Caminhos das imagens do menu
MENU_IMG_PATHS = [
	"assets/novosfundos/MENUcalifornication.jpg",
	"assets/novosfundos/MENUamericanidiot.jpg",
	"assets/novosfundos/MENUdumb.jpg",
	"assets/novosfundos/MENUfeelgood.jpg",
	"assets/novosfundos/MENUtheemptinessmachine.jpg",
	"assets/novosfundos/MENUheartshapedbox.jpg",
	"assets/novosfundos/MENUbackinblack.jpg",
	"assets/novosfundos/MENUtnt.jpg",
]

# Variavies de posicao
hitVerde_x, hitVerde_y = 168, 0
hitVermelho_x, hitVermelho_y = 295, 0
hitAmarelo_x, hitAmarelo_y = 428, 0
hitAzul_x, hitAzul_y = 558, 0

    # Barra de ativacao
ativacaoInicial, ativacaoFinal = 460, 550
barraAtv_x, barraAtv_y = 150, 510

# Variaveis de controle
fallSpeed = 0
tempoMusica = 0
duracaoMusicas = 60  # segundos




