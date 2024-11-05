import tkinter as tk
import random
import time
import os

PROMPT_DIR = "./prompts"  # Ensure this directory exists with appropriately named files

class PromptManager:
    def __init__(self, prompt_dir):
        self.prompt_dir = prompt_dir
    
    def load_prompts(self, category, difficulty, length):
        difficulty = difficulty.replace(" ", "-").lower()
        length = length.replace(" ", "-").lower()
        category = category.lower()

        filename = f"{category}_{difficulty}_{length}.txt"
        try:
            with open(os.path.join(self.prompt_dir, filename), "r") as file:
                content = file.read()
                prompts = content.split("[[END]]")
                return [prompt.strip() for prompt in prompts if prompt.strip()]
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return []

class StatBoard:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.title_label = tk.Label(self.frame, text="Typing Test Results", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=(0, 20))
        self.time_label = tk.Label(self.frame, font=("Helvetica", 14))
        self.time_label.pack(pady=5)
        self.wpm_label = tk.Label(self.frame, font=("Helvetica", 14))
        self.wpm_label.pack(pady=5)
        self.accuracy_label = tk.Label(self.frame, font=("Helvetica", 14))
        self.accuracy_label.pack(pady=5)
        self.restart_button = tk.Button(self.frame, text="Next Prompt", font=("Helvetica", 14), command=self.frame.pack_forget)
        self.restart_button.pack(pady=20)

    def display(self, time_taken, wpm, accuracy):
        self.time_label.config(text=f"Time Taken: {time_taken:.2f} seconds")
        self.wpm_label.config(text=f"Words Per Minute (WPM): {wpm:.2f}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")
        self.frame.pack(pady=20)
    
    def hide(self):
        self.frame.pack_forget()

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Practice App")
        self.root.geometry("600x500")
        self.start_time = 0
        self.prompt_text = ""
        self.running = False
        self.lines = []
        self.current_line_index = 0
        self.displayed_lines = 10
        self.char_counter = 0
        self.prompt_manager = PromptManager(PROMPT_DIR)
        self.stat_board = StatBoard(root)
        self.setup_ui()
    
    def setup_ui(self):
        self.category_var = tk.StringVar(value="Select Category")
        categories = ["Programmer", "Literature", "Motivational", "Math", "Science"]
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *categories)
        self.category_menu.config(font=("Helvetica", 12))
        self.category_menu.pack(side=tk.TOP, padx=5, pady=10)

        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = ["Easy", "Medium", "Hard", "Very Hard"]
        self.difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, *difficulties)
        self.difficulty_menu.config(font=("Helvetica", 12))
        self.difficulty_menu.pack(side=tk.TOP, padx=5, pady=10)

        self.length_var = tk.StringVar(value="medium")
        lengths = ["Short", "Medium", "Long", "Very Long"]
        self.length_menu = tk.OptionMenu(self.root, self.length_var, *lengths)
        self.length_menu.config(font=("Helvetica", 12))
        self.length_menu.pack(side=tk.TOP, padx=5, pady=10)

        self.prompt_label = tk.Text(self.root, font=("Helvetica", 16), wrap="word", height=10, width=50)
        self.prompt_label.config(state="disabled", background=self.root.cget("background"))
        self.prompt_label.pack(pady=20)

        self.input_box = tk.Text(self.root, height=2, width=50, font=("Helvetica", 14))
        self.input_box.pack()
        self.input_box.bind("<KeyRelease>", self.check_current_position)

        self.start_button = tk.Button(self.root, text="Start Typing Test", command=self.start_test, font=("Helvetica", 14))
        self.start_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)
    
    def start_test(self):
        self.start_time = time.time()
        selected_category = self.category_var.get()
        selected_difficulty = self.difficulty_var.get()
        selected_length = self.length_var.get()
        prompts = self.prompt_manager.load_prompts(selected_category, selected_difficulty, selected_length)

        if prompts:
            self.prompt_text = random.choice(prompts)
            self.lines = self.prompt_text.splitlines()
            self.current_line_index = 0
            self.char_counter = 0
            self.display_prompt()
            self.input_box.delete(1.0, tk.END)
            self.input_box.focus_set()
            self.running = True
            self.update_stats()
            self.start_button.config(text="Next Prompt")
        else:
            self.prompt_label.config(text="No prompts available for this combination.")
    
    def display_prompt(self):
        self.prompt_label.config(state="normal")
        self.prompt_label.delete("1.0", tk.END)

        start_index = max(0, self.current_line_index - 1)
        end_index = min(len(self.lines), start_index + self.displayed_lines)

        for i in range(start_index, end_index):
            line = self.lines[i]
            self.prompt_label.insert(tk.END, line + "\n")

        if self.char_counter < len(self.prompt_text):
            start_pos = f"1.0 + {self.char_counter} chars"
            end_pos = f"1.0 + {self.char_counter + 1} chars"
            self.prompt_label.tag_add("highlight", start_pos, end_pos)
        
        self.prompt_label.tag_configure("highlight", foreground="red")
        self.prompt_label.config(state="disabled")
    
    def end_test(self, event=None):
        self.running = False
        end_time = time.time()
        time_taken = end_time - self.start_time

        user_input = self.input_box.get("1.0", tk.END).strip()
        wpm = (len(self.prompt_text.split()) / time_taken) * 60
        correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(self.prompt_text) and char == self.prompt_text[i])
        accuracy = (correct_chars / len(self.prompt_text)) * 100

        self.input_box.pack_forget()
        self.stat_board.display(time_taken, wpm, accuracy)
    
    def reset_test(self):
        self.running = False
        self.char_counter = 0
        self.stat_board.hide()
        self.prompt_label.config(state="normal")
        self.prompt_label.delete("1.0", tk.END)
        self.prompt_label.config(state="disabled")
        self.result_label.config(text="")
        self.input_box.pack()
        self.input_box.delete(1.0, tk.END)
        self.input_box.focus_set()
        self.start_test()
    
    def check_current_position(self, event):
        if not self.running:
            return

        user_input = self.input_box.get("1.0", tk.END).strip()

        if event.keysym == "BackSpace" and self.char_counter > 0:
            self.char_counter -= 1
        elif event.keysym not in ["BackSpace", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"]:
            self.char_counter += 1

        self.display_prompt()

        if self.char_counter >= len(self.prompt_text):
            self.end_test()
    
    def calculate_stats(self):
        current_time = time.time()
        time_elapsed = max(current_time - self.start_time, 1)
        user_input = self.input_box.get("1.0", tk.END).strip()

        correct_chars = sum(1 for i, char in enumerate(user_input) if i < len(self.prompt_text) and char == self.prompt_text[i])
        wpm = (correct_chars / 5) / (time_elapsed / 60)

        if user_input:
            accuracy = (correct_chars / len(user_input)) * 100
        else:
            accuracy = 100

        return wpm, accuracy

    def update_stats(self):
        if self.running:
            wpm, accuracy = self.calculate_stats()
            self.result_label.config(text=f"Real-Time WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")
            self.root.after(1000, self.update_stats)

root = tk.Tk()
app = TypingTestApp(root)
root.mainloop()
