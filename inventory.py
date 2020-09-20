## Import PyQt5 library

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication


import sys, os

from os import path

def resource_path(relative_path):
    base_path = getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)


from PyQt5.uic import loadUiType

FORM_CLASS,_=loadUiType(resource_path("main.ui"))

import sqlite3


## Main Class

class Main(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        ##Main Function
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.NAVIGATE()
        
    
    def Handel_Buttons(self):
        ## Actions after using buttons
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)
        self.check_btn.clicked.connect(self.LEVEL)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)
        
    
    def GET_DATA(self):
        ## Connect to SQlite3 database
        db = sqlite3.connect(resource_path("parts"))
        cursor = db.cursor()
        
        command = ''' SELECT * from parts_table '''
        
        result = cursor.execute(command)
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    
    
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        cursor4 = db.cursor()
        cursor5 = db.cursor()
        
        
        parts_nbr = ''' SELECT COUNT (DISTINCT PartName) from parts_table '''
        ref_nbr = ''' SELECT COUNT (DISTINCT Reference) from parts_table '''
        
        result_ref_nbr = cursor2.execute(ref_nbr)
        result_parts_nbr = cursor3.execute(parts_nbr)
    
        self.lbl_ref.setText(str(result_ref_nbr.fetchone()[0]))   
        self.lbl_part.setText(str(result_parts_nbr.fetchone()[0]))
        
        min_nbr = ''' SELECT MIN(NumberOfHoles), Reference from parts_table'''
        max_nbr = ''' SELECT MAX(NumberOfHoles), Reference from parts_table'''
        
        result_min_nbr = cursor4.execute(min_nbr)
        result_max_nbr = cursor5.execute(max_nbr)
        
        r1 = result_min_nbr.fetchone()
        r2 = result_max_nbr.fetchone()
        
        self.lbl_min.setText(str(r1[0]))
        self.lbl_max.setText(str(r2[0]))
        self.lbl_min_2.setText(str(r1[1]))
        self.lbl_max_2.setText(str(r2[1]))
    
    
    
    
    
    def SEARCH(self):
        ## Search Function
        db = sqlite3.connect("parts")
        cursor = db.cursor()
        
        nbr = int(self.count_filter_txt.text())
        command = ''' SELECT * from parts_table WHERE Count <=?'''
        
        result = cursor.execute(command,[nbr])
        
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def LEVEL(self):
        db = sqlite3.connect("parts")
        cursor = db.cursor()
        command = '''SELECT Reference, PartName,Count from parts_table order by Count asc LIMIT 3'''
        
        result = cursor.execute(command)
        
        self.table_stat.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table_stat.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_stat.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def NAVIGATE(self):
        db = sqlite3.connect("parts")
        cursor = db.cursor()
        
        command = '''SELECT * from parts_table'''
        
        result = cursor.execute(command)
        val = result.fetchone()
        
        self.id_id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.number_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])

    def UPDATE(self):
            db = sqlite3.connect("parts")
            cursor = db.cursor()
            
            id_= int(self.id_id.text())
            reference_= self.reference.text()
            part_name_= self.part_name.text()
            min_area_= self.min_area.text()
            max_area_= self.max_area.text()
            number_of_holes_= self.number_holes.text()
            min_diameter_= self.min_diameter.text()
            max_diameter_= self.max_diameter.text()
            count_= str(self.count.value())
            
            
            row = (reference_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_,id_)
            
            command = ''' UPDATE parts_table SET Reference=?, PartName=?, MinArea=?, MaxArea=?, NumberOfHoles=?, MinDiameter=?, MaxDiameter=?,Count=? WHERE Id=?'''
            
            cursor.execute(command,row)
            
            db.commit()
            self.print.setText("Update Succesfully")


    def ADD(self):
            db = sqlite3.connect("parts")
            cursor = db.cursor()
            
           
            reference_= self.reference.text()
            part_name_= self.part_name.text()
            min_area_= self.min_area.text()
            max_area_= self.max_area.text()
            number_of_holes_= self.number_holes.text()
            min_diameter_= self.min_diameter.text()
            max_diameter_= self.max_diameter.text()
            count_= str(self.count.value())
            
            
            row = (reference_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_)
            
            command = ''' INSERT INTO parts_table (Reference, PartName, MinArea, MaxArea, NumberOfHoles, MinDiameter, MaxDiameter, Count) VALUES(?,?,?,?,?,?,?,?) '''
            
            cursor.execute(command,row)
            
            db.commit() 
            
            self.print.setText("Added Succesfully")
            

    def DELETE(self):
        db = sqlite3.connect("parts")
        cursor = db.cursor()
        
        d = (self.id_id.text())
        
        command = ''' DELETE from parts_table WHERE id=?'''
        
        cursor.execute(command,d)
        
        db.commit()
        self.print.setText("Deleted Succesfully")
        
        
        
        
        

        
    

def main():
    app = QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()