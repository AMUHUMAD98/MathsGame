import pygame
import random
import sys
from pygame.locals import *

# Start Pygame
pygame.init()

# Define constants
WIDTH = 800
HEIGHT = 600
FONT_SIZE = 50
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Load background image and sound
background = pygame.image.load("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/background.png")
background_sound = pygame.mixer.Sound("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/backgroundsound.mp3")

# Avatars
avatar1 = pygame.image.load("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/avatar1.png")
avatar2 = pygame.image.load("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/avatar2.png")

# Reward Badges
gold_badge = pygame.image.load("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/Gold.png")
silver_badge = pygame.image.load("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/Silver.png")
bronze_badge = pygame.image.load("/Users/amranmuhumad/Desktop/Msc Maths Game CODE/Bronze.png")

# Desired size for the badge images
badge_width = 200
badge_height = 200

# Scale the badge images
gold_badge = pygame.transform.scale(gold_badge, (badge_width, badge_height))
silver_badge = pygame.transform.scale(silver_badge, (badge_width, badge_height))
bronze_badge = pygame.transform.scale(bronze_badge, (badge_width, badge_height))

pygame.mixer.Sound.play(background_sound, loops=-1)  # Play the sound on repeat

# Game variables
score = 0
questions = 0
game_over = False
# Timer set to 10 minutes (600 seconds)
timer = 600
start_ticks = pygame.time.get_ticks()
feedback = ""
difficulty_levels = {"easy": (1, 5), "medium": (1, 10), "hard": (1, 20)}
difficulty = "easy"

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Game")

# Text configuration
font = pygame.font.SysFont('freesansbold.ttf', FONT_SIZE, bold=True)

# Placeholder for the correct answer
answer_placeholder = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 4 + FONT_SIZE, 200, 100)
pygame.draw.rect(screen, WHITE, answer_placeholder, 0)  # Draw answer placeholder

INSTRUCTION_FONT_SIZE = 30

# Set up the font for instructions
instruction_font = pygame.font.SysFont('freesansbold.ttf', INSTRUCTION_FONT_SIZE)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 45
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maths Game')

# Load font
font = pygame.font.SysFont('freesansbold.ttf', FONT_SIZE, bold=True)

class DraggableChoice(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        super().__init__()
        self.text = text
        self.image = font.render(str(self.text), True, BLUE)  # Changed text color to BLUE to contrast with the white box
        self.rect = self.image.get_rect(center=pos)
        self.selected = False

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.selected = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected = False
            if self.rect.colliderect(answer_placeholder):
                return self.text
        elif event.type == pygame.MOUSEMOTION:
            if self.selected:
                self.rect.move_ip(event.rel)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, 0)  # Draw a white box
        surface.blit(self.image, self.rect)  # Then draw the text over it

def generate_problem(difficulty):
    lower, upper = difficulty_levels[difficulty]
    num1 = random.randint(lower, upper)
    num2 = random.randint(lower, upper)
    operator = random.choice(["+", "-", "/", "*"])  # Added multiplication operator

    if operator == "+":
        answer = num1 + num2
    elif operator == "-":
        answer = num1 - num2
    elif operator == "/":  # Ensure division gives a whole number
        num1, num2 = num2, num1 * num2
        answer = num2 / num1
    elif operator == "*":  # Added multiplication case
        answer = num1 * num2

    choices = [answer] + random.sample(range(lower * 2, upper * 2 + 1), 3)
    random.shuffle(choices)

    return num1, num2, answer, operator, choices

# New function to render a simple button
def render_button(surface, text, position, color, font):
    text_render = font.render(text, True, WHITE)
    width, height = text_render.get_size()
    button_rect = pygame.Rect(position[0] - width // 2, position[1] - height // 2, width, height)
    pygame.draw.rect(surface, color, button_rect)
    surface.blit(text_render, (position[0] - width // 2, position[1] - height // 2))
    return button_rect

# New function to display the initial menu and get the user's choice
def get_user_type():
    while True:
        screen.blit(background, (0, 0))
        prompt = font.render("Who is playing?", True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 4))

        kid_button = render_button(screen, "Kid", (WIDTH // 2, HEIGHT // 2), BLUE, font)
        parent_and_kid_button = render_button(screen, "Parent and Kid", (WIDTH // 2, HEIGHT * 3 // 4), BLUE, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kid_button.collidepoint(event.pos):
                    return "Kid"
                if parent_and_kid_button.collidepoint(event.pos):
                    return "Parent and Kid"

user_type = get_user_type()
# Depending on the user_type, you can now modify the game behavior if needed.
      
# locations for each draggable choice
locations = [(WIDTH // 4, HEIGHT // 2), (WIDTH * 3 // 4, HEIGHT // 2), (WIDTH // 4, HEIGHT // 1.5), (WIDTH * 3 // 4, HEIGHT // 1.5)]

def render_problem(problem):
    num1, num2, _, operator, _ = problem
    question = font.render(f"What is {num1} {operator} {num2}?", True, WHITE)
    screen.blit(question, (WIDTH // 2 - question.get_width() // 2, HEIGHT // 4))

def render_input(input_text):
    text = font.render(input_text, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

def render_feedback(feedback):
    text = font.render(feedback, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + FONT_SIZE))

def render_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def render_questions(questions):
    question_text = font.render(f"Questions: {questions+1}/10", True, WHITE)
    screen.blit(question_text, (WIDTH - 10 - question_text.get_width(), 10))

def render_timer(seconds):
    mins, secs = divmod(seconds, 60)
    timer_format = "{:02d}:{:02d}".format(mins, secs)
    timer_text = font.render(f"Time: {timer_format}", True, WHITE)
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 10))

def render_difficulty_selection():
    easy_text = font.render(f"Press 1 for Easy", True, WHITE)
    medium_text = font.render(f"Press 2 for Medium", True, WHITE)
    hard_text = font.render(f"Press 3 for Hard", True, WHITE)
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 4))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT * 3 // 4))

def check_badge(score):
    if score >= 10:
        return gold_badge
    elif score >= 7:
        return silver_badge
    elif score >= 4:
        return bronze_badge
    else:
        return None

def render_badge(badge):
    badge_text = font.render(f"Badge: {badge}", True, GREEN)
    screen.blit(badge_text, (WIDTH // 2 - badge_text.get_width() // 2, HEIGHT // 1.5))

def render_avatar_selection():
    screen.blit(avatar1, (WIDTH // 4 - avatar1.get_width() // 2, HEIGHT // 2 - avatar1.get_height() // 2))
    screen.blit(avatar2, (WIDTH * 3 // 4 - avatar2.get_width() // 2, HEIGHT // 2 - avatar2.get_height() // 2))
    prompt = font.render("Press 1 for Avatar 1, Press 2 for Avatar 2", True, WHITE)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT * 3 // 4))

def render_instructions():
    instructions = [
        "Instructions:",
        "1. Choose an avatar.", 
        "2.Drag and drop the correct answer into the white box.",
        "3. If you answer correctly, you earn a point.",
        "4. If you answer incorrectly, no points are awarded.",
        "5. The game is timed, so answer as quickly as you can.",
        "6. After 10 questions, the game ends.",
        "7. At the end of the game, you will earn a badge based on your score.",
        "8. Rate the game 1-5.",
        "9. Answer the game survey.",
        "10. Press any key to continue."
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 + i * INSTRUCTION_FONT_SIZE))

# Display instructions
showing_instructions = True
while showing_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            showing_instructions = False
            game_over = True
        elif event.type == pygame.KEYDOWN:
            showing_instructions = False
    screen.blit(background, (0, 0))  # Add background image
    render_instructions()
    pygame.display.flip()

# Avatar Choice
selecting_avatar = True
while selecting_avatar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            selecting_avatar = False
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                avatar = avatar1
                selecting_avatar = False
            elif event.key == pygame.K_2:
                avatar = avatar2
                selecting_avatar = False
    screen.blit(background, (0, 0))  # Add background image
    render_avatar_selection()
    pygame.display.flip()

# produce the first problem
problem = generate_problem(difficulty)
draggable_choices = [DraggableChoice(choice, loc) for choice, loc in zip(problem[4], locations)]

# Difficulty choice
selecting_difficulty = True
while selecting_difficulty:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            selecting_difficulty = False
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                difficulty = "easy"
                selecting_difficulty = False
            elif event.key == pygame.K_2:
                difficulty = "medium"
                selecting_difficulty = False
            elif event.key == pygame.K_3:
                difficulty = "hard"
                selecting_difficulty = False
    screen.blit(background, (0, 0))  # Add background image
    render_difficulty_selection()
    pygame.display.flip()
    
# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            for choice in draggable_choices:
                chosen = choice.update(event)
                if chosen is not None:
                    if chosen == problem[2]:
                        score += 1
                        feedback = "Good job! That's correct."
                    else:
                        feedback = f"Wrong! The correct answer was {problem[2]}"
                    questions += 1
                    if questions == 10:
                        if score == 10:
                            score += 5  # Bonus for perfect score
                        game_over = True
                    else:
                        # Generate a new problem only when a choice is dropped into the answer box
                        problem = generate_problem(difficulty)
                        draggable_choices = [DraggableChoice(choice, loc) for choice, loc in zip(problem[4], locations)]

    # Calculate the time since the game started
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    remaining_time = timer - seconds_passed

    # When time's up, end the game
    if remaining_time <= 0:
        game_over = True
        remaining_time = 0

    # Clear the screen and add background
    screen.blit(background, (0, 0))

    # Render the problem, input, score, questions, and timer
    render_problem(problem)
    for choice in draggable_choices:
        choice.draw(screen)
    pygame.draw.rect(screen, WHITE, answer_placeholder, 2)  # Draw answer placeholder
    render_score(score)
    render_questions(questions)
    render_timer(int(remaining_time))
    render_feedback(feedback)

    # Update the display
    pygame.display.flip()

# After game is over, display avatar, badge
badge = check_badge(score)
screen.blit(background, (0, 0))  # Add background image
screen.blit(avatar, (WIDTH // 2 - avatar.get_width() // 2, HEIGHT // 4 - avatar.get_height() // 2))
render_score(score)

# Draw badge
if badge is not None:
    screen.blit(badge, (WIDTH // 2 - badge.get_width() // 2, HEIGHT // 1.5 - badge.get_height() // 2))
    if badge == gold_badge:
        render_feedback("Congratulations! You've earned a Gold badge!")
    elif badge == silver_badge:
        render_feedback("Well done! You've earned a Silver badge!")
    else:
        render_feedback("Good effort! You've earned a Bronze badge!")
else:
    render_feedback("No badges earned this time. Keep practicing!")

pygame.display.flip()

pygame.time.wait(5000)

 # Ask the player to rate the game
rating = None
while rating is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:  # Handles keys 1-9
                    rating = event.key - pygame.K_0
                elif event.key == pygame.K_0:  # Handles key 0 separately, as it doesn't fit into the previous range
                    rating = 10
        screen.blit(background, (0, 0))  # Add background image
        rating_prompt = font.render("Rate the game (1-5, 1 being bad, 5 being great)", True, WHITE)
        screen.blit(rating_prompt, (WIDTH // 2 - rating_prompt.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

    # Display the rating
screen.blit(background, (0, 0))  # Add background image
rating_message = font.render(f"Thank you! You rated the game a {rating}.", True, WHITE)
screen.blit(rating_message, (WIDTH // 2 - rating_message.get_width() // 2, HEIGHT // 2))

pygame.display.flip()

pygame.time.wait(5000)

# Survey questions and options
questions = [
    {
        "question": "Did you enjoy the Maths Game?",
        "options": ["Yes", "No"]
    },
    {
        "question": "Was the game too easy or too hard?",
        "options": ["Too easy", "Just right", "Too hard"]
    },
    {
        "question": "Would you play this game again?",
        "options": ["Yes", "No"]
    },
    {
        "question": "Do you feel the game helped improve your math skills?",
        "options": ["Yes", "No", "Not sure"]
    },
    {
        "question": "Would you recommend this game to a friend?",
        "options": ["Yes", "No"]
    }
]

# Current question index
current_question_index = 0

# User's answers
answers = []

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Display question
    question_text = font.render(questions[current_question_index]["question"], True, BLACK)
    question_rect = question_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
    screen.blit(question_text, question_rect)

    # Display options and handle input
    for index, option in enumerate(questions[current_question_index]["options"]):
        option_text = font.render(option, True, BLACK)
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + index * 50))
        screen.blit(option_text, option_rect)

        if option_rect.collidepoint(pygame.mouse.get_pos()):
            option_text = font.render(option, True, BLACK, WHITE)
            screen.blit(option_text, option_rect)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    answers.append(option)
                    current_question_index += 1
                    if current_question_index == len(questions):
                        running = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pygame.display.flip()

pygame.quit()

print("User's answers:", answers)

pygame.quit()
sys.exit()