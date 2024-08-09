import pygame
import random
import time
import pandas as pd

# Inicializando o Pygame
pygame.init()

# Configurando a tela para a resolução do computador
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Simple Present English Game")

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Carregando fontes
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Carregando e redimensionando imagens
def load_and_resize_image(path, width, height):
    image = pygame.image.load(path).convert_alpha()  # Use convert_alpha() to keep transparency
    return pygame.transform.scale(image, (width, height))

# Função para carregar questões do arquivo Excel
def load_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    questions = []
    images = {}
    for index, row in df.iterrows():
        image_path = row['imagem']
        if image_path not in images:
            images[image_path] = load_and_resize_image(image_path, 400, 400)
        question = {
            "image": image_path,
            "correct": row['correta'],
            "options": [row['opcao1'], row['opcao2'], row['opcao3'], row['opcao4']]
        }
        questions.append(question)
    return questions, images

# Carregar questões e imagens
questions, images = load_questions_from_excel('questions.xlsx')

def draw_teams(teams, surface, font, x, y):
    """Desenha a lista de times na tela na posição (x, y)."""
    for i, team in enumerate(teams):
        text = f"Team {i+1}: {team}"
        draw_text_with_background(text, font, WHITE, DARK_GREEN, GREEN, surface, x, y + i * 40, 300, 30, 10)

# Função para desenhar texto na tela com fundo verde escuro e bordas arredondadas
def draw_text_with_background(text, font, text_color, bg_color, border_color, surface, x, y, width, height, border_radius):
    textobj = font.render(text, True, text_color)
    textrect = textobj.get_rect(center=(x + width // 2, y + height // 2))
    # Desenha o fundo com bordas arredondadas
    pygame.draw.rect(surface, border_color, (x, y, width, height), border_radius=border_radius)
    pygame.draw.rect(surface, bg_color, (x + 2, y + 2, width - 4, height - 4), border_radius=border_radius)
    surface.blit(textobj, textrect)

# Função para exibir mensagem de acerto ou erro
def show_feedback(surface, message, bg_color, duration):
    surface.fill(bg_color)
    textobj = large_font.render(message, True, WHITE)
    textrect = textobj.get_rect(center=(screen_width // 2, screen_height // 2))
    surface.blit(textobj, textrect)
    pygame.display.flip()
    pygame.time.wait(duration)

# Tela inicial do jogo
def main_menu():
    teams = []
    corner_image = load_and_resize_image("if.png", 200, 200)
    corner_image2 = load_and_resize_image("cc.png", 200, 200)
    corner_image3 = load_and_resize_image("edukar.png", 200, 200)
    while True:
        screen.fill(BLACK)
        
        # Exibir a tela inicial
        draw_text_with_background("Welcome!", large_font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 400, 250, 800, 60, 20)
        draw_text_with_background("Game Simple Present", large_font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 400, 320, 800, 60, 15)
        draw_text_with_background("Create Team", font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 80, screen_height // 2 - 50, 160, 50, 15)
        draw_text_with_background("Start Game", font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 80, screen_height // 2 + 10, 160, 50, 15)
        draw_text_with_background("Exit", font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 50, screen_height // 2 + 70, 100, 50, 15)
        screen.blit(corner_image, (10, screen_height - corner_image.get_height() - 10))
        screen.blit(corner_image2, (230, screen_height - corner_image2.get_height() - 10))
        screen.blit(corner_image3, (450, screen_height - corner_image3.get_height() - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Verifica se o clique está dentro do botão "Create Team"
                if screen_width // 2 - 80 < x < screen_width // 2 + 80 and screen_height // 2 - 50 < y < screen_height // 2:
                    team_name = create_team()
                    if team_name:
                        teams.append(team_name)
                # Verifica se o clique está dentro do botão "Start Game"
                elif screen_width // 2 - 80 < x < screen_width // 2 + 80 and screen_height // 2 + 10 < y < screen_height // 2 + 60:
                    if teams:
                        return teams
                    else:
                        show_feedback(screen, "Please create at least one team!", RED, 2000)
                # Verifica se o clique está dentro do botão "Exit"
                elif screen_width // 2 - 50 < x < screen_width // 2 + 50 and screen_height // 2 + 70 < y < screen_height // 2 + 120:
                    pygame.quit()
                    return

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Tela para criar novos times
def create_team():
    input_box = pygame.Rect(screen_width // 2 - 100, 200, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    corner_image = load_and_resize_image("if.png", 200, 200)
    corner_image2 = load_and_resize_image("cc.png", 200, 200)
    corner_image3 = load_and_resize_image("edukar.png", 200, 200)
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    while True:
        screen.fill(BLACK)
        
        draw_text_with_background("Enter Team Name", large_font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 200, 100, 500, 50, 15)
        draw_text_with_background("Save", font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 160, screen_height // 2 + 50, 140, 50, 15)
        draw_text_with_background("Back", font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 + 20, screen_height // 2 + 50, 140, 50, 15)
        draw_text_with_background("Exit", font, WHITE, DARK_GREEN, GREEN, screen, screen_width // 2 - 50, screen_height // 2 + 110, 100, 50, 15)

        screen.blit(corner_image, (10, screen_height - corner_image.get_height() - 10))
        screen.blit(corner_image2, (230, screen_height - corner_image2.get_height() - 10))
        screen.blit(corner_image3, (450, screen_height - corner_image3.get_height() - 10))

        if active:
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, color, input_box, 2)
        else:
            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, color, input_box, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text:
                        return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                x, y = event.pos
                if screen_width // 2 - 160 < x < screen_width // 2 - 20 and screen_height // 2 + 50 < y < screen_height // 2 + 100:
                    if text:
                        return text
                elif screen_width // 2 + 20 < x < screen_width // 2 + 160 and screen_height // 2 + 50 < y < screen_height // 2 + 100:
                    return None
                elif screen_width // 2 - 50 < x < screen_width // 2 + 50 and screen_height // 2 + 110 < y < screen_height // 2 + 160:
                    pygame.quit()
                    return

        pygame.display.flip()
        clock.tick(30)

def game_screen(teams):
    current_question = random.choice(questions)
    correct_answer = current_question['correct']
    options = current_question['options']
    random.shuffle(options)
    score = {team: 0 for team in teams}
    corner_image = load_and_resize_image("if.png", 200, 200)
    corner_image2 = load_and_resize_image("cc.png", 200, 200)
    corner_image3 = load_and_resize_image("edukar.png", 200, 200)
    
    # Definindo as posições das opções
    option_positions = [
        (screen_width // 2 - 200, screen_height // 2 + 10),
        (screen_width // 2 - 200, screen_height // 2 + 80),
        (screen_width // 2 - 200, screen_height // 2 + 150),
        (screen_width // 2 - 200, screen_height // 2 + 220)
    ]

    option_rects = [
        pygame.Rect(pos[0], pos[1], 380, 50) for pos in option_positions
    ]
    
    while True:
        screen.fill(BLACK)
        
        # Desenhar as opções
        for i, option in enumerate(options):
            draw_text_with_background(option, font, WHITE, DARK_GREEN, GREEN, screen, *option_positions[i], 380, 50, 15)
        
        # Desenhar a imagem
        image = images[current_question['image']]
        screen.blit(image, (screen_width // 2 - image.get_width() // 2, 50))

        # Desenhar o quadrado com o nome do time atual e a pontuação
        current_team = teams[0]  # Time atual
        team_score = score[current_team]
        draw_text_with_background(f"Team: {current_team}", font, WHITE, DARK_GREEN, GREEN, screen, screen_width - 300, 20, 250, 50, 15)
        draw_text_with_background(f"Score: {team_score}", font, WHITE, DARK_GREEN, GREEN, screen, screen_width - 300, 70, 250, 50, 15)
        
        # Desenhar o botão "Exit" no canto inferior direito
        draw_text_with_background("Exit", font, WHITE, DARK_GREEN, GREEN, screen, screen_width - 160, screen_height - 60, 140, 50, 15)

        screen.blit(corner_image, (10, screen_height - corner_image.get_height() - 10))
        screen.blit(corner_image2, (230, screen_height - corner_image2.get_height() - 10))
        screen.blit(corner_image3, (450, screen_height - corner_image3.get_height() - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if screen_width - 160 < x < screen_width - 20 and screen_height - 60 < y < screen_height - 10:
                    pygame.quit()
                    return
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(x, y):
                        if options[i] == correct_answer:
                            show_feedback(screen, "Correct!", GREEN, 2000)
                            score[teams[0]] += 1
                        else:
                            show_feedback(screen, "Incorrect!", RED, 2000)
                        
                        # Selecionar próxima questão
                        teams.append(teams.pop(0))  # Mover para o próximo time
                        current_question = random.choice(questions)
                        correct_answer = current_question['correct']
                        options = current_question['options']
                        random.shuffle(options)
                        break

        pygame.display.flip()
        pygame.time.Clock().tick(30)



# Iniciar o jogo
teams = main_menu()
if teams:
    game_screen(teams)
