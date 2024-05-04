# 卍
from PyQt5.QtCore import Qt
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel,QListWidget,QLineEdit,\
    QTextEdit,QHBoxLayout,QVBoxLayout,QInputDialog,QMessageBox
# from ui import Ui_MainWindow
# from random import randint,choice  

app=QApplication([])
#Розумні замітки
win=QWidget()
win.setWindowTitle("Розумне, для розумних!")
win.resize(900, 600)

#|||
QNotes=QTextEdit()
#|||

#||||||||||||||||| НАЗВИ ЗАМІТОК ||||||||||||||||||||

Note_z=QLabel('Список заміток')

z_List=QListWidget()

Add_z=QPushButton('Створити замітку')
Del_z=QPushButton('Видаллити замітку')
Save_z=QPushButton('Зберегти замітку')
#||||||||||||||||||| НАЗВИ ТЕГ ||||||||||||||||||||||
Note_t=QLabel('Список тегів')

t_List=QListWidget()

LineEdit=QLineEdit('')
LineEdit.setPlaceholderText('Введіть тег...')

Add_t=QPushButton('Додати до замітки')
Del_t=QPushButton('Відкріпити від заміток')
Seeck_t=QPushButton('Шукати замітки по тегу')
#||||||||||||||||||||||||||||||||||||||||||||||||||||

#|||
main_layout=QHBoxLayout()
#|||

#|||||||||||||||||| ЗАМІТКИ |||||||||||||||||||||||||
VBox_layout=QVBoxLayout()
VBox_layout.addWidget(Note_z)

VBox_layout.addWidget(z_List)

HBox_layout1=QHBoxLayout()
HBox_layout1.addWidget(Add_z)
HBox_layout1.addWidget(Del_z)
VBox_layout.addLayout(HBox_layout1)
VBox_layout.addWidget(Save_z)
#|||||||||||||||||| ТЕГИ ||||||||||||||||||||||||||||
VBox_layout.addWidget(Note_t)

VBox_layout.addWidget(t_List)

VBox_layout.addWidget(LineEdit)

HBox_layout2=QHBoxLayout()
HBox_layout2.addWidget(Add_t)
HBox_layout2.addWidget(Del_t)
VBox_layout.addLayout(HBox_layout2)
VBox_layout.addWidget(Seeck_t)
#||||||||||||||||||||||||||||||||||||||||||||||||||||

main_layout.addWidget(QNotes,stretch=2)
main_layout.addLayout(VBox_layout,stretch=1)
win.setLayout(main_layout) #卍

def show_note():
    key=z_List.selectedItems()[0].text()
    QNotes.setText(notes[key]["текст"])
    t_List.clear()
    t_List.addItems(notes[key]["теги"])

#|||||||||||||||||| ЗАМІТКИ |||||||||||||||||||||||||
def add_note():
    name, ok=QInputDialog.getText(win,"Додати замітку...","Введіть назву нової замітки:")
    if ok and name !="":
        notes[name]={"текст":"","теги":[]}
        z_List.addItem(name)

def save_note():
    if z_List.selectedItems():
        key=z_List.selectedItems()[0].text()
        notes[key]["текст"]=QNotes.toPlainText()
        with open("notes_data.json","w") as file:
            json.dump(notes,file,sort_keys=True)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def del_note():
    if z_List.selectedItems():
        box=QMessageBox(text="Ви точно готові видалити замітку?")
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if box.exec_()==QMessageBox.Ok:
            key=z_List.selectedItems()[0].text()
            del notes[key]
            QNotes.clear()
            z_List.clear()
            z_List.addItems(notes)
            t_List.clear()
            with open("notes_data.json","w") as file:
                json.dump(notes,file,sort_keys=True)

    else:
        QMessageBox(text="Замітка не обрана").exec_()

# |||||||||||||||||| ТЕГИ ||||||||||||||||||||||||||||
def add_tag():
    if z_List.selectedItems():
        key=z_List.selectedItems()[0].text()
        tag=LineEdit.text()
        if tag !=""and not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            t_List.clear()
            t_List.addItems(notes[key]["теги"])
            LineEdit.clear()
            with open("notes_data.json","w") as file:
                json.dump(notes,file,sort_keys=True, ensure_ascii=False)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def del_tag():
    if z_List.selectedItems() and t_List.selectedItems():
        key=z_List.selectedItems()[0].text()
        key=t_List.selectedItems()[0].text()
        tag=LineEdit.text()
        notes[key]["теги"].remove(tag)
        t_List.clear()
        t_List.addItems(notes[key]["теги"])
        LineEdit.clear()
        with open("notes_data.json","w") as file:
            json.dump(notes,file,sort_keys=True, ensure_ascii=False)
    else:
        QMessageBox(text="Замітка не обрана").exec_()

def seeck_t():
    tag=LineEdit.text()
    if Seeck_t.text()=='Шукати замітки по тегу' and tag!='':
        notes_filtered={}
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        z_List.clear()
        z_List.addItems(notes_filtered)
        t_List.clear()
        Seeck_t.setText('Скинути пошук')
    elif Seeck_t.text()=='Скинути пошук':
        z_List.clear()
        z_List.addItems(notes)
        t_List.clear()
        LineEdit.clear()
        Seeck_t.setText('Шукати замітки по тегу')



#||||||||||||||||||Виконання|||||||||||||||||||||||||
z_List.itemClicked.connect(show_note)
Add_z.clicked.connect(add_note)
Save_z.clicked.connect(save_note)
Del_z.clicked.connect(del_note)
Add_t.clicked.connect(add_tag)
Del_t.clicked.connect(del_tag)
Seeck_t.clicked.connect(seeck_t)

with open("notes_data.json","r") as file:
    notes=json.load(file)

z_List.addItems(notes)


win.show()
app.exec_()

# Не дивитися до 72 стрічки!