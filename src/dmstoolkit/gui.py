import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from dmstoolkit import dungeon_generator as dg


class DungeonGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Dungeon Generator")
        self.root.resizable(False, False)

        self.settings = {
            "target_size": tk.StringVar(value="500"),
            "hall_percentage": tk.StringVar(value="70"),
            "room_percentage": tk.StringVar(value="30"),
            "room_9_percentage": tk.StringVar(value="20"),
            "room_7_percentage": tk.StringVar(value="60"),
            "room_5_percentage": tk.StringVar(value="20"),
        }
        self._results: queue.Queue[Exception | None] = queue.Queue()

        form = ttk.Frame(root, padding=16)
        form.grid()

        fields = (
            ("Target size (occupied cells)", "target_size"),
            ("Hall chance (%)", "hall_percentage"),
            ("Room chance (%)", "room_percentage"),
            ("Size 9 room chance (%)", "room_9_percentage"),
            ("Size 7 room chance (%)", "room_7_percentage"),
            ("Size 5 room chance (%)", "room_5_percentage"),
        )
        for row, (label, key) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=4)
            ttk.Entry(form, textvariable=self.settings[key], width=10).grid(
                row=row, column=1, sticky="ew", pady=4
            )

        ttk.Label(
            form,
            text="Hall/room chances and room-size chances must each total 100%.",
            wraplength=300,
        ).grid(row=len(fields), column=0, columnspan=2, sticky="w", pady=(8, 4))

        self.generate_button = ttk.Button(form, text="Generate dungeon", command=self.generate)
        self.generate_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(8, 4))
        self.status = tk.StringVar(value="Ready")
        ttk.Label(form, textvariable=self.status).grid(
            row=len(fields) + 2, column=0, columnspan=2, sticky="w", pady=(4, 0)
        )

    def generate(self) -> None:
        try:
            values: tuple[int, int, int, int, int, int] = (
                int(self.settings["target_size"].get()),
                int(self.settings["hall_percentage"].get()),
                int(self.settings["room_percentage"].get()),
                int(self.settings["room_9_percentage"].get()),
                int(self.settings["room_7_percentage"].get()),
                int(self.settings["room_5_percentage"].get()),
            )
            dg.validate_generation_options(*values)
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error), parent=self.root)
            return

        self.generate_button.configure(state="disabled")
        self.status.set("Generating dungeon...")
        threading.Thread(target=self._generate_in_background, args=(values,), daemon=True).start()
        self.root.after(100, self._check_result)

    def _generate_in_background(self, values: tuple[int, int, int, int, int, int]) -> None:
        try:
            dg.generate_dungeon(*values)
        except Exception as error:
            self._results.put(error)
        else:
            self._results.put(None)

    def _check_result(self) -> None:
        try:
            error = self._results.get_nowait()
        except queue.Empty:
            self.root.after(100, self._check_result)
            return

        self.generate_button.configure(state="normal")
        if error is None:
            self.status.set("Dungeon generated. Check your Downloads folder.")
        else:
            self.status.set("Generation failed.")
            messagebox.showerror("Generation failed", str(error), parent=self.root)


def launch_gui() -> None:
    root = tk.Tk()
    DungeonGeneratorApp(root)
    root.mainloop()
