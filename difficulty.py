import tkinter as tk


class Difficulty(tk.Tk):

    def __init__(self):
        """
        Initialize the difficulty selection window.
        """
        super().__init__()

        self.geometry(f"+{self.winfo_screenwidth() // 4}+{self.winfo_screenheight() // 8}")
        self.title("Choose Difficulty")

        self.difficulty_level = tk.StringVar(value="easy")

        self.easy_radio = tk.Radiobutton(self, text="Easy", variable=self.difficulty_level, value="easy", font=("Helvetica", 12), command=self.update_difficulty)
        self.medium_radio = tk.Radiobutton(self, text="Medium", variable=self.difficulty_level, value="medium", font=("Helvetica", 12), command=self.update_difficulty)
        self.hard_radio = tk.Radiobutton(self, text="Hard", variable=self.difficulty_level, value="hard", font=("Helvetica", 12), command=self.update_difficulty)

        self.easy_radio.grid(row=0, column=0, padx=10, pady=5)
        self.medium_radio.grid(row=0, column=1, padx=10, pady=5)
        self.hard_radio.grid(row=0, column=2, padx=10, pady=5)

        self.ok_button = tk.Button(self, text="OK", font=("Helvetica", 12), command=self.quit)
        self.ok_button.grid(row=1, column=0, columnspan=3, pady=20)


    def update_difficulty(self):
        """
        Update the difficulty based on the radio button choice.
        """

        return self.difficulty_level.get()


    def choose_difficulty(self):
        """
        Display the difficulty selection window and return the chosen difficulty.
        """

        self.mainloop()
        self.destroy()
        return self.difficulty_level.get()