import pygame
import random
import sys

pygame.init()

# Mengatur ukuran layar
width, height = 600, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Typing Shooter")

# Memuat efek suara game
sound_play = pygame.mixer.Sound("play.wav")
sound_shoot = pygame.mixer.Sound("shoot.wav")
sound_explode = pygame.mixer.Sound("explosion.wav")
sound_explode.set_volume(0.8)
sound_win = pygame.mixer.Sound("win.wav")
sound_lose = pygame.mixer.Sound("lose.wav")
sound_hit = pygame.mixer.Sound("hit.wav")
sound_powerup = pygame.mixer.Sound("power-up.wav")
sound_gameplay = pygame.mixer.Sound("gameplay.wav")
sound_gameplay.set_volume(0.2)
sound_menu = pygame.mixer.Sound("menu.wav")
sound_menu.set_volume(0.3)

# Memuat dan mengatur gambar
icon = pygame.image.load("logo-space.png")
pygame.display.set_icon(icon)
background_img = pygame.image.load("galaksi2.jpeg").convert()
background_img = pygame.transform.scale(background_img, (width, height))
ship_img = pygame.image.load("spaceship.png")
ship_img = pygame.transform.scale(ship_img, (80, 80))
virus_img = pygame.image.load("virus.png")
virus_img = pygame.transform.scale(virus_img, (80, 80))
arrow_img = pygame.image.load("arrows.png")
arrow_img = pygame.transform.scale(arrow_img, (50, 50))
heart_img = pygame.image.load("heart.png")
heart_img = pygame.transform.scale(heart_img, (40, 40))
book_img = pygame.image.load("book.png")
book_img = pygame.transform.scale(book_img, (80, 80))
small_book_img = pygame.transform.scale(book_img, (40, 40))
explosion_img = pygame.image.load("explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (80, 80))
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (25, 40))
pause_img = pygame.image.load("pause.png")
pause_img = pygame.transform.scale(pause_img, (50, 50))
button_bg_img = pygame.image.load("all-button.png")
button_bg_img = pygame.transform.scale(button_bg_img, (300, 120))
menu_box_img = pygame.image.load("menu-box.png")
menu_box_img = pygame.transform.scale(menu_box_img, (400, 300))

# Warna dan font
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white_transparent = (255, 255, 255, 60)
black_clear = (0, 0, 0, 0)
blue_transparent = (10, 10, 160, 180)
font = pygame.font.SysFont("arial", 32)
title_font = pygame.font.SysFont("agencyfb", 110)
button_font = pygame.font.SysFont("agencyfb", 60)
large_font = pygame.font.SysFont("arial", 72)

# Variabel game
words_list = ["python", "space", "asteroid", "rocket", "beyond", "impact", "variety", "justify", "develop", "why", "lily", "code", "ship", "arrange", "advanced", "programmer", "cybersecurity", "necessary", "resident", "innovation"]
words_to_type = random.sample(words_list * 3, 29) + ["coding destroys virus digital"]
special_words = ["technology", "future", "school"]
special_words_left = special_words[:]
special_words_spawned = []
active_words = []
bullets = []
explosions = []
word_spawn_delay = 600
last_spawn_time = pygame.time.get_ticks()
special_books_collected = 0
score = 0
lives = 3
ship_y = height - 100
menu = True
game_active = False
show_story = False
show_difficulty = False
difficulty = "Easy"

# Mengatur scrolling background
bg_y1 = 0
bg_y2 = -height
bg_scroll_speed = 1

# Fungsi scrolling background
def draw_scrolling_background():
    global bg_y1, bg_y2
    screen.blit(background_img, (0, bg_y1)) # Latar 1
    screen.blit(background_img, (0, bg_y2)) # Latar 2 (posisi di atas)
    bg_y1 += bg_scroll_speed
    bg_y2 += bg_scroll_speed
    if bg_y1 >= height:
        bg_y1 = -height # Reset posisi
    if bg_y2 >= height:
        bg_y2 = -height

# Fungsi gambar peluru
def draw_bullets():
    global bullets
    for bullet in bullets[:]:
        bullet[1] -= 10 # Peluru gerak ke atas
        if bullet[1] <= bullet[2]:
            bullets.remove(bullet)
        else:
            screen.blit(bullet_img, (bullet[0] - 10, bullet[1]))  

# Fungsi gambar nyawa
def draw_lives():
    for i in range(lives):
        screen.blit(heart_img, (width - 150 + i * 45, 10))

# Fungsi gambar buku
def draw_books():
    for i in range(special_books_collected):
        screen.blit(small_book_img, (width - 150 + i * 45, 60))

# Fungsi gambar menu utama
def draw_main_menu():
    draw_scrolling_background()
     
    # Judul
    title_text = title_font.render("Typing Shooter", True, white)
    screen.blit(title_text, title_text.get_rect(center=(width // 2, height // 2 - 180)))

    # Tombol play
    play_text = button_font.render("Play game", True, white)
    play_rect = play_text.get_rect(center=(width // 2, height // 2 + 80))
    play_bg_rect = button_bg_img.get_rect(center=play_rect.center)
    screen.blit(button_bg_img, play_bg_rect)
    screen.blit(play_text, play_rect)

    # Tombol story
    story_text = button_font.render("Story", True, white)
    story_rect = story_text.get_rect(center=(width // 2, height // 2 + 200))
    story_bg_rect = button_bg_img.get_rect(center=story_rect.center)
    screen.blit(button_bg_img, story_bg_rect)
    screen.blit(story_text, story_rect)

    return play_rect, story_rect

# Fungsi gambar menu difficulty
def draw_difficulty_menu():
    draw_scrolling_background()

    # Tombol kembali
    back_rect = pygame.Rect(20, 20, 50, 50)
    screen.blit(arrow_img, back_rect)

    # Kotak menu
    box_width, box_height = 600, 800
    box_x = width // 2 - box_width // 2
    box_y = height // 2 - box_height // 2
    screen.blit(pygame.transform.scale(menu_box_img, (box_width, box_height)), (box_x, box_y))

    # Judul
    title = button_font.render("Difficulty", True, white)
    title_rect = title.get_rect(center=(width // 2, box_y + 170))
    screen.blit(title, title_rect)

    # Tombol easy
    easy_text = button_font.render("Easy", True, white)
    easy_rect = easy_text.get_rect(center=(width // 2, box_y + 350))
    easy_bg_rect = button_bg_img.get_rect(center=easy_rect.center)
    screen.blit(button_bg_img, easy_bg_rect)
    screen.blit(easy_text, easy_rect)

    # Tombol hard
    hard_text = button_font.render("Hard", True, white)
    hard_rect = hard_text.get_rect(center=(width // 2, box_y + 500))
    hard_bg_rect = button_bg_img.get_rect(center=hard_rect.center)
    screen.blit(button_bg_img, hard_bg_rect)
    screen.blit(hard_text, hard_rect)

    return easy_rect, hard_rect, back_rect

# Fungsi gambar cerita
def draw_story_screen():
    draw_scrolling_background()
    back_rect = pygame.Rect(20, 20, 50, 50)
    screen.blit(arrow_img, back_rect)

    # Kotak cerita
    box_width, box_height = width - 40, 480
    box_x, box_y = 20, 180
    story_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    story_box.fill(black_clear)
    pygame.draw.rect(story_box, blue_transparent, (0, 0, box_width, box_height), border_radius=30)
    pygame.draw.rect(story_box, white_transparent, (10, 10, box_width - 20, box_height - 20), width= 4, border_radius=25)
    screen.blit(story_box, (box_x, box_y))

    # Teks cerita
    story_line1 = "Pada tahun 2050, virus digital berbahaya"
    story_line2 = "menyerang bumi. Mereka ingin"
    story_line3 = "menghancurkan sekolah dan masa"
    story_line4 = "depan anak-anak. Tapi harapan belum"
    story_line5 = "hilang. Anak-anak hebat bangkit! Dengan"
    story_line6 = "semangat belajar dan kemampuan"
    story_line7 = "teknologi, mereka bersatu melawan virus"
    story_line8 = "dan menyelamatkan masa depan."
    story_line9 = "Gunakan kekuatan codingmu untuk"
    story_line10 = "menyelamatkan dunia!"

    screen.blit(font.render(story_line1, True, white), (box_x + 30, box_y + 30))
    screen.blit(font.render(story_line2, True, white), (box_x + 30, box_y + 70))
    screen.blit(font.render(story_line3, True, white), (box_x + 30, box_y + 110))
    screen.blit(font.render(story_line4, True, white), (box_x + 30, box_y + 150))
    screen.blit(font.render(story_line5, True, white), (box_x + 30, box_y + 190))
    screen.blit(font.render(story_line6, True, white), (box_x + 30, box_y + 230))
    screen.blit(font.render(story_line7, True, white), (box_x + 30, box_y + 270))
    screen.blit(font.render(story_line8, True, white), (box_x + 30, box_y + 310))
    screen.blit(font.render(story_line9, True, white), (box_x + 30, box_y + 350))
    screen.blit(font.render(story_line10, True, white), (box_x + 30, box_y + 390))

    return back_rect

# Fungsi tampilan akhir layar (menang/kalah)
def show_end_screen(message):
    screen.blit(background_img, (0, 0))

    if message == "You Win":
        title_text = "You Win"
        title_color = green
        line2 = f"Score: {score}"
        line3 = "Kamu menyelamatkan sekolah"
        line4 = "dengan coding"
    else:
        title_text = "You lose"
        title_color = red
        line2 = f"Score: {score}"
        line3 = "Virus berhasil masuk."
        line4 = "Upgrade lagi skillmu!"

    text1 = large_font.render(title_text, True, title_color)
    text2 = font.render(line2, True, white)
    text3 = font.render(line3, True, white)
    text4 = font.render(line4, True, white)
    screen.blit(text1, text1.get_rect(center=(width // 2, height // 2 - 60)))
    screen.blit(text2, text2.get_rect(center=(width // 2, height // 2)))
    screen.blit(text3, text3.get_rect(center=(width // 2, height // 2 + 50)))
    screen.blit(text4, text4.get_rect(center=(width // 2, height // 2 + 90)))

    pygame.display.update()
    pygame.time.wait(3000)

# Fungsi tampilan pause
def pause_screen():

    # Kotak pause
    box_width, box_height = 600, 800
    box_x = width // 2 - box_width // 2
    box_y = height // 2 - box_height // 2
    screen.blit(pygame.transform.scale(menu_box_img, (box_width, box_height)), (box_x, box_y))

    # Tulisan paused
    paused_text = button_font.render("Game Paused", True, white)
    paused_rect = paused_text.get_rect(center=(width // 2, box_y + 170))
    screen.blit(paused_text, paused_rect)

    # Tombol resume
    resume_text = button_font.render("Resume", True, white)
    resume_rect = resume_text.get_rect(center=(width // 2, box_y + 350))
    resume_bg_rect = button_bg_img.get_rect(center=resume_rect.center)
    screen.blit(button_bg_img, resume_bg_rect)
    screen.blit(resume_text, resume_rect)

    # Tombol exit
    exit_text = button_font.render("Exit", True, white)
    exit_rect = exit_text.get_rect(center=(width // 2, box_y + 500))
    exit_bg_rect = button_bg_img.get_rect(center=exit_rect.center)
    screen.blit(button_bg_img, exit_bg_rect)
    screen.blit(exit_text, exit_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    sound_play.play()
                    pygame.mixer.music.unpause()
                    return "resume"
                elif exit_rect.collidepoint(event.pos):
                    sound_play.play()
                    pygame.mixer.music.stop()
                    return "exit"
        pygame.time.Clock().tick(60)

# Game loop
def run_game():
    global score, lives, bullets, words_to_type, bg_y1, bg_y2
    global special_books_collected, special_words_left, special_words_spawned, explosions
    pygame.mixer.music.load("gameplay.wav")
    pygame.mixer.music.play(-1)
    active_words.clear()
    bullets.clear()
    explosions.clear()
    score = 0
    lives = 3
    word_index = 0
    typed_inputs = {}
    current_target_id = None
    ship_x = width // 2 - 40
    clock = pygame.time.Clock()
    running = True
    last_spawn = pygame.time.get_ticks()
    special_books_collected = 0
    special_words_left = special_words[:]
    special_words_spawned = []
    bg_y1 = 0
    bg_y2 = -height
    while running:
        draw_scrolling_background()
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = event.unicode
                if current_target_id is not None:
                    word = next((w for w in active_words if w["id"] == current_target_id), None)
                    if word:
                        current_input = typed_inputs.get(word["id"], "")
                        if word["text"].startswith(current_input + key):
                            sound_shoot.play()
                            typed_inputs[word["id"]] = current_input + key
                            bullets.append([ship_x + 40, ship_y, word["y"] + 20])
                            if typed_inputs[word["id"]] == word["text"]:
                                explosions.append({"x": word["x"], "y": word["y"], "timer": 15})
                                if word.get("boss", False):
                                    sound_explode.play()
                                    score += 1
                                elif word["text"] in special_words:
                                    sound_powerup.play()
                                    special_books_collected += 1
                                else:
                                    sound_explode.play()
                                    score += 1
                                active_words.remove(word)
                                typed_inputs.pop(word["id"])
                                current_target_id = None
                else:
                    for word in active_words:
                        if word["text"].startswith(key):
                            current_target_id = word["id"]
                            typed_inputs[word["id"]] = key
                            sound_shoot.play()
                            bullets.append([ship_x + 40, ship_y, word["y"] + 20])
                            break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    sound_play.play()
                    pygame.mixer.music.pause()
                    result = pause_screen()
                    if result == "exit":
                        return
        
        if current_time - last_spawn > word_spawn_delay and (word_index < len(words_to_type) or len(special_words_left) > 0):
            if len(active_words) < 3:
                if len(special_words_left) > 0 and random.random() < 0.25:
                    special = special_words_left.pop(random.randint(0, len(special_words_left)-1))
                    special_words_spawned.append(special)
                    active_words.append({"id": 100 + len(special_words_spawned), "text": special, "x": random.randint(50, width - 150), "y": 50})
                elif word_index < len(words_to_type):
                    word = words_to_type[word_index]
                    word_index += 1
                    is_boss = (word == "coding destroys virus digital")
                    active_words.append({
                        "id": word_index,
                        "text": word,
                        "x": random.randint(50, width - 250 if is_boss else width - 150),
                        "y": 50,
                        "boss": is_boss
                    })
                    if is_boss:
                        sound_powerup.play()
                last_spawn = current_time

        for word in active_words[:]:
            speed = 2.0 if difficulty == "Hard" else 1.0
            if word.get("boss", False):
                word["y"] += speed * 0.8
            else:
                word["y"] += speed
            if word["y"] > height:
                if word.get("boss", False):
                    sound_lose.play()
                    pygame.mixer.music.stop()
                    show_end_screen("You Lose")
                    return
                else:
                    sound_hit.play()
                    if word["text"] not in special_words:
                        lives -= 1
                    active_words.remove(word)
                    typed_inputs.pop(word["id"], None)
                    if current_target_id == word["id"]:
                        current_target_id = None
                    if lives <= 0:
                        sound_lose.play()
                        pygame.mixer.music.stop()
                        show_end_screen("You Lose")
                        return
            
        missed_words = 30 - (score + len(active_words))
        if (score == 30 and missed_words == 0) or (score == 29 and missed_words == 1) or (score == 28 and missed_words == 2):
            sound_win.play()
            pygame.mixer.music.stop()
            show_end_screen("You Win")
            return
            
        if current_target_id is not None:
            word = next((w for w in active_words if w["id"] == current_target_id), None)
        else:
            word = active_words[0] if active_words else None

        if word:
            center_x = word["x"] + font.size(word["text"])[0] // 2
            if ship_x + 40 < center_x:
                ship_x += 4
            elif ship_x + 40 > center_x:
                ship_x -= 4
        screen.blit(ship_img, (ship_x, ship_y))

        for word in active_words:
            if word.get("boss", False):
                boss_img = pygame.transform.scale(virus_img, (180, 180))
                screen.blit(boss_img, (word["x"], word["y"] - 60))
            elif word["text"] in special_words:
                screen.blit(book_img, (word["x"] - 10, word["y"] - 10))
            else:
                screen.blit(virus_img, (word["x"], word["y"] - 20))
            typed = typed_inputs.get(word["id"], "")
            remaining = word["text"][len(typed):]
            word_surface = font.render(remaining, True, white)
            screen.blit(word_surface, (word["x"] + 10, word["y"] + 20))

        for exp in explosions[:]:
            screen.blit(explosion_img, (exp["x"], exp["y"]))
            exp["timer"] -= 1
            if exp["timer"] <= 0:
                explosions.remove(exp)

        draw_bullets()
        score_display = font.render(f"Score: {score}", True, white)
        screen.blit(score_display, (10, 10))
        difficulty_display = font.render(f"Difficulty: {difficulty}", True, white)
        screen.blit(difficulty_display, (10, 50))
        pause_rect = screen.blit(pause_img, (10, 90))
        draw_lives()
        draw_books()
        pygame.display.update()
        clock.tick(60)

# Main loop
while True:
    if menu:
        if not pygame.mixer.get_busy():
            sound_menu.play(-1)
        play_button_rect, story_button_rect = draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    sound_play.play()
                    menu = False
                    show_difficulty = True
                elif story_button_rect.collidepoint(event.pos):
                    sound_play.play()
                    show_story = True
                    menu = False
        pygame.display.update()
        pygame.time.Clock().tick(60)
    elif show_story:
        back_button_rect = draw_story_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    sound_play.play()
                    show_story = False
                    menu = True
        pygame.display.update()
        pygame.time.Clock().tick(60)
    elif show_difficulty:
        easy_rect, hard_rect, back_rect = draw_difficulty_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    sound_play.play()
                    show_difficulty = False
                    menu = True
                elif easy_rect.collidepoint(event.pos):
                    sound_menu.stop()
                    sound_play.play()
                    difficulty = "Easy"
                    show_difficulty = False
                    game_active = True
                elif hard_rect.collidepoint(event.pos):
                    sound_menu.stop()
                    sound_play.play()
                    difficulty = "Hard"
                    show_difficulty = False
                    game_active = True
        pygame.display.update()
        pygame.time.Clock().tick(60)
    elif game_active:
        run_game()
        game_active = False
        menu = True