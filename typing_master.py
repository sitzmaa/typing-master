import tkinter as tk
import random
import time

# List of typing prompts
prompts = [
        "The quick brown fox jumped over the lazy dog",
        "A journey of a thousand miles begins with a single step",
        "To be or not to be, that is the question",
        "All that glitters is not gold",
        "Practice makes perfect"
]

# Initialize variables
start_time = 0
prompt_text = ""

def start_test():
    global start_time, prompt_text
    # Set the prompt and start time
    prompt_text = random.choice(prompts)
    prompt_label.config(text=prompt_text)
    input_box.delete(1.0, tk.END) # Clear previous input
    input_box.focus_set()         # Focus on the input box for typing
    start_time = time.time()

def end_test(event):
    global start_time
    end_time = time.time()
    time_taken = end_time - start_time

    # Get user input and calculate results
    user_input = input_box.get("1.0", tk.END).strip()
    wpm = (len(prompt_text.split()) / time_taken) * 60
    correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(prompt_text) and char == prompt_text[i])
    accuracy = (correct_chars / len(prompt_text)) * 100

    # Display results
    result_label.config(text=f"Time: {time_taken:.2f} sec | WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

root = tk.Tk()
root.title("Typing Practice App")
root.geometry("600x400")

# Prompt Label
prompt_label = tk.Label(root, text="", font=("Helvetica", 16), wraplength=500, justify="center")
prompt_label.pack(pady=20)

# Input Text Box
input_box = tk.Text(root, height=5, width=50, font=("Helvetica",14))
input_box.pack()
input_box.bind("<Return>", end_test) # Bind enter key to end_test

# Start Button
start_button =tk.Button(root, text="Start Typing Test", command=start_test, font=("Helvetica", 14))
start_button.pack(pady=20)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=20)

root.mainloop()


