import tkinter as tk
import random

MAX_ADVENTURE_LEVELS = 100
COLORS = ["#2ecc71", "#3498db", "#e67e22", "#9b59b6"]


class BlockBeam:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Beam")

        self.mode = "adventure"
        self.current_level = 1

        self.grid_size = 6
        self.max_moves = 10
        self.moves_used = 0
        self.grid_data = []

        self.cells = []

        self.build_ui()
        self.setup_level()

    # ---------------- UI ----------------
    def build_ui(self):
        self.root.configure(bg="#050509")

        main = tk.Frame(self.root, bg="#050509")
        main.pack(padx=10, pady=10)

        # Title
        tk.Label(
            main, text="Block Beam",
            fg="#ffffff", bg="#050509",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            main, text="Puzzle game with Adventure (100 levels) and Classic (random)",
            fg="#aaaaaa", bg="#050509",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 10))

        content = tk.Frame(main, bg="#050509")
        content.pack()

        # Left panel
        left = tk.Frame(content, bg="#111320")
        left.grid(row=0, column=0, padx=(0, 10))

        # Right panel
        right = tk.Frame(content, bg="#111320")
        right.grid(row=0, column=1)

        # Mode buttons
        mode_frame = tk.Frame(left, bg="#111320")
        mode_frame.pack(padx=10, pady=10)

        self.btn_adv = tk.Button(
            mode_frame, text="🚀 Adventure",
            command=self.set_adventure,
            bg="#ffb347", fg="#111111",
            relief="flat", padx=10, pady=4
        )
        self.btn_adv.grid(row=0, column=0, padx=(0, 5))

        self.btn_cls = tk.Button(
            mode_frame, text="🎲 Classic",
            command=self.set_classic,
            bg="#222433", fg="#ffffff",
            relief="flat", padx=10, pady=4
        )
        self.btn_cls.grid(row=0, column=1)

        # Info row
        info = tk.Frame(left, bg="#111320")
        info.pack(padx=10, pady=(0, 10), fill="x")

        self.mode_label = tk.Label(info, text="Mode: Adventure", fg="#ffffff", bg="#111320")
        self.mode_label.pack(side="left")

        self.level_label = tk.Label(info, text="Level 1 / 100", fg="#ffffff", bg="#222433", padx=8, pady=2)
        self.level_label.pack(side="right")

        # Grid container
        grid_outer = tk.Frame(left, bg="#111320")
        grid_outer.pack(padx=10, pady=10)

        self.grid_frame = tk.Frame(grid_outer, bg="#050509")
        self.grid_frame.pack()

        # Stats
        stats = tk.Frame(left, bg="#111320")
        stats.pack(padx=10, pady=(0, 10), fill="x")

        self.moves_used_label = tk.Label(stats, text="Moves used: 0", fg="#ffffff", bg="#111320")
        self.moves_used_label.pack(anchor="w")

        self.moves_max_label = tk.Label(stats, text="Max moves: 0", fg="#ffffff", bg="#111320")
        self.moves_max_label.pack(anchor="w")

        # Right panel content
        self.message_label = tk.Label(
            right,
            text="Welcome to Block Beam. Click any block to begin.",
            fg="#ffffff", bg="#111320",
            wraplength=260, justify="left"
        )
        self.message_label.pack(padx=10, pady=10)

        btns = tk.Frame(right, bg="#111320")
        btns.pack(padx=10, pady=10)

        tk.Button(
            btns, text="🔁 Restart",
            command=self.setup_level,
            bg="#ffb347", fg="#111111",
            relief="flat", padx=10, pady=4
        ).grid(row=0, column=0, padx=(0, 5))

        tk.Button(
            btns, text="⏭️ Next level",
            command=self.next_level,
            bg="#222433", fg="#ffffff",
            relief="flat", padx=10, pady=4
        ).grid(row=0, column=1)

    # ---------------- GAME LOGIC ----------------
    def set_adventure(self):
        self.mode = "adventure"
        self.btn_adv.configure(bg="#ffb347", fg="#111111")
        self.btn_cls.configure(bg="#222433", fg="#ffffff")
        self.setup_level()

    def set_classic(self):
        self.mode = "classic"
        self.btn_cls.configure(bg="#ffb347", fg="#111111")
        self.btn_adv.configure(bg="#222433", fg="#ffffff")
        self.setup_level()

    def setup_level(self):
        if self.mode == "adventure":
            t = (self.current_level - 1) / (MAX_ADVENTURE_LEVELS - 1)
            self.grid_size = 5 + int(t * 5)
            self.max_moves = max(5, 14 - int(t * 7))
        else:
            self.grid_size = random.randint(5, 10)
            self.max_moves = random.randint(7, 14)

        self.grid_data = [
            [random.randint(0, 3) for _ in range(self.grid_size)]
            for _ in range(self.grid_size)
        ]

        self.moves_used = 0
        self.build_grid()
        self.update_ui()
        self.set_message("Make all blocks the same color.")

    def build_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        self.cells = []

        for r in range(self.grid_size):
            row_widgets = []
            for c in range(self.grid_size):
                color = COLORS[self.grid_data[r][c]]
                btn = tk.Button(
                    self.grid_frame,
                    bg=color, activebackground=color,
                    width=2, height=1,
                    relief="flat",
                    command=lambda rr=r, cc=c: self.on_click(rr, cc)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_widgets.append(btn)
            self.cells.append(row_widgets)

    def on_click(self, r, c):
        if self.moves_used >= self.max_moves:
            self.set_message("No moves left.")
            return

        self.apply_move(r, c)
        self.moves_used += 1
        self.refresh_colors()
        self.update_ui()
        self.check_win()

    def apply_move(self, r, c):
        coords = [(r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for rr, cc in coords:
            if 0 <= rr < self.grid_size and 0 <= cc < self.grid_size:
                self.grid_data[rr][cc] = (self.grid_data[rr][cc] + 1) % 4

    def refresh_colors(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                color = COLORS[self.grid_data[r][c]]
                self.cells[r][c].configure(bg=color, activebackground=color)

    def all_same(self):
        first = self.grid_data[0][0]
        return all(cell == first for row in self.grid_data for cell in row)

    def check_win(self):
        if self.all_same():
            self.set_message("Level completed!")
        elif self.moves_used >= self.max_moves:
            self.set_message("You lost. No moves left.")

    def update_ui(self):
        self.mode_label.configure(text=f"Mode: {self.mode.capitalize()}")
        if self.mode == "adventure":
            self.level_label.configure(text=f"Level {self.current_level} / {MAX_ADVENTURE_LEVELS}")
        else:
            self.level_label.configure(text="Random level")

        self.moves_used_label.configure(text=f"Moves used: {self.moves_used}")
        self.moves_max_label.configure(text=f"Max moves: {self.max_moves}")

    def set_message(self, text):
        self.message_label.configure(text=text)

    def next_level(self):
        if self.mode == "adventure":
            if self.current_level < MAX_ADVENTURE_LEVELS:
                self.current_level += 1
                self.setup_level()
            else:
                self.set_message("You completed all 100 Adventure levels!")
        else:
            self.setup_level()


if __name__ == "__main__":
    root = tk.Tk()
    BlockBeam(root)
    root.mainloop()
