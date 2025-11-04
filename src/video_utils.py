import pygame
import cv2
import numpy as np

def carregar_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise Exception(f"Não foi possível abrir o vídeo: {path}")
    return cap

def ler_frame(cap, largura, altura):
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
    frame = cv2.resize(frame, (largura, altura))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    surf = pygame.surfarray.make_surface(np.rot90(frame))
    return surf

def liberar_video(cap):
    cap.release()
