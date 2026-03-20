import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime

# ===== LOGIC ENGINE =====
class SATLogicEngine:
    def __init__(self):
        self.math_library = {
            "Heart of Algebra": {
                "keywords": r"linear|system|no solution|infinitely many|parallel|perpendicular",
                "formula": "y = mx + b | m = (y2-y1)/(x2-x1)",
                "logic": "No solution: same slope, different intercept. Infinitely many: same slope, same intercept."
            },
            "Advanced Math": {
                "keywords": r"quadratic|parabola|vertex|roots|zeros|exponential",
                "formula": "x = -b/2a | Δ = b^2 - 4ac",
                "logic": "Δ > 0: 2 roots | Δ = 0: 1 root | Δ < 0: no real roots"
            },
            "Data Analysis": {
                "keywords": r"mean|median|standard deviation|probability|ratio|percent",
                "formula": "Mean = sum/n | P = favorable/total",
                "logic": "Standard deviation measures spread"
            },
            "Geometry": {
                "keywords": r"circle|radius|triangle|angle|volume|radians",
                "formula": "(x-h)^2 + (y-k)^2 = r^2 | SOHCAHTOA",
                "logic": "Area of sector = (θ/360) * πr²"
            }
        }

        self.verbal_strategies = {
            r"main idea|primary purpose|central claim": {
                "type": "Main Idea",
                "summary": "Identify the core message of the passage",
                "keywords": ["thesis", "overall", "primary"],
                "strategy": "Read first + last sentence carefully"
            },
            r"infer|imply|suggest": {
                "type": "Inference",
                "summary": "Find conclusion supported by text",
                "keywords": ["evidence", "support"],
                "strategy": "Do NOT assume anything"
            },
            r"function|role": {
                "type": "Function",
                "summary": "Explain why the sentence is used",
                "keywords": ["context", "transition"],
                "strategy": "Check before and after sentence"
            },
            r"vocabulary|meaning|closest meaning": {
                "type": "Vocabulary",
                "summary": "Find meaning from context",
                "keywords": ["synonym", "context"],
                "strategy": "Replace word mentally"
            }
        }

    def analyze_math(self, text):
        results = []
        for cat, content in self.math_library.items():
            if re.search(content["keywords"], text.lower()):
                results.append(
                    f"📍 {cat}\nFormula: {content['formula']}\nLogic: {content['logic']}\n"
                )
        return "\n".join(results) if results else "No specific Math concept detected."

    def analyze_verbal(self, text):
        for pattern, data in self.verbal_strategies.items():
            if re.search(pattern, text.lower()):
                return (
                    f"--- {data['type']} ---\n\n"
                    f"Summary: {data['summary']}\n"
                    f"Keywords: {', '.join(data['keywords'])}\n"
                    f"Strategy: {data['strategy']}"
                )

        return "General strategy: Look for transitions and eliminate extreme answers."

    def log_action(self, section, user_input, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {section}\nInput: {user_input[:50]}...\nResult: {result[:50]}...\n{'-'*30}\n"

        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(entry)


# ===== GUI =====
class SATApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAT Intelligent Assistant")
        self.root.geometry("650x500")

        self.engine = SATLogicEngine()

        tk.Label(root, text="SAT REASONING SYSTEM", font=("Arial", 16)).pack(pady=10)

        self.container = ttk.Frame(root)
        self.container.pack(expand=True, fill="both", padx=20, pady=10)

        self.show_home()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_screen()

        tk.Label(self.container, text="Select a module").pack(pady=10)

        ttk.Button(self.container, text="Verbal", command=self.show_verbal).pack(pady=10)
        ttk.Button(self.container, text="Math", command=self.show_math).pack(pady=10)
        ttk.Button(self.container, text="History", command=self.show_history).pack(pady=10)

    def show_verbal(self):
        self.clear_screen()

        ttk.Button(self.container, text="Back", command=self.show_home).pack()

        self.v_input = tk.Text(self.container, height=5, width=60)
        self.v_input.pack()

        self.v_output = tk.Label(self.container, text="", wraplength=500, justify="left")
        self.v_output.pack()

        def run():
            res = self.engine.analyze_verbal(self.v_input.get("1.0", tk.END))
            self.v_output.config(text=res)
            self.engine.log_action("Verbal", self.v_input.get("1.0", tk.END), res)

        ttk.Button(self.container, text="Analyze", command=run).pack()

    def show_math(self):
        self.clear_screen()

        ttk.Button(self.container, text="Back", command=self.show_home).pack()

        self.m_input = ttk.Entry(self.container, width=60)
        self.m_input.pack()

        self.m_output = tk.Label(self.container, text="", wraplength=500, justify="left")
        self.m_output.pack()

        def run():
            res = self.engine.analyze_math(self.m_input.get())
            self.m_output.config(text=res)
            self.engine.log_action("Math", self.m_input.get(), res)

        ttk.Button(self.container, text="Analyze", command=run).pack()

    def show_history(self):
        self.clear_screen()

        ttk.Button(self.container, text="Back", command=self.show_home).pack()

        text = tk.Text(self.container, height=15, width=70)
        text.pack()

        try:
            with open("history.txt", "r", encoding="utf-8") as f:
                text.insert(tk.END, f.read())
        except:
            text.insert(tk.END, "No history yet.")

        text.config(state="disabled")


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = SATApp(root)
    root.mainloop()