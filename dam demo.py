import pygame
import json

pygame.init()

# Colors
COLORS = {
    'G': (255, 190, 190),   # Red
    'I': (190, 190, 255),   # Blue
    'B': (255, 255, 190),   # Yellow
    'A': (190, 255, 190)    # Green
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
HIGHLIGHT = (255, 158, 84)
BUTTON_COLOR = (190, 190, 190)
BACKGROUND = (52, 53, 65)  # Dark mode

# Manage Theme
theme = False

# Keep track of updates for optimization
frame = 0

# Adjustable scale
scale_factor = 0.48

# Font
font_name = 'Verdana'
font_size = int(20 * scale_factor)
font = pygame.font.SysFont(font_name, font_size)
edittext_font = pygame.font.SysFont(font_name, 26)

def get_text_width(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface.get_width()

def compute_column_widths(columns, font, starting_col_title, starting_col_values, padding=10):
    widths = []
    title_width = get_text_width(starting_col_title, font)
    max_value_width = max(get_text_width(value_data['value'], font) for value_data in starting_col_values)
    starting_col_width = max(title_width, max_value_width) + padding
    widths.append(starting_col_width)
    
    for col in columns:
        title_width = get_text_width(col['Title'], font)
        column_width = title_width + padding
        widths.append(column_width)
    
    return widths

FILE_NAME = 'example' # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
DATA_FILE = f'data_{FILE_NAME}.json'
with open(DATA_FILE, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

starting_col_title = data['StartingColumn']['Title']
starting_col_values = data['StartingColumn']['Values']
columns = data['Columns']

ROWS = len(starting_col_values)
COLS = len(columns) + 1

column_widths = compute_column_widths(columns, font, starting_col_title, starting_col_values)
CELL_WIDTHS = column_widths

def recalc_columns():
    global CELL_WIDTHS
    CELL_WIDTHS = compute_column_widths(columns, font, starting_col_title, starting_col_values)

CELL_HEIGHT = int(30 * scale_factor)

TABLE_WIDTH = sum(CELL_WIDTHS)
TABLE_HEIGHT = CELL_HEIGHT * (ROWS + 1)

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('DEMO - Dynamic Authorisation Matrix - Doove Care Groep')
clock = pygame.time.Clock()
fps = 5

scroll_x, scroll_y = 0, 0
scroll_speed = 50 # adjustable

def draw_table():
    global scroll_x, scroll_y

    tmp_color = WHITE if theme else BLACK
    start_col_text = font.render(starting_col_title, True, tmp_color)
    start_col_text_rect = start_col_text.get_rect(center=(scroll_x + CELL_WIDTHS[0] // 2, scroll_y + CELL_HEIGHT // 2))
    screen.blit(start_col_text, start_col_text_rect)

    for row_index in range(ROWS):
        value_data = starting_col_values[row_index] if row_index < len(starting_col_values) else {"value": "", "highlight": False}
        value = value_data['value']
        highlight = value_data['highlight']
        
        bg_color = HIGHLIGHT
        txt_color = WHITE if theme else BLACK
        if highlight:
            txt_color = BLACK
        elif not highlight:
            bg_color = BACKGROUND if theme else WHITE
        rect = pygame.Rect(scroll_x, scroll_y + (row_index + 1) * CELL_HEIGHT, CELL_WIDTHS[0], CELL_HEIGHT)
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, tmp_color, rect, 1)
        text = font.render(value, True, txt_color)
        text_rect = text.get_rect(center=(scroll_x + CELL_WIDTHS[0] // 2, scroll_y + (row_index + 1) * CELL_HEIGHT + CELL_HEIGHT // 2))
        screen.blit(text, text_rect)
    
    for col_index, col in enumerate(columns):
        title = col['Title']
        text = font.render(title, True, tmp_color)
        col_start_x = scroll_x + sum(CELL_WIDTHS[:col_index + 1]) + CELL_WIDTHS[col_index + 1] // 2
        text_rect = text.get_rect(center=(col_start_x, scroll_y + CELL_HEIGHT // 2))
        screen.blit(text, text_rect)

        highlight_count = 0
        for row_index in range(ROWS):
            rect = pygame.Rect(scroll_x + sum(CELL_WIDTHS[:col_index + 1]), scroll_y + (row_index + 1) * CELL_HEIGHT, CELL_WIDTHS[col_index + 1], CELL_HEIGHT)
            row_highlighted = starting_col_values[row_index]['highlight']
            
            if row_index < ROWS:
                if row_highlighted:
                    highlight_count += 1
                    value = ''
                    color = BACKGROUND if theme else HIGHLIGHT
                elif row_index - highlight_count >= len(col['Values']):
                    value = ''
                    color = WHITE
                else:
                    value = col['Values'][row_index - highlight_count]
                    color = COLORS.get(value, WHITE)
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, tmp_color, rect, 1)
                text = font.render(value, True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def draw_button(rect, text):
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def update_screen():
    global frame, scroll_x, scroll_y
    frame += 1
    tmp_color = BACKGROUND if theme else WHITE
    screen.fill(tmp_color)

    scroll_x = max(min(scroll_x, 0), -TABLE_WIDTH + screen_width)
    scroll_y = max(min(scroll_y, 0), -TABLE_HEIGHT + screen_height)

    draw_table()
    draw_button(btn1_rect, btn1_text)
    draw_button(btn2_rect, btn2_text)
    draw_button(btn3_rect, btn3_text)
    draw_button(btn4_rect, btn4_text)
    draw_button(btn5_rect, btn5_text)
    tmp_color = WHITE if theme else BLACK
    text_frame = font.render(f'Frame: {frame}', True, tmp_color)
    text_fps = font.render(f'FPS: {fps}', True, tmp_color)
    screen.blit(text_frame, (50, 980))
    screen.blit(text_fps, (50, 990))
    pygame.display.flip()
    clock.tick(fps)

def add_function(title, values):
    new_function = {
        "Title": title,
        "Values": values
    }
    data['Columns'].append(new_function)
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent='\t')
    
    recalc_columns()

def remove_function(title):
    global data, starting_col_values, columns, ROWS, COLS, CELL_WIDTHS, TABLE_WIDTH, TABLE_HEIGHT

    for i, column in enumerate(data['Columns']):
        if column['Title'] == title:
            del data['Columns'][i]
            print(f"Function '{title}' removed.")
            break
    else:
        print(f"Function '{title}' not found.")
        return  # Exit if the function wasn't found

    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent='\t')

    # Update in-memory data and recalculate dimensions
    starting_col_values = data['StartingColumn']['Values']
    columns = data['Columns']
    ROWS = len(starting_col_values)
    COLS = len(columns) + 1
    recalc_columns()

    # Immediately reflect changes on screen
    update_screen()

def draw_text(surface, text, position, color=BLACK):
    text_surface = edittext_font.render(text, True, color)
    surface.blit(text_surface, position)

def get_user_input(prompt, limit=20, all_caps=False, suggestions=False):
    user_input = ""
    input_active = True
    suggestion_list = []

    while input_active:
        screen.fill((0, 0, 0))
        draw_text(screen, prompt + user_input + ' (' + str(len(user_input)) + '/' + str(limit) + ')', (20, 200), WHITE)

        # Update suggestions if enabled
        if suggestions and user_input:
            suggestion_list = [col['Title'] for col in data['Columns'] if col['Title'].startswith(user_input)]
        
        # Draw suggestions
        for i, suggestion in enumerate(suggestion_list):
            index_of_suggestion = next((index for index, col in enumerate(data['Columns']) if col['Title'] == suggestion), -1)
            draw_text(screen, f"{suggestion} (#{index_of_suggestion})", (20, 250 + i * 30), WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_TAB and len(suggestion_list) > 0:
                    user_input = suggestion_list[0]
                else:
                    user_input += event.unicode
        if all_caps:
            user_input = user_input.upper()
    return user_input

def get_column_index_by_title(target_title):
    for index, column in enumerate(data['Columns']):
        if column['Title'] == target_title:
            return index
    return -1

def switch_columns(indexA, indexB):
    if indexA != -1 or indexB != -1:
        data['Columns'][indexA], data['Columns'][indexB] = data['Columns'][indexB], data['Columns'][indexA]
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent='\t')
            print("succes!")
            recalc_columns()
    else:
        print("-1 in switch: Function not found. No actions taken.")

def insert_column_after(column_index, insert_index):        
    if column_index == -1 or insert_index == -1:
        print("-1: no action taken.")
    else:
        insert_position = insert_index + 1

        if 0 <= column_index < len(columns):
            column_to_insert = columns[column_index]
            
            del columns[column_index]
            
            columns.insert(insert_position, column_to_insert)

        with open(DATA_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            print("succesfully inserted column!")
            recalc_columns()

# dont forget to add the buttons to update_screen()
btn1_rect = pygame.Rect(150, 980, 100, 30)
btn1_text = 'Add Function'
btn2_rect = pygame.Rect(250, 980, 100, 30)
btn2_text = 'Theme'
btn3_rect = pygame.Rect(350, 980, 100, 30)
btn3_text = 'Del Function'
btn4_rect = pygame.Rect(450, 980, 100, 30)
btn4_text = 'Switch'
btn5_rect = pygame.Rect(550, 980, 100, 30)
btn5_text = 'Insert After'

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if btn1_rect.collidepoint(mouse_pos):
                print("Adding Function")
                tmp_title = get_user_input("Enter the title of the new function: ")
                non_highlighted_count = sum(1 for item in data["StartingColumn"]["Values"] if not item["highlight"])
                tmp_values = get_user_input("Enter the values for " + str(tmp_title) + ": ", non_highlighted_count, True)
                add_function(tmp_title, tmp_values)

            elif btn2_rect.collidepoint(mouse_pos):
                print("Switching Theme")
                theme = not theme

            elif btn3_rect.collidepoint(mouse_pos):
                title_to_remove = get_user_input("Enter the title of the function you want to delete: ", suggestions=True)
                remove_function(title_to_remove)

            elif btn4_rect.collidepoint(mouse_pos):
                columnA = get_user_input("Enter the title of the first function you want to swap: ", suggestions=True)
                columnB = get_user_input("Enter the title of the second function you want to swap: ", suggestions=True)
                switch_columns(get_column_index_by_title(columnA), get_column_index_by_title(columnB))

            elif btn5_rect.collidepoint(mouse_pos):
                insert = get_user_input("Enter the title of the function you want to insert: ", suggestions=True)
                after = get_user_input("Enter the title of the function you want to insert after: ", suggestions=True)
                insert_column_after(get_column_index_by_title(insert), get_column_index_by_title(after))
    
    # Set fps higher when scrolling for smooth movement
    keys = pygame.key.get_pressed()
    isScrolling = keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
    fps = 60 if isScrolling else 5
    if isScrolling:
        if keys[pygame.K_UP]:
            scroll_y += scroll_speed
        if keys[pygame.K_DOWN]:
            scroll_y -= scroll_speed
        if keys[pygame.K_LEFT]:
            scroll_x += scroll_speed
        if keys[pygame.K_RIGHT]:
            scroll_x -= scroll_speed
        
    update_screen()

pygame.quit()