import tkinter as tk


class Settings(tk.Tk):

    def __init__(self):
        super().__init__()
        """
        Initialize the difficulty selection window.
        """

        self.geometry(f"+{self.winfo_screenwidth() // 4}+{self.winfo_screenheight() // 8}")
        self.title("Choose Difficulty")
        self.iconphoto(False, tk.PhotoImage(file="images/settings.png"))
        self.resizable(False, False)

        self.difficulty_level = tk.StringVar(value="easy")
        self.grid_size = tk.StringVar(value="10x10")

        self.easy_difficulty = tk.Radiobutton(self, text="Easy", variable=self.difficulty_level, value="easy",
                                              font=("Helvetica", 12), command=self.update_difficulty)
        self.medium_difficulty = tk.Radiobutton(self, text="Medium", variable=self.difficulty_level, value="medium",
                                                font=("Helvetica", 12), command=self.update_difficulty)
        self.hard_difficulty = tk.Radiobutton(self, text="Hard", variable=self.difficulty_level, value="hard",
                                              font=("Helvetica", 12), command=self.update_difficulty)

        self.grid_10x10 = tk.Radiobutton(self, text="10x10", variable=self.grid_size, value="10x10",
                                         font=("Helvetica", 12), command=self.update_grid_size)
        self.grid_16x16 = tk.Radiobutton(self, text="16x16", variable=self.grid_size, value="16x16",
                                         font=("Helvetica", 12), command=self.update_grid_size)
        self.grid_20x20 = tk.Radiobutton(self, text="20x20", variable=self.grid_size, value="16x30",
                                         font=("Helvetica", 12), command=self.update_grid_size)

        self.easy_difficulty.grid(row=0, column=0, padx=10, pady=5)
        self.medium_difficulty.grid(row=0, column=1, padx=10, pady=5)
        self.hard_difficulty.grid(row=0, column=2, padx=10, pady=5)

        self.grid_10x10.grid(row=1, column=0, padx=10, pady=5)
        self.grid_16x16.grid(row=1, column=1, padx=10, pady=5)
        self.grid_20x20.grid(row=1, column=2, padx=10, pady=5)

        self.ok_button = tk.Button(self, text="OK", font=("Helvetica", 12), command=self.quit)
        self.ok_button.grid(row=2, column=0, columnspan=3, pady=20)

    def update_difficulty(self):
        """
        Update the difficulty based on the radio button choice.
        """

        return self.difficulty_level.get()

    def update_grid_size(self):
        """
        Update the grid size based on the radio button choice.
        """

        return self.grid_size.get()

    def choose_difficulty_and_grid_size(self):
        """
        Display the difficulty and grid size selection window and return the chosen difficulty and grid size.
        """

        self.mainloop()
        self.destroy()
        return self.difficulty_level.get(), self.grid_size.get()
