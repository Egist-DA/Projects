from tkinter import *
import math
import tkinter.messagebox

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


#  when app is minimised
def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
    elif option == "off":
        window.attributes('-topmost', 0)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label.config(text="Timer")
    check.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        focus_window("on")
        tkinter.messagebox.showinfo(title="Break", message="Long break!")
        count_down(long_break_sec)
        label.config(text="Break!", fg=RED)
    elif reps % 2 == 0:
        focus_window("on")
        tkinter.messagebox.showinfo(title="Work", message="Small break!")
        count_down(short_break_sec)
        label.config(text="Break~", fg=PINK)
    else:
        focus_window("off")
        tkinter.messagebox.showinfo(title="Work", message="Start working~")
        count_down(work_sec)
        label.config(text="Work")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps

    count_minute = math.floor(count / 60)  # gives us the largest number less than itself
    count_seconds = count % 60  # gives us the reminder

    if count_seconds < 10:
        count_seconds = f"0{count_seconds}"  # dynamic typing (from int to string) - dynamically change the variables
        # type from
        # variables to variables
        # f"0{count_seconds} it is when we are below 10 seconds, and we want to show in the format of 09, 08... seconds

    canvas.itemconfig(timer_text, text=f"{count_minute}:{count_seconds}")  # to change the value of a canvas
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    # milliseconds, function, #args (the argument that we are going to pass in the function)

    else:
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)
        window.bell()
        start_timer()  # after it counted everything, we want to call again the function
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

label = Label(text="Timer", font=(FONT_NAME, 48), bg=YELLOW, fg=GREEN)
label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)  # x and y values
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start = Button(text="Start", highlightbackground=YELLOW, command=start_timer)
start.grid(row=3, column=0)

reset = Button(text="Reset", highlightbackground=YELLOW, command=reset_timer)
reset.grid(row=3, column=2)

check = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 32))
check.grid(row=4, column=1)

window.lift()
window.attributes('-topmost', True)
window.after_idle(window.attributes, '-topmost', False)
window.mainloop()
