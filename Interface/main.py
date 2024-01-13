import tkinter as tk
def create_ui():
    window = tk.Tk()
    window.title("Life Flow")

    # Welcome Label
    welcome_label = tk.Label(window, text="Welcome\nTo Life Flow", font=("Arial", 20), pady=10)
    welcome_label.pack()

    # Voice Control Button
    voice_control_button = tk.Button(window, text="Voice control: On", bg="green", fg="white", font=("Arial", 15), width=25, height=2)
    voice_control_button.pack()

    # Narrator Button
    narrator_button = tk.Button(window, text="Narrator: On", bg="green", fg="white", font=("Arial", 15), width=25, height=2)
    narrator_button.pack()

    # Languages Button
    languages_button = tk.Button(window, text="Languages", bg="gray", fg="white", font=("Arial", 15), width=25, height=2)
    languages_button.pack()

    # More Information Button
    more_info_button = tk.Button(window, text="More Information", bg="gray", fg="white", font=("Arial", 15), width=25, height=2)
    more_info_button.pack()

    # Done Button
    done_button = tk.Button(window, text="DONE", bg="blue", fg="white", font=("Arial", 15), width=25, height=2, command=window.destroy)
    done_button.pack()

    window.mainloop()

create_ui()