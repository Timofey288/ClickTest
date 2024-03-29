from tkinter import * 
from tkinter import messagebox
import sqlite3


conn = sqlite3.connect("CLICKS_DATA.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS clicks_info (

	"clicks" INT

	)""")

conn.commit()

tk = Tk() 
tk.title("ClickTest") 
tk.geometry("400x400") 

clicks = 0 
seconds = 0 

def clicks_count(value=""): 
	global clicks, clicks_info

	clicks += 1 

	clicks_info.config(text = f"Clicks: {str(clicks)}") 

def start():
	seconds_count()
	start_button.pack_forget()
	press_text.pack_forget()


clicks_info = Label(tk, font = ("Arial", 20)) 

time_info = Label(tk, font = ("Arial", 20))

press_text = Label(tk, text = "Нажмите start, чтобы начать!", font = ("Arial", 20))
press_text.pack(pady = 30)

start_button = Button(tk, text = "Start", width = 30, height = 3, command = start)
start_button.pack(pady = 10)

click_button = Button(tk, text = "Click me!", width = 30, height = 20, command = clicks_count)

def restart():
	clicks_info.config(text = "Clicks: 0") 
	time_info.config(text = "Time: 0") 
	tk_2.destroy()
	
	seconds_count()

def seconds_count():
	global seconds, time_info, clicks

	try:
		if seconds == 10: # здесь можно изменить время которое пройдет, сейчас задано 10 секунд
			global tk_2

			click_button.pack_forget()
			
			tk_2 = Tk()
			tk_2.wm_attributes("-topmost", True)
			tk_2.title("Info")
			tk_2.geometry("400x400")

			text_info = Label(tk_2, font = ("Arial", 15))
			text_info.pack()

			cur.execute(f"INSERT INTO clicks_info (clicks) VALUES ('{clicks}')")
			conn.commit()

			cur.execute("SELECT clicks FROM clicks_info")
			
			numbers = []

			for result in cur:
				count = result["clicks"]
				numbers.append(count)

			lenght = len(numbers)
			
			messagebox.showinfo("Info", f"Общее колличество кликов: {(sum(numbers)//lenght)}")
			text_info.config(text = f"Общее колличество кликов: {(sum(numbers)//lenght)}")

			restart_prog_button = Button(tk_2, text = "Restart", width = 40, height = 2, command = restart)
			restart_prog_button.pack(pady = 10)

			seconds = 0
			clicks = 0

			tk.after_cancel(seconds)

			tk_2.mainloop()

		clicks_info.pack(ipady = 10)
		time_info.pack(ipady = 10)
		click_button.pack(pady = 50)
		
		tk.after(1000, seconds_count) 
		seconds += 1 

		time_info.config(text = f"Time: {str(seconds)}") 

	except Exception:
		pass

click_button.bind("<Return>", clicks_count)

tk.mainloop() 
