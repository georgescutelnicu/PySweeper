import tkinter as tk



class Difficulty:

    def __init__(self):
        """
        Initialize the difficulty selection window.
        """

        self.window = tk.Tk()
        self.window.geometry(f"+{self.window.winfo_screenwidth() // 4}+{self.window.winfo_screenheight() // 8}")
        self.window.title("Choose Difficulty")

        self.difficulty = None
        self.difficulty_level = tk.StringVar(value="none")

        self.easy_radio = tk.Radiobutton(self.window, text="Easy", variable=self.difficulty_level, value="easy", font=("Helvetica", 12), command=self.update_difficulty)
        self.medium_radio = tk.Radiobutton(self.window, text="Medium", variable=self.difficulty_level, value="medium", font=("Helvetica", 12), command=self.update_difficulty)
        self.hard_radio = tk.Radiobutton(self.window, text="Hard", variable=self.difficulty_level, value="hard", font=("Helvetica", 12), command=self.update_difficulty)

        self.easy_radio.grid(row=0, column=0, padx=10, pady=5)
        self.medium_radio.grid(row=0, column=1, padx=10, pady=5)
        self.hard_radio.grid(row=0, column=2, padx=10, pady=5)

        self.ok_button = tk.Button(self.window, text="OK", font=("Helvetica", 12), command=self.window.quit)
        self.ok_button.grid(row=1, column=0, columnspan=3, pady=20)


    def update_difficulty(self):
        """
        Update the selected difficulty based on the radio button choice.
        """

        self.difficulty = self.difficulty_level.get()


    def choose_difficulty(self):
        """
        Display the difficulty selection window and return the chosen difficulty.
        """

        self.window.mainloop()
        self.window.destroy()
        return self.difficulty