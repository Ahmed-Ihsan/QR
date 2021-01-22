import tkinter as tk
from tkinter import *   
import qrcode
from openpyxl import Workbook
from sqlalchemy import *
from PIL import ImageTk, Image
import os

# define the name of the directory to be deleted
path = "QR_images"
try:
	os.mkdir(path)
except Exception as e:
    print(1)

metadata = MetaData()
engine = create_engine('sqlite:///db.sqlite')
conn = engine.connect()
users = Table('users', metadata,
	     Column('id', Integer, primary_key=True),
	     Column('name', String),
	     Column('number', Integer),
	     Column('code', String),
 )
metadata.create_all(engine)
ins = users.insert()
x=None

def aa2():
	workbook = Workbook()
	sheet = workbook.active
	workbook.save(filename="db.xlsx")
	conn = engine.connect()
    # The result of a "cursor.execute" can be iterated over by row
	x=1
	for row in conn.execute('SELECT * FROM users;'):
		sheet["A"+str(x)] = str(row.name)
		sheet["B"+str(x)] = str(row.number)
		sheet["c"+str(x)] = str(row.code)
		x=x+1
	conn.close()
	workbook.save(filename="db.xlsx")
	res.configure(text = "تم استخراج البيانات")

def evaluate():
	try:
		if variable.get() and int(entry2.get()):
			# The result of a "cursor.execute" can be iterated over by row
			conn = engine.connect()
			for row in conn.execute('SELECT * FROM users;'):
				global x
				x = row[1] in variable.get()
			if x :
				qr = qrcode.QRCode(

			        version=1,
			        error_correction=qrcode.constants.ERROR_CORRECT_L,
			        box_size=20,
			        border=4,
			    )
				number=int(entry2.get())+int(row[2])
				qr.add_data("اسم القطعة :"+variable.get()+"\n عدد القطع :"+str(number)+"\n الرمز:: "+entry3.get())
				qr.make(fit=True)
				print(row[0])
				img = qr.make_image(fill_color="black", back_color="white")
				stmt = users.update().\
				        values(number=number).\
				        where(users.c.id == row[0])
				conn.execute(stmt)
				conn.close()
				res.configure(text ="تم ادخال البيانات" )
				img.show()
				with open('QR_images/'+entry3.get()+'.png', 'wb') as f:
					img.save(f)
			else:
				qr = qrcode.QRCode(

			        version=1,
			        error_correction=qrcode.constants.ERROR_CORRECT_L,
			        box_size=20,
			        border=4,
			    )
				qr.add_data("اسم القطعة :"+str(variable.get())+"\n عدد القطع :"+str(entry2.get()))
				qr.make(fit=True)
				img = qr.make_image(fill_color="black", back_color="white")
				print(conn.execute(ins, { "name":str(variable.get()), "number": entry2.get() , "code": str(entry3.get())}))
				conn.close()
				res.configure(text ="تم ادخال البيانات" )
				img.show()
				with open('QR_images/'+entry3.get()+'.png', 'wb') as f:
					img.save(f)
	except Exception as e:
	  print(e)
	  res.configure(text = "تاكد من ادخال البيانات")

def helloCallBack():

	conn = engine.connect()

	# The result of a "cursor.execute" can be iterated over by row
	f = open("db.txt", "w")
	for row in conn.execute('SELECT * FROM users;'):
		f.write(str(row)+"\n")
	f.close()

	# Be sure to close the connection
	conn.close()
	res.configure(text = "تم استخراج البيانات ")
    
w = tk.Tk()
#w.geometry("200x350")
w.title("كلية الحكمة الجامعة ")
tk.Label(w, text="اسم المادة").grid()
variable = tk.StringVar(w)
variable.set("حاسبات" )
r = tk.OptionMenu(w, variable,"حاسبات","طابعة","راوتر" )
r.grid()
tk.Label(w, text="العدد").grid()
entry2 = tk.Entry(w,width=30)
entry2.bind("<Return>", evaluate)
entry2.grid()
tk.Label(w, text="الرمز").grid()
entry3 = tk.Entry(w,width=30)
entry3.bind("<Return>", evaluate)
entry3.grid()
tk.Label(w, text=" ").grid()
B = tk.Button(w, text ="ادخال", command = evaluate)
B.grid()
tk.Label(w,text="").grid()
o = tk.Button(w, text ="Excel", command = aa2)
o.grid()
tk.Label(w,text="").grid()
c = tk.Button(w, text ="Text", command = helloCallBack)
c.grid()
res = tk.Label(w)
res.grid()
load = Image.open("b.png")
render = ImageTk.PhotoImage(load)
label1 = tk.Label(image=render)
label1.image = render
label1.grid()

w.mainloop()