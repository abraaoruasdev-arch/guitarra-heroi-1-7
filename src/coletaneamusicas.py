import var
import pygame
from abc import ABC, abstractmethod

class Musica(ABC): # HERANCA - Classe pai, MUSICA abstrata, FUNDO polimorfismo
    def __init__(self, nome, bpm, duracao, chance_acorde, chance_contratempo, arquivo=None, arquivo_fundo=None, video_fundo=None):
        self.nome = nome
        self.bpm = bpm
        self.duracao = duracao
        self.chance_acorde = chance_acorde
        self.chance_contratempo = chance_contratempo
        self.arquivo = arquivo
        self.arquivo_fundo = arquivo_fundo
        self.video_fundo = video_fundo  # Caminho do vídeo de fundo

    def tempo_batida(self):
        return 60 / self.bpm

    def tempo_meia_batida(self):
        return self.tempo_batida() / 2

    # Return de informacoes da musica
    @abstractmethod
    def __str__(self):
        pass

    # Altera fundo de acordo com a musica
    @abstractmethod
    def get_fundo(self):
        pass
    


# Musicas - Classes filhas
class Californication(Musica):
    def __init__(self):
        super().__init__(
            nome="Red Hot Chili Peppers - Californication",
            bpm=96,
            duracao=var.duracaoMusicas,
            chance_acorde=0.01,
            chance_contratempo=0.75,
            arquivo="assets/musicas/californication.mp3",
            video_fundo="assets/fundos/californication.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"
    
    def get_fundo(self):
        return "assets/fundos/californication.png"

class AmericanIdiot(Musica):
    def __init__(self):
        super().__init__(
            nome="Green Day - American Idiot",
            bpm=93,
            duracao=var.duracaoMusicas,
            chance_acorde=0.1,
            chance_contratempo=0.9,
            arquivo="assets/musicas/american_idiot.mp3",
            video_fundo="assets/fundos/americanidiot.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"
    
    def get_fundo(self):
        return "assets/fundos/americanidiot.png"
    

class Dumb(Musica):
    def __init__(self):
        super().__init__(
            nome="Nirvana - Dumb",
            bpm=114,
            duracao=var.duracaoMusicas,
            chance_acorde=0,
            chance_contratempo=0.65,
            arquivo="assets/musicas/dumb.mp3",
            video_fundo="assets/fundos/dumb.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"

    def get_fundo(self):
        return "assets/fundos/dumb.png"
    
class FeelGood(Musica):
    def __init__(self):
        super().__init__(
            nome="Gorillaz - Feel Good Inc",
            bpm=139,
            duracao=var.duracaoMusicas,
            chance_acorde=0,
            chance_contratempo=0.50,
            arquivo="assets/musicas/feel_good.mp3",
            video_fundo="assets/fundos/feelgood.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"

    def get_fundo(self):
        return "assets/fundos/feelgood.png"
    
class TheEmptinessMachine(Musica):
    def __init__(self):
        super().__init__(
            nome="Linkin Park - The Emptiness Machine",
            bpm=92.25,
            duracao=var.duracaoMusicas,
            chance_acorde=0.15,
            chance_contratempo=0.7,
            arquivo="assets/musicas/the_emptiness_machine.mp3",
            video_fundo="assets/fundos/theemptinessmachine.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"

    def get_fundo(self):
        return "assets/fundos/theemptinessmachine.png"
    
class HeartShapedBox(Musica):
    def __init__(self):
        super().__init__(
            nome="Nirvana - Heart-Shaped Box",
            bpm=101,
            duracao=var.duracaoMusicas,
            chance_acorde=0.1,
            chance_contratempo=0.8,
            arquivo="assets/musicas/heart_shaped_box.mp3",
            video_fundo="assets/fundos/heartshapedbox.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"

    def get_fundo(self):
        return "assets/fundos/heartshapedbox.png"
    
class BackInBlack(Musica):
    def __init__(self):
        super().__init__(
            nome="AC DC - Back In Black",
            bpm=94.5,
            duracao=var.duracaoMusicas,
            chance_acorde=0.1,
            chance_contratempo=0.4,
            arquivo="assets/musicas/back_in_black.mp3",
            video_fundo="assets/fundos/backinblack.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"

    def get_fundo(self):
        return "assets/fundos/backinblack.png"
    
class TNT(Musica):
    def __init__(self):
        super().__init__(
            nome="AC DC - T.N.T",
            bpm=126,
            duracao=var.duracaoMusicas,
            chance_acorde=0.5,
            chance_contratempo=0.02,
            arquivo="assets/musicas/tnt.mp3",
            video_fundo="assets/fundos/tnt.mp4"
        )
    def __str__(self):
        return f"{self.nome} ({self.bpm} BPM, {self.duracao}s)"

    def get_fundo(self):
        return "assets/fundos/tnt.png"
    


    # Função para tocar as musicas
def tocar_musica(path, loop=True):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if loop else 0)
    except Exception as e:
        print(f"Erro ao tocar música: {e}")
