import tkinter as tk
import random
import time
import os

# Directory for prompt files
PROMPT_DIR = "./prompts"  # Ensure this directory exists with appropriately named files

# Initialize variables
start_time = 0
prompt_text = ""
running = False
lines = []
current_line_index = 0
displayed_lines = 10  # Number of lines to display at once
char_counter = 0  # Track position in the prompt
stat_board = None  # Initialize stat board variable for later reference

# Load prompts from a file
def load_prompts(category, difficulty, length):
    # Replace spaces with hyphens
    difficulty = difficulty.replace(" ", "-")
    length = length.replace(" ", "-")
    category.lower()
    difficulty.lower()
    length.lower()

    filename = f"{category}_{difficulty}_{length}.txt"
    try:
        with open(os.path.join(PROMPT_DIR, filename), "r") as file:
            content = file.read()  # Read the entire file content
            prompts = content.split("[[END]]")  # Split by the chosen delimiter
            return [prompt.strip() for prompt in prompts if prompt.strip()]  # Ignore empty prompts
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []

# Start the typing test with a random prompt
def start_test():
    global start_time, prompt_text, running, lines, current_line_index, char_counter
    selected_category = category_var.get()
    selected_difficulty = difficulty_var.get()
    selected_length = length_var.get()

    prompts = load_prompts(selected_category, selected_difficulty, selected_length)
    if prompts:
        prompt_text = random.choice(prompts)
        lines = prompt_text.splitlines()
        current_line_index = 0
        char_counter = 0
        display_prompt()
        input_box.delete(1.0, tk.END)
        input_box.focus_set()
        start_time = time.time()
        running = True
        update_stats()  # Start real-time stats update
        start_button.config(text="Next Prompt")
    else:
        prompt_label.config(text="No prompts available for this combination.")

# Update the prompt display with the current character highlighted
def display_prompt():
    prompt_label.config(state="normal")
    prompt_label.delete("1.0", tk.END)

    # Calculate the start and end indices for the displayed lines
    start_index = max(0, current_line_index - 1)
    end_index = min(len(lines), start_index + displayed_lines)

    # Insert each line
    for i in range(start_index, end_index):
        line = lines[i]
        prompt_label.insert(tk.END, line + "\n")

    # Highlight based on character counter
    if char_counter < len(prompt_text):
        start_pos = f"1.0 + {char_counter} chars"
        end_pos = f"1.0 + {char_counter + 1} chars"
        prompt_label.tag_add("highlight", start_pos, end_pos)

    prompt_label.tag_configure("highlight", foreground="red")
    prompt_label.config(state="disabled")

# End the test, calculate stats, and display the stat board
def end_test(event=None):
    global start_time, running
    running = False
    end_time = time.time()
    time_taken = end_time - start_time

    # Get user input and calculate results
    user_input = input_box.get("1.0", tk.END).strip()
    wpm = (len(prompt_text.split()) / time_taken) * 60
    correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(prompt_text) and char == prompt_text[i])
    accuracy = (correct_chars / len(prompt_text)) * 100

    # Hide input box and show stat board
    input_box.pack_forget()
    display_stat_board(time_taken, wpm, accuracy)

# Display the stat board with results
def display_stat_board(time_taken, wpm, accuracy):
    global stat_board
    stat_board = tk.Frame(root)
    stat_board.pack(pady=20)

    # Add a title label for the stat board
    title_label = tk.Label(stat_board, text="Typing Test Results", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 20))

    # Display the time taken
    time_label = tk.Label(stat_board, text=f"Time Taken: {time_taken:.2f} seconds", font=("Helvetica", 14))
    time_label.pack(pady=5)

    # Display the WPM
    wpm_label = tk.Label(stat_board, text=f"Words Per Minute (WPM): {wpm:.2f}", font=("Helvetica", 14))
    wpm_label.pack(pady=5)

    # Display the accuracy
    accuracy_label = tk.Label(stat_board, text=f"Accuracy: {accuracy:.2f}%", font=("Helvetica", 14))
    accuracy_label.pack(pady=5)

    # Add a restart button
    restart_button = tk.Button(stat_board, text="Next Prompt", font=("Helvetica", 14), command=reset_test)
    restart_button.pack(pady=20)

# Reset the test to initial state
def reset_test():
    global running, char_counter, stat_board
    running = False
    char_counter = 0

    # Remove the stat board
    if stat_board:
        stat_board.pack_forget()
        stat_board.destroy()
        stat_board = None

    # Clear prompt and result labels, show input box again
    prompt_label.config(state="normal")
    prompt_label.delete("1.0", tk.END)
    prompt_label.config(state="disabled")
    result_label.config(text="")

    # Re-pack the input box and clear any previous input
    input_box.pack()
    input_box.delete(1.0, tk.END)
    input_box.focus_set()
    start_test()

# Check user input to update the current character highlight
def check_current_position(event):
    global char_counter
    if not running:
        return  # Stop checking input if test is not running

    user_input = input_box.get("1.0", tk.END).strip()

    # Adjust character counter based on keystrokes
    if event.keysym == "BackSpace" and char_counter > 0:
        char_counter -= 1
    elif event.keysym not in ["BackSpace", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"]:
        char_counter += 1

    display_prompt()

    # End test if char_counter reaches end of prompt
    if char_counter >= len(prompt_text):
        end_test()

# Calculate WPM and accuracy in real-time
def calculate_stats():
    current_time = time.time()
    time_elapsed = max(current_time - start_time, 1)
    user_input = input_box.get("1.0", tk.END).strip()

    correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(prompt_text) and char == prompt_text[i])
    wpm = (correct_chars / 5) / (time_elapsed / 60)

    if user_input:
        accuracy = (correct_chars / len(user_input)) * 100
    else:
        accuracy = 100

    return wpm, accuracy

# Update the real-time stats and schedule the next update
def update_stats():
    if running:
        wpm, accuracy = calculate_stats()
        result_label.config(text=f"Real-Time WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")
        root.after(1000, update_stats)

# GUI setup
root = tk.Tk()
root.title("Typing Practice App")
root.geometry("600x500")

# Category selection
category_var = tk.StringVar(value="Select Category")
categories = ["Programmer", "Literature", "Motivational", "Math", "Science"]
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.config(font=("Helvetica", 12))
category_menu.pack(side=tk.LEFT, padx=5, pady=10)

# Difficulty selection
difficulty_var = tk.StringVar(value="medium")
difficulties = ["Easy", "Medium", "Hard", "Very Hard"]
difficulty_menu = tk.OptionMenu(root, difficulty_var, *difficulties)
difficulty_menu.config(font=("Helvetica", 12))
difficulty_menu.pack(side=tk.LEFT, padx=5, pady=10)

# Length selection
length_var = tk.StringVar(value="medium")
lengths = ["Short", "Medium", "Long", "Very Long"]
length_menu = tk.OptionMenu(root, length_var, *lengths)
length_menu.config(font=("Helvetica", 12))
length_menu.pack(side=tk.LEFT, padx=5, pady=10)

# Prompt Label
prompt_label = tk.Text(root, font=("Helvetica", 16), wrap="word", height=10, width=50)
prompt_label.config(state="disabled", background=root.cget("background"))
prompt_label.pack(pady=20)

# Input Text Box
input_box = tk.Text(root, height=2, width=50, font=("Helvetica", 14))
input_box.pack()
input_box.bind("<KeyRelease>", check_current_position)

# Start Button
start_button = tk.Button(root, text="Start Typing Test", command=start_test, font=("Helvetica", 14))
start_button.pack(pady=10)

# Real-Time Stats Label
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=10)

root.mainloop()
