import cv2
import numpy as np
import pygame
import mediapipe as mp

# Constantes
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CHARACTER_SIZE = 50
MOVE_SPEED = 5
JUMP_HEIGHT = 10
GRAVITY = 2

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Control de Juegos con Gestos")

# Cargar el personaje
character = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
character.fill((0, 255, 0))  # Color verde

# Variables de juego
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Posición inicial del personaje
jump = False
clock = pygame.time.Clock()

# Inicializar la cámara y MediaPipe
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def detect_gesture(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Calcular el desplazamiento
            movement_x = index_finger.x - wrist.x
            movement_y = index_finger.y - wrist.y

            # Ajustar los umbrales para detectar gestos
            if abs(movement_x) > 0.1:  # Movimiento horizontal
                return "left" if movement_x < 0 else "right"
            elif abs(movement_y) > 0.1:  # Movimiento vertical
                return "up" if movement_y < 0 else "down"

    return None

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            exit()

    # Captura de video
    ret, frame = cap.read()
    if not ret:
        break

    # Detección de gestos
    gesture = detect_gesture(frame)

    # Lógica de movimiento
    if gesture == "left" and x > 0:
        x -= MOVE_SPEED  # Mover a la izquierda
    elif gesture == "right" and x < SCREEN_WIDTH - CHARACTER_SIZE:
        x += MOVE_SPEED  # Mover a la derecha
    elif gesture == "up" and not jump:
        jump = True  # Activar salto

    # Simulación de salto
    if jump:
        y -= JUMP_HEIGHT
        if y < SCREEN_HEIGHT // 2:  # Altura máxima del salto
            jump = False
    else:
        if y < SCREEN_HEIGHT - CHARACTER_SIZE:
            y += GRAVITY  # Efecto de gravedad

    # Limpiar pantalla
    screen.fill((0, 0, 0))
    screen.blit(character, (x, y))

    # Mostrar el frame de la cámara en una ventana de OpenCV
    cv2.imshow("Gestos de la Mano", frame)

    pygame.display.flip()
    clock.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()