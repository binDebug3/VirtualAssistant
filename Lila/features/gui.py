import tkinter as tk

# ---------------------------- VARIABLES ------------------------------- #

font = "Times New Roman"
font_size = 10
title_size = 11
font_color = "white"
bg_color = "black"
input_color = "#222222"
input_value = ""

# ---------------------------- FUNCTIONS ------------------------------- #
def handle_enter(event=None):
    global input_box, input_value, root
    input_value = input_box.get()
    # input_box.delete(0, 'end')
    root.destroy()
    # return input_value

def on_title_bar_drag(event):
    global root
    # Calculate the new position of the window based on the mouse movement
    x, y = root.winfo_pointerxy()
    root.geometry("+{}+{}".format(x-offset_x, y-offset_y))

def on_title_bar_release(event):
    title_bar.unbind('<B1-Motion>')
    title_bar.unbind('<ButtonRelease-1>')

# Calculate the offset between the mouse cursor and the top-left corner of the window
def on_title_bar_press(event):
    global offset_x, offset_y, title_bar
    offset_x = event.x
    offset_y = event.y
    title_bar.bind('<B1-Motion>', on_title_bar_drag)
    title_bar.bind('<ButtonRelease-1>', on_title_bar_release)

# ---------------------------- UI SETUP ------------------------------- #

def input_window(title):
    # Create the main window
    global title_bar, root, input_box
    root = tk.Tk()
    root.title("Lila")
    root.geometry("300x180")
    root.configure(bg=bg_color)
    root.overrideredirect(True)

    # Create custom title bar
    title_bar = tk.Frame(root, bg=bg_color, relief='raised', bd=0)
    title_bar.pack(expand=1, fill='x')

    # Create title label in the custom title bar
    title_label = tk.Label(title_bar, text="Lila", bg=bg_color, fg=font_color, font=(font, title_size))
    title_label.pack(side='left', padx=5)

    # Create close button in the custom title bar
    close_button = tk.Button(title_bar, text='x', bg=bg_color, fg=font_color, font=(font, title_size), bd=0, command=root.destroy)
    close_button.pack(padx=5, side='right')

    # ---------------------------- INPUT BOX ------------------------------- #

    # Create label above the input box
    label = tk.Label(root, text=title, font=(font, font_size), bg=bg_color, fg=font_color)
    label.pack(pady=1)

    # Create the input textbox
    input_box = tk.Entry(root, width=20, font=(font, 15), bg=input_color, fg=font_color)
    input_box.pack(pady=10)

    # ---------------------------- BINDINGS ------------------------------- #

    input_box.bind("<Return>", handle_enter)

    # Bind the mouse button events to the title bar
    title_bar.bind('<ButtonPress-1>', on_title_bar_press)

    # Set the input box to stay on top
    root.wm_attributes("-topmost", 1)

    # Place the window at the center of the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 8) - (width // 8)
    y = (root.winfo_screenheight() // 8) - (height // 8)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # ---------------------------- MAIN LOOP ------------------------------- #

    root.mainloop()

    return input_value