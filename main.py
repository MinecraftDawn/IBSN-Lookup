# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 21:13:50 2020

@author: Eric
"""

import isbnlib
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Create a conection of database
conn = sqlite3.connect("books.db")

# Create a cursor of connection
cursor = conn.cursor()
# SQL of create the table
sql = """CREATE TABLE IF NOT EXISTS BOOKS (
         isbn VARCHAR(13) PRIMARY KEY,
         title VARCHAR(255) NOT NULL,
         publisher VARCHAR(255),
         year VARCHAR(5),
         language VARCHAR(10),
         count INTEGER DEFAULT 1);"""
# Create table
cursor.execute(sql)

# Commit the change
conn.commit()

def insert(isbnData:dict):
    # Get the data from dict
    isbn = isbnData.get("ISBN-13")
    title = isbnData.get("Title")
    authors = isbnData.get("Authors")
    publisher = isbnData.get("Publisher")
    year = isbnData.get("Year")
    language = isbnData.get("Language")
    
    # SQL of isbn exist
    sql = """SELECT *
             FROM BOOKS
             WHERE isbn=?;"""
    cursor.execute(sql, (isbn,))
    # Get the sql respond
    sqlRespond = cursor.fetchall()
    
    # If isbn in table
    if not sqlRespond:
        # SQL of insert a new book
        sql = """INSERT INTO BOOKS (isbn, title, publisher, year, language)
                 VALUES (?,?,?,?,?);"""
        cursor.execute(sql, (isbn, title, publisher, year, language))
    # If isbn not in table
    else:
        # SQL of update count of the book
        sql = """UPDATE BOOKS
                 SET count=?
                 WHERE isbn=?;"""
        cursor.execute(sql, (sqlRespond[0][5]+1, isbn))
    # Submit commit
    conn.commit()

#isbn = "9789863478751"
##isbn = "9780446310789"
#a = isbnlib.meta(isbn)
#insert(a)


window = tk.Tk()
window.geometry("800x600")
window.resizable(False,False)

def clearTree():
    for item in dataTree.get_children():
        dataTree.delete(item)
        
def showTree():
    sql = """SELECT *
             FROM BOOKS"""
    cursor.execute(sql)
    sqlRespond = cursor.fetchall()
    
    for data in sqlRespond:
        ibsn = data[0]
        title = data[1]
        dataTree.insert('','end',values=[ibsn, title])

def insertBtn():
    isbn = isbnEntry.get()
    if not (isbnlib.is_isbn10(isbn) or isbnlib.is_isbn13(isbn)):
        messagebox.showwarning("ISBN錯誤","請再確認ISBN碼")
        isbnVar.set("")
        return
    
    try:
        isbnDict = isbnlib.meta(isbn)
        insert(isbnDict)
        
        clearTree()
        showTree()
    except isbnlib.ISBNLibException:
        messagebox.showwarning("Bug","此書無法自動填入資料(問題待解決)")
        

isbnLabel = tk.Label(window, text="ISBN：", font=("Verdana", 20))
isbnLabel.place(x=200, y=10)

isbnVar = tk.StringVar()
isbnEntry = tk.Entry(window,textvariable=isbnVar, width=15, font=("Verdana", 20))
isbnEntry.place(x=300, y=10)

insertButton = tk.Button(window, text="新增", font=("Verdana", 13), command=insertBtn)
insertButton.place(x=580, y=10)

dataTree = ttk.Treeview(window, show="headings", columns=["ISBN","Title"])
dataTree.column("ISBN", width=150)
dataTree.column("Title", width=300)
dataTree.heading("ISBN", text="ISBN", anchor="center")
dataTree.heading("Title", text="書名", anchor="center")
dataTree.place(x=190, y=80)
showTree()



window.mainloop()



# Close connection
conn.close()