import sys
from PySide2.QtUiTools import QUiLoader
from PyQt5.QtWidgets import QApplication  
from PySide2.QtCore import QFile, QIODevice
import qrcode
from sqlalchemy import *
import os

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

def aa():

    conn = engine.connect()

    # The result of a "cursor.execute" can be iterated over by row
    f = open("db.txt", "w",encoding="utf-8")
    for row in conn.execute('SELECT * FROM users;'):
        f.write(str(row)+"\n")
    f.close()
    # Be sure to close the connection
    conn.close()


def foo():
    print( 1, 2)
    try:
        if window.lineEdit.text() and int(window.spinBox.text()):
            # The result of a "cursor.execute" can be iterated over by row
            conn = engine.connect()
            for row in conn.execute('SELECT * FROM users;'):
                global x
                x = row[1] in window.comboBox.currentText()
            if x :
                qr = qrcode.QRCode(

                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=20,
                    border=4,
                )
                number=int(window.spinBox.text())+int(row[2])
                qr.add_data("اسم القطعة :"+window.comboBox.currentText()+"\n عدد القطع :"+str(number)+"\n الرمز:: "+window.lineEdit.text())
                qr.make(fit=True)
                print(row[0])
                img = qr.make_image(fill_color="black", back_color="white")
                stmt = users.update().\
                        values(number=number).\
                        where(users.c.id == row[0])
                conn.execute(stmt)
                conn.close()
                img.show()
                with open('QR_images/'+window.lineEdit.text()+'.png', 'wb') as f:
                    img.save(f)
            else:
                qr = qrcode.QRCode(

                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=20,
                    border=4,
                )
                qr.add_data("اسم القطعة :"+str(window.comboBox.currentText())+"\n عدد القطع :"+str(window.spinBox.text()))
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                print(conn.execute(ins, { "name":str(window.comboBox.currentText()), "number": window.spinBox.text() , "code": str(window.lineEdit.text())}))
                conn.close()
                img.show()
                with open('QR_images/'+window.lineEdit.text()+'.png', 'wb') as f:
                    img.save(f)
    except Exception as e:
      print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_file_name = "a.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.pushButton.clicked.connect(foo)
    
    window.pushButton_2.clicked.connect(aa)

    window.show()

    sys.exit(app.exec_())