from tkinter import *
import sqlite3

root = Tk()
root.title('CZC price monitoring')
root.geometry('1200x800')

# Frames
selection_frame = LabelFrame(root, text = 'Menu', padx = 10, pady = 10)
names_frame = LabelFrame(root, text = 'Jméno produktu', padx = 10, pady = 10)
prices_frame = LabelFrame(root, text = 'Cena', padx = 10, pady = 10)

# Dropdown menus for category and subcategory selection
categories = [
		'Komponenty',
		'PC doplňky'
]

komponenty = {
		'Procesory' : 'Procesory',
		'Základní desky' : 'Základní_desky',
		'Grafické karty' : 'Grafické_karty_do_PC',
		'Operační paměti' : 'Operační_paměti',
		'Disky' : 'Pevné_a_SSD_disky',
		'Skříně' : 'PC_skříně_Case',
		'Zdroje' : 'PC_zdroje',
		'Rozšiřující karty' : 'Rozšiřující_karty_pro_PC_a_NB',
		'Chladiče' : 'Chladiče'
}

pc_doplnky = {
		'Monitory' : 'Monitory',
		'Tiskárny' : 'Tiskárny_a_náplně',
		'Klávesnice' : 'Klávesnice',
		'Myši' : 'Myši',
		'Sluchátka' : 'Sluchátka_a_mikrofony',
		'Reproduktory' : 'Reproduktory',
		'Paměťové karty' : 'Paměťové_karty',
		'Flash disky' : 'Flash_disky'
}

selected_cat = StringVar()
selected_sub = StringVar()

def clicked_cat(*args):
	if selected_cat.get() == 'Komponenty':
		dropdown_sub = OptionMenu(selection_frame, selected_sub, *list(komponenty.keys()))
		dropdown_sub.grid(row = 1, column = 0, padx = 10, pady = 10)

	elif selected_cat.get() == 'PC doplňky':
		dropdown_sub = OptionMenu(selection_frame, selected_sub, *list(pc_doplnky.keys()))
		dropdown_sub.grid(row = 1, column = 0, padx = 10, pady = 10)

def clicked_sub(*args):
	for widget in names_frame.winfo_children():
		widget.destroy()

	active_sub = selected_sub.get()
	conn = sqlite3.connect('database.db')
	c = conn.cursor()

	if selected_cat.get() == 'Komponenty':
		active_dict = komponenty
		c.execute(f'SELECT * FROM {active_dict[active_sub]}')

	elif selected_cat.get() == 'PC doplňky':
		active_dict = pc_doplnky
		c.execute(f'SELECT * FROM {active_dict[active_sub]}')

	# else:
	# 	print('Not found')

	def show_price():
		conn = sqlite3.connect('database.db')
		c = conn.cursor()

		c.execute(f'SELECT price FROM {active_dict[active_sub]} WHERE product_name = ?', (names_listbox.get(ANCHOR), ))

		for widget in prices_frame.winfo_children():
			widget.destroy()

		price = Label(prices_frame, text = c.fetchone()[0])
		price.pack()
		conn.close()

	scrollbar = Scrollbar(names_frame, orient = VERTICAL)
	names_listbox = Listbox(names_frame, width = 70, height = 20, yscrollcommand = scrollbar.set)
	scrollbar.config(command = names_listbox.yview, width = 20)

	for product in c.fetchall():
		names_listbox.insert(END, product[0])

	scrollbar.pack(side = RIGHT, fill = Y)
	show_price_button = Button(names_frame, text = 'Ukaž cenu', command = show_price)
	names_listbox.pack()
	show_price_button.pack()

	conn.commit()
	conn.close()

dropdown_cat = OptionMenu(selection_frame, selected_cat, *categories)
selected_cat.trace('w', clicked_cat)
selected_sub.trace('w', clicked_sub)

# Putting the content on the screen
selection_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N)
names_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
prices_frame.grid(row = 0, column = 2, padx = 10, pady = 10)

dropdown_cat.grid(row = 0, column = 0, padx = 10, pady = 10)

root.mainloop()