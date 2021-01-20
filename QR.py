import tkinter as tk
import qrcode
from PIL import ImageTk, Image
from sqlalchemy import *
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
def evaluate(event):
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
w.title("كلية الحكمة الجامعة ")
tk.Label(w, text="اسم المادة").pack()
variable = tk.StringVar(w)
variable.set("حاسبات")
r = tk.OptionMenu(w, variable, "حاسبات", "طابعة", "راوتر")
r.pack()
tk.Label(w, text="العدد").pack()
entry2 = tk.Entry(w,width=40)
entry2.bind("<Return>", evaluate)
entry2.pack()
tk.Label(w, text="الرمز").pack()
entry3 = tk.Entry(w,width=40)
entry3.bind("<Return>", evaluate)
entry3.pack()
tk.Label(w, text=" ").pack()
B = tk.Button(w, text ="استخراج البيانات", command = helloCallBack)
B.pack()
res = tk.Label(w)
res.pack()
img = ImageTk.PhotoImage(Image.open("a.png"))
panel = tk.Label(w, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
w.mainloop()