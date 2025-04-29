import pygame
import sys
import random
import os

# Initialisation
pygame.init()

# Dimensions
TAILLE_FENETRE = 600
TAILLE_CASE = 20
FPS_INITIAL = 10
FPS_MAX = 30
OBSTACLE_MOVE_TIME = 3000

# Fichiers
HIGH_SCORE_FILE = 'high_score.txt'
IMAGE_ACCUEIL = 'assets/images/snake-start.png'

# Fenetre
screen = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption('Snake Classique - Neon Violet')
clock = pygame.time.Clock()

# Police
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 120)

# Charger ressources
try:
    wall_img = pygame.image.load('assets/images/wall.png')
    wall_img = pygame.transform.scale(wall_img, (TAILLE_CASE, TAILLE_CASE))
    accueil_img = pygame.image.load(IMAGE_ACCUEIL)
    accueil_img = pygame.transform.scale(accueil_img, (TAILLE_FENETRE, TAILLE_FENETRE))
    pygame.mixer.music.load('assets/sounds/background_music.mp3')
    eat_sound = pygame.mixer.Sound('assets/sounds/eat.wav')
    gameover_sound = pygame.mixer.Sound('assets/sounds/gameover.wav')
except Exception as e:
    print(f"Erreur lors du chargement des ressources: {e}")
    pygame.quit()
    sys.exit()

pygame.mixer.music.play(-1)

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
GRIS = (100, 100, 100)
ORANGE = (255, 165, 0)

# Difficulté initiale
DIFFICULTE = 3

# Variables globales
def charger_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def sauvegarder_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

high_score = charger_high_score()

# Fonctions diverses

