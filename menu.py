from pygame import *
from assets.animations.magic_book.magic_b_an import create_info_book


def show_menu(screen, WIDTH, HEIGHT, clock, font_win, font_main):
    """Відображає головне меню гри."""
    menu_running = True 
    selected = 0  # 0 - Грати, 1 - Вийти
    
    #----------------ШРИФТИ------------------ #
    font_win = font.Font("assets/fonts/Daydream_DEMO.otf", 72)
    font_main = font.Font("assets/fonts/megaman_2.ttf", 36)

    anim = create_info_book(WIDTH, loop=True, frame_duration=150, scale=(80, 80), x=10, y=0)

    if anim.frames:
        anim.y = HEIGHT - anim.frames[0].get_height() - 10

    while menu_running:
        dt = clock.tick(60)

        for e in event.get():
            if e.type == QUIT:
                return False
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    selected = (selected - 1) % 2 
                elif e.key == K_DOWN:
                    selected = (selected + 1) % 2 
                elif e.key == K_RETURN:
                    if selected == 0:
                        return True
                    else:
                        return False
                elif e.key == K_ESCAPE:
                    return False
        
        # Draw a menu
        screen.fill((30, 30, 30))

        # Create a title 
        title = font_win.render("PING PONG", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        anim.update(dt)
        anim.draw(screen)

        # Create menu options
        play_color = (255, 255, 255) if selected == 0 else (100, 100, 100)
        exit_color = (255, 255, 255) if selected == 1 else (100, 100, 100)

        play_text = font_main.render("PLAY", True, play_color)
        exit_text = font_main.render("EXIT", True, exit_color)

        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 300))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 400))

        # Перевіряємо наведення на анімацію
        mouse_pos = mouse.get_pos()
        anim_rect = Rect(anim.x, anim.y, anim.frames[0].get_width(), anim.frames[0].get_height())
        
        if anim_rect.collidepoint(mouse_pos):
            small_font = font.Font("assets/fonts/megaman_2.ttf", 12)
            tooltip_text = small_font.render("  Use the arrow keys to move around, ENTER to select", True, ("#312F2F"))
            screen.blit(tooltip_text, (anim.x + anim.frames[0].get_width() + 20, anim.y + 40))

        display.update()