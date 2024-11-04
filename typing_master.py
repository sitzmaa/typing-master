import tkinter as tk
import random
import time
import os

# Directory for prompt files
PROMPT_DIR = "./prompts"  # Ensure this directory exists with text files inside

# Initialize variables
start_time = 0
prompt_text = ""
running = False

# Load prompts from a file
def load_prompts(filename):
    try:
        with open(os.path.join(PROMPT_DIR, filename), "r") as file:
            content = file.read()
            # Split content into multi-line prompts based on double newlines
            return [prompt.strip() for prompt in content.strip().split('\n\n') if prompt.strip()]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []

# Start the typing test with a random prompt from the selected category
def start_test():
    global start_time, prompt_text, running
    selected_category = category_var.get()
    prompts = load_prompts(f"{selected_category}.txt")
    if prompts:
        prompt_text = random.choice(prompts)
        prompt_label.config(text=prompt_text)
        input_box.delete(1.0, tk.END)  # Clear previous input
        input_box.focus_set()          # Focus on the input box for typing
        start_time = time.time()
        running = True
        update_stats()  # Start real-time stats update
    else:
        prompt_label.config(text="No prompts available for this category.")

# End the test, calculate WPM and accuracy, and show final results
def end_test(event):
    global start_time, running
    running = False
    end_time = time.time()
    time_taken = end_time - start_time

    # Get user input and calculate results
    user_input = input_box.get("1.0", tk.END).strip()
    wpm = (len(prompt_text.split()) / time_taken) * 60
    correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(prompt_text) and char == prompt_text[i])
    accuracy = (correct_chars / len(prompt_text)) * 100

    # Display final results
    result_label.config(text=f"Time: {time_taken:.2f} sec | WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

# Calculate WPM and accuracy in real-time
def calculate_stats():
    current_time = time.time()
    time_elapsed = max(current_time - start_time, 1)  # Avoid division by zero
    user_input = input_box.get("1.0", tk.END).strip()

    # Calculate WPM
    correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(prompt_text) and char == prompt_text[i])
    wpm = (correct_chars / 5) / (time_elapsed / 60)

    # Calculate Accuracy
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
        root.after(1000, update_stats)  # Update every second

# GUI setup
root = tk.Tk()
root.title("Typing Practice App")
root.geometry("600x450")

# Category selection
category_var = tk.StringVar(value="Select Category")
categories = ["programmer_prompts", "literature_prompts", "motivational_prompts"]  # Add other file names here
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.config(font=("Helvetica", 14))
category_menu.pack(pady=10)

# Prompt Label
prompt_label = tk.Label(root, text="", font=("Helvetica", 16), wraplength=500, justify="center")
prompt_label.pack(pady=20)

# Input Text Box
input_box = tk.Text(root, height=10, width=50, font=("Helvetica", 14))
input_box.pack()
input_box.bind("<Return>", end_test)  # Bind Enter key to end_test

# Start Button
start_button = tk.Button(root, text="Start Typing Test", command=start_test, font=("Helvetica", 14))
start_button.pack(pady=20)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=20)

root.mainloop()