def afficher_ecran_accueil():
    fondu = pygame.Surface((TAILLE_FENETRE, TAILLE_FENETRE))
    for alpha in range(255, -1, -10):
        screen.blit(accueil_img, (0, 0))
        fondu.set_alpha(alpha)
        fondu.fill(NOIR)
        screen.blit(fondu, (0, 0))
        titre = font.render('Appuie sur ESPACE pour commencer', True, BLANC)
        screen.blit(titre, (TAILLE_FENETRE // 2 - titre.get_width() // 2, TAILLE_FENETRE - 80))
        pygame.display.update()
        pygame.time.delay(30)

    attendre = True
    while attendre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attendre = False

def calculer_nombre_murs():
    NOMBRE_CASES = (TAILLE_FENETRE // TAILLE_CASE) ** 2
    return (NOMBRE_CASES * DIFFICULTE) // 50

def generer_murs():
    murs = set()
    while len(murs) < calculer_nombre_murs():
        x = random.randint(1, (TAILLE_FENETRE // TAILLE_CASE) - 2) * TAILLE_CASE
        y = random.randint(1, (TAILLE_FENETRE // TAILLE_CASE) - 2) * TAILLE_CASE
        murs.add((x, y))
    return list(murs)

def obtenir_description_difficulte(niveau):
    if niveau <= 3:
        return "Facile"
    elif niveau <= 7:
        return "Moyen"
    else:
        return "Difficile"

def couleur_difficulte(niveau):
    if niveau <= 3:
        return VERT
    elif niveau <= 7:
        return ORANGE
    else:
        return ROUGE

def afficher_score(score):
    texte = font.render(f"Score: {score}  High Score: {high_score}", True, BLANC)
    screen.blit(texte, (10, 10))

def dessiner_contour():
    pygame.draw.rect(screen, BLANC, (0, 0, TAILLE_FENETRE, TAILLE_FENETRE), 5)

def effet_crash():
    screen.fill(ROUGE)
    pygame.display.update()
    pygame.time.delay(150)

def game_over(score):
    global high_score
    if score > high_score:
        high_score = score
        sauvegarder_high_score(high_score)

    gameover_sound.play()
    screen.fill(NOIR)
    texte = font.render(f"Game Over! Score: {score}", True, ROUGE)
    high_score_text = font.render(f"High Score: {high_score}", True, BLANC)
    instruction = font.render("Espace: Rejouer | Échap: Quitter", True, BLANC)
    screen.blit(texte, (TAILLE_FENETRE // 2 - texte.get_width() // 2, TAILLE_FENETRE // 2 - 60))
    screen.blit(high_score_text, (TAILLE_FENETRE // 2 - high_score_text.get_width() // 2, TAILLE_FENETRE // 2 - 20))
    screen.blit(instruction, (TAILLE_FENETRE // 2 - instruction.get_width() // 2, TAILLE_FENETRE // 2 + 30))
    pygame.display.update()

    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attente = False
                    menu_demarrage()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def compte_a_rebours():
    for i in range(3, 0, -1):
        for taille in range(30, 121, 10):
            screen.fill(NOIR)
            font_temp = pygame.font.SysFont(None, taille)
            texte = font_temp.render(str(i), True, (255, 255, 0))
            screen.blit(texte, (TAILLE_FENETRE // 2 - texte.get_width() // 2, TAILLE_FENETRE // 2 - texte.get_height() // 2))
            dessiner_contour()
            pygame.display.update()
            pygame.time.delay(50)
        pygame.time.delay(300)

def menu_selection_difficulte():
    global DIFFICULTE
    selecting = True
    while selecting:
        screen.fill(NOIR)
        titre = font.render('Sélectionnez la difficulté', True, BLANC)
        niveau = font.render(f'Difficulté actuelle: {DIFFICULTE} - {obtenir_description_difficulte(DIFFICULTE)}', True, BLANC)
        instruction = font.render('← / → pour ajuster | Entrée pour valider', True, BLANC)

        screen.blit(titre, (TAILLE_FENETRE // 2 - titre.get_width() // 2, TAILLE_FENETRE // 4))
        screen.blit(niveau, (TAILLE_FENETRE // 2 - niveau.get_width() // 2, TAILLE_FENETRE // 2))
        screen.blit(instruction, (TAILLE_FENETRE // 2 - instruction.get_width() // 2, TAILLE_FENETRE // 2 + 50))

        barre_largeur = 300
        barre_hauteur = 20
        barre_x = TAILLE_FENETRE // 2 - barre_largeur // 2
        barre_y = TAILLE_FENETRE // 2 + 100
        pygame.draw.rect(screen, GRIS, (barre_x, barre_y, barre_largeur, barre_hauteur))
        pygame.draw.rect(screen, couleur_difficulte(DIFFICULTE), (barre_x, barre_y, (barre_largeur * DIFFICULTE) // 10, barre_hauteur))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and DIFFICULTE > 1:
                    DIFFICULTE -= 1
                if event.key == pygame.K_RIGHT and DIFFICULTE < 10:
                    DIFFICULTE += 1
                if event.key == pygame.K_RETURN:
                    selecting = False

def menu_demarrage():
    murs = generer_murs()
    screen.fill(NOIR)
    titre = font.render('Snake Classique', True, BLANC)
    instruction = font.render('Espace: Commencer | Échap: Quitter', True, BLANC)
    screen.blit(titre, (TAILLE_FENETRE // 2 - titre.get_width() // 2, TAILLE_FENETRE // 3))
    screen.blit(instruction, (TAILLE_FENETRE // 2 - instruction.get_width() // 2, TAILLE_FENETRE // 2))
    dessiner_contour()
    pygame.display.update()

    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    en_attente = False
                    compte_a_rebours()
                    demarrer_jeu(murs)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def demarrer_jeu(walls):
    snake = [(200, 200)]
    snake_direction = (TAILLE_CASE, 0)
    pomme = random.choice([(x, y) for x in range(0, TAILLE_FENETRE, TAILLE_CASE) for y in range(0, TAILLE_FENETRE, TAILLE_CASE) if (x, y) not in walls])
    score = 0
    fps = FPS_INITIAL
    pygame.time.set_timer(pygame.USEREVENT, OBSTACLE_MOVE_TIME)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, TAILLE_CASE):
                    snake_direction = (0, -TAILLE_CASE)
                if event.key == pygame.K_DOWN and snake_direction != (0, -TAILLE_CASE):
                    snake_direction = (0, TAILLE_CASE)
                if event.key == pygame.K_LEFT and snake_direction != (TAILLE_CASE, 0):
                    snake_direction = (-TAILLE_CASE, 0)
                if event.key == pygame.K_RIGHT and snake_direction != (-TAILLE_CASE, 0):
                    snake_direction = (TAILLE_CASE, 0)

        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        if snake[0] == pomme:
            eat_sound.play()
            pomme = random.choice([(x, y) for x in range(0, TAILLE_FENETRE, TAILLE_CASE) for y in range(0, TAILLE_FENETRE, TAILLE_CASE) if (x, y) not in walls and (x, y) not in snake])
            score += 10
            fps = min(fps + 0.5, FPS_MAX)
        else:
            snake.pop()

        if (snake[0][0] < 0 or snake[0][0] >= TAILLE_FENETRE or
            snake[0][1] < 0 or snake[0][1] >= TAILLE_FENETRE or
            snake[0] in snake[1:] or
            snake[0] in walls):
            effet_crash()
            game_over(score)
            return

        screen.fill(NOIR)
        for bloc in snake:
            pygame.draw.rect(screen, VERT, (bloc[0], bloc[1], TAILLE_CASE, TAILLE_CASE))
        pygame.draw.ellipse(screen, ROUGE, (pomme[0], pomme[1], TAILLE_CASE, TAILLE_CASE))
        for mur in walls:
            screen.blit(wall_img, mur)
        afficher_score(score)
        dessiner_contour()
        pygame.display.update()
        clock.tick(fps)

# Programme principal
if __name__ == "__main__":
    afficher_ecran_accueil()
    menu_selection_difficulte()
    menu_demarrage()