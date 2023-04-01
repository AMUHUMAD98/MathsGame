import random
import time

# define the main function
def main():
    print("Welcome to the Math Game!")
    print("Choose a level of difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    # get the user's choice of difficulty level
    level = int(input("Enter your choice: "))
    
    # set the range of numbers for each level
    if level == 1:
        num_range = range(1, 11)
    elif level == 2:
        num_range = range(1, 21)
    else:
        num_range = range(1, 51)
        
    # set the number of questions to ask and the time limit in seconds
    num_questions = 10
    time_limit = 600
    
    # initialize the score and start the timer
    score = 0
    start_time = time.time()
    
    # ask the questions
    for i in range(num_questions):
        # randomly choose the type of question
        operation = random.choice(["+", "-", "*", "/"])
        
        # randomly choose two numbers within the given range
        num1 = random.choice(num_range)
        num2 = random.choice(num_range)
        
        # ask the question and get the user's answer
        question = f"What is {num1} {operation} {num2}? "
        answer = int(input(question))
        
        # check the answer and update the score
        if operation == "+":
            correct_answer = num1 + num2
        elif operation == "-":
            correct_answer = num1 - num2
        elif operation == "*":
            correct_answer = num1 * num2
        else:
            correct_answer = num1 / num2
            
        if answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer is {correct_answer}.")
            
    # calculate the final score and time elapsed
    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    final_score = score / num_questions * 100
    
    # print the final score and time elapsed
    print(f"Time elapsed: {elapsed_time} seconds")
    print(f"Your score is: {final_score:.0f}%")
    
# call the main function
main()
