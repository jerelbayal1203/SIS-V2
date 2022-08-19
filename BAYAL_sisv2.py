#AUTHOR: JEREL BAYAL


#================================================== SIMPLE STUDENT INFORMATION SYSTEM (VER. 2) ==================================================#


from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox

top = Tk()


def SSIS(root):
    root.title("STUDENT INFORMATION SYSTEM")
    root.geometry(f'{1200}x{600}+{80}+{60}')
    root.config(bg='sky blue')
    root.resizable(False, False)

    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = 1")

    c.execute("""CREATE TABLE IF NOT EXISTS studentinfo (ID_NUM VARCHAR(9) NOT NULL PRIMARY KEY, S_NAME VARCHAR(50) NOT NULL,
              GENDER VARCHAR(10) NOT NULL, YR_LVL VARCHAR(10) NOT NULL, S_COURSECODE VARCHAR(25) NOT NULL,
              FOREIGN KEY (S_COURSECODE) REFERENCES  courseinfo (C_CODE) ON UPDATE CASCADE ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS courseinfo (C_CODE VARCHAR(20) NOT NULL PRIMARY KEY, C_NAME VARCHAR(100) NOT NULL)""")

    idno = StringVar()
    name = StringVar()
    yrlvl = StringVar()
    gender = StringVar()
    courseid = StringVar()
    schidno = StringVar()
    schccode = StringVar()


#======================================== FRAMES AND LABELS =======================================#


    headlabel = Label(root, text="", bg="pink", fg="black", font=("Arial", 30, "bold"), anchor="center")
    headlabel.place(x=10, y=10, width=1180, height=50)
    
    studentroot = LabelFrame(root, bg='pink', text="    STUDENT DETAILS   ", fg="black", font=("Arial", 20, "bold"))
    courseroot = LabelFrame(root, bg='pink',  text="    COURSE DETAILS   ", fg="black", font=("Arial", 20, "bold"))
    displayroot = LabelFrame(root, bg='pink', font=("Arial", 20, "bold"))
    displayroot.place(x=470, y=80, height=400, width=720)
    
    slabel = Label(displayroot, bg="black", fg="gold", font=("Arial", 12, "bold"), anchor="w")
    slabel.place(x=10, y=15, height=30, width=90)
    searchid = Entry(displayroot, textvariable=schidno, font=("Arial", 12))
    searchcode = Entry(displayroot, textvariable=schccode, font=("Arial", 12))

    studlist = Frame(displayroot, bg="white")
    courselist = Frame(displayroot, bg="white")

    sy = Scrollbar(studlist, orient=VERTICAL)
    sx = Scrollbar(studlist, orient=HORIZONTAL)
    cy = Scrollbar(courselist, orient=VERTICAL)
    studtable = ttk.Treeview(studlist, columns=("id_no", "name", "gender", "course", "yrlvl"), xscrollcommand=sx, yscrollcommand=sy)
    coursetable = ttk.Treeview(courselist, columns=("course_code", "course_name"), yscrollcommand=cy)




#======================================== STUDENT LIST FUNCTIONS =======================================#


    def student():
        ccourse = []
        c.execute("SELECT C_CODE from courseinfo")
        res = c.fetchall()
        for x in res:
            ccourse.append(x[0])

        key = StringVar()


#========== ADD STUDENT ==========#


        def addStudent():
            studid = idno.get()
            if studid == "" or name.get() == "" or gender.get() == "" or yrlvl.get() == "" or courseid.get() == "":
                messagebox.showerror("ERROR", "Please fill out all fields!")
                return
            elif len(studid) != 9 or studid[4] != '-' or not studid.replace("-", "").isdigit():
                messagebox.showerror("ERROR", "Invalid ID Number")
                return
            else:
                if messagebox.askyesno("Add Student", "Do you wish to add the student information?"):
                    try:
                        c.execute("INSERT INTO studentinfo VALUES(?, ?, ?, ?, ?)",
                                  (studid, name.get(), gender.get(), yrlvl.get(), courseid.get()))
                        messagebox.showinfo("SUCCESS", "Student added!")
                        conn.commit()
                        clear()
                        searchStudent()
                    except sqlite3.IntegrityError:
                        if courseid.get() not in ccourse:
                            messagebox.showerror("ERROR", "Course ID not found.")
                        else:
                            messagebox.showerror("ERROR", "Student ID already in database!")


#========== SEARCH STUDENT ==========#


        def searchStudent():
            if schidno.get() == "":
                c.execute("SELECT * FROM studentinfo")
            elif not schidno.get().replace("-", "").isdigit():
                messagebox.showerror("ERROR", "Search Error!")
                return
            else:
                c.execute("SELECT * FROM studentinfo WHERE ID_NUM LIKE ?", ('%' + schidno.get() + '%',))
            search = c.fetchall()
            studtable.delete(*studtable.get_children())
            if not search:
                return
            else:
                for x in search:
                    studtable.insert('', END, values=(x[0], x[1], x[2], x[4], x[3]))


#========== DELETE STUDENT ==========#


        def deleteStudent():
            sel = studtable.focus()
            cont = studtable.item(sel)
            rows = cont['values']
            if rows == "":
                messagebox.showerror("ERROR", "Select a student.")
            else:
                if messagebox.askyesno("Delete Student", "Confirm deleting student information?"):
                    c.execute("DELETE FROM studentinfo WHERE ID_NUM=?", (rows[0],))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", "Student information deleted!")
                    clear()
                    searchStudent()
                else:
                    return


#========== UPDATE STUDENT ==========#


        def updateStudent():
            studid = idno.get()
            if key.get() == "":
                messagebox.showerror("ERROR", "Select a student.")
                return
            elif studid == "" or name.get() == "" or gender.get() == "" or yrlvl.get() == "" or courseid.get() == "":
                messagebox.showerror("ERROR", "Please fill out all fields!")
                return
            elif len(studid) != 9 or studid[4] != '-' or not studid.replace("-", "").isdigit():
                messagebox.showerror("ERROR", "Invalid ID Number")
                return
            else:
                if messagebox.askyesno("Update Student", "Confirm updating student information?"):
                    try:
                        if key.get() != studid:
                            c.execute("UPDATE studentinfo SET ID_NUM=?, S_NAME=?, GENDER=?, ""YR_LVL=?, S_COURSECODE=? WHERE ID_NUM=?",
                                      (studid, name.get(), gender.get(), yrlvl.get(), courseid.get(), key.get()))
                        else:
                            c.execute("UPDATE studentinfo SET S_NAME=?, GENDER=?, ""YR_LVL=?, S_COURSECODE=? WHERE ID_NUM=?",
                                      (name.get(), gender.get(), yrlvl.get(), courseid.get(), studid))
                        conn.commit()
                        messagebox.showinfo("SUCCESS", "Student information updated!")
                        key.set("")
                        clear()
                        searchStudent()
                    except sqlite3.IntegrityError:
                        if courseid.get() not in ccourse:
                            messagebox.showerror("ERROR", "Course ID found.")
                        else:
                            messagebox.showerror("ERROR", "Student ID already in database!")


#========== CLEAR AND SELECT STUDENT ==========#


        def clear():
            idno.set("")
            name.set("")
            yrlvl.set("")
            gender.set("")
            courseid.set("")

        def selectStudent(ev):
            sel_row = studtable.focus()
            selco = studtable.item(sel_row)
            rows = selco['values']
            clear()
            key.set(rows[0])
            idno.set(rows[0])
            name.set(rows[1])
            gender.set(rows[2])
            courseid.set(rows[3])
            yrlvl.set(rows[4])


#======================================== STUDENT LIST FEATURES =======================================#


        headlabel.config(text="STUDENT INFORMATION SYSTEM")
        displayroot.config(text="    LIST OF STUDENTS   ", fg="black")
        studentroot.place(x=10, width=450, y=120, height=360)
        
        lid = Label(studentroot, text="  ID NUMBER", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        lid.place(x=10, y=20, width=135, height=35)
        eid = Entry(studentroot, textvariable=idno, font=("Arial", 12, "bold"))
        eid.place(x=145, y=20, width=280, height=35)
        
        lname = Label(studentroot, text="  NAME", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        lname.place(x=10, y=60, width=135, height=35)
        ename = Entry(studentroot, textvariable=name, font=("Arial", 12, "bold"))
        ename.place(x=145, y=60, width=280, height=35)
        
        lgender = Label(studentroot, text="  GENDER", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        lgender.place(x=10, y=100, width=135, height=35)
        egender = ttk.Combobox(studentroot, textvariable=gender, values=["MALE", "FEMALE"], font=("Arial", 12, "bold"),)
        egender.place(x=145, y=100, width=280, height=35)
        
        lyear = Label(studentroot, text="  YEAR LEVEL", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        lyear.place(x=10, y=140, width=135, height=35)
        eyear = ttk.Combobox(studentroot, textvariable=yrlvl, values=["1ST YEAR", "2ND YEAR", "3RD YEAR", "4TH YEAR", "5TH YEAR"], font=("Arial", 12, "bold"))
        eyear.place(x=145, y=140, width=280, height=35)
        
        lcourse = Label(studentroot, text="  COURSE", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        lcourse.place(x=10, y=180, width=135, height=35)
        ecourse = ttk.Combobox(studentroot, textvariable=courseid, values=ccourse, font=("Arial", 12, "bold"))
        ecourse.place(x=145, y=180, width=280, height=35)
        
        courseroot.place_forget()
        studbutton.place_forget()
        coursebutton.place(x=425, y=520, width=150, height=50)

        addbut = Button(studentroot, text="ADD", command=addStudent, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        updbut = Button(studentroot, text="UPDATE", command=updateStudent, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        delbut = Button(studentroot, text="DELETE", command=deleteStudent, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        clearbut = Button(studentroot, text="CLEAR", command=clear, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        addbut.place(x=25, y=270, width=90, height=35)
        updbut.place(x=125, y=270, width=90, height=35)
        delbut.place(x=225, y=270, width=90, height=35)
        clearbut.place(x=325, y=270, width=90, height=35)

        courselist.place_forget()
        studtable.pack_forget()
        sx.pack_forget()
        sy.pack_forget()
        studlist.place(x=0, y=65, height=300, width=715)
        slabel.config(text="Student ID: ", bg="violet")
        searchcode.place_forget()
        searchid.place(x=100, y=15, height=30, width=200)
        
        searchbut = Button(displayroot, text="SEARCH", command=searchStudent, relief=FLAT, font=("Arial", 12, "bold"), bg="violet", fg="white", activeforeground="violet", activebackground="white")
        searchbut.place(x=305, height=30, y=15, width=80)
        refreshbut = Button(displayroot, text="VIEW ALL", command=lambda: [schidno.set(""), searchStudent()], relief=FLAT, font=("Arial", 12, "bold"), bg="violet", fg="white", activeforeground="violet", activebackground="white")
        refreshbut.place(x=390, height=30, y=15, width=80)

        sx.pack(side=BOTTOM, fill=X)
        sy.pack(side=RIGHT, fill=Y)
        sx.config(command=studtable.xview)
        sy.config(command=studtable.yview)
        
        studtable.heading("id_no", text="ID NUMBER")
        studtable.heading("name", text="NAME")
        studtable.heading("gender", text="GENDER")
        studtable.heading("course", text="COURSE")
        studtable.heading("yrlvl", text="YEAR")
        
        studtable['show'] = 'headings'
        studtable.column("id_no", width=100, anchor="center")
        studtable.column("name", width=260)
        studtable.column("gender", width=80, anchor="center")
        studtable.column("course", width=170)
        studtable.column("yrlvl", width=80, anchor="center")
        studtable.pack(fill=BOTH, expand=1)
        studtable.bind("<ButtonRelease-1>", selectStudent)

        schidno.set("")
        searchStudent()
        clear()




#======================================== COURSE LIST FUNCTIONS =======================================#



    def course():

        key = StringVar()


#========== ADD COURSE ==========#


        def addCourse():
            if courseid.get() == "" or tcoursename.get(1.0, END) == "":
                messagebox.showerror("ERROR", "Please fill out all fields")
                return
            else:
                if messagebox.askyesno("Add Course", "Do you wish to add the course information?"):
                    try:
                        c.execute("INSERT INTO courseinfo VALUES (?, ?)",
                                  (courseid.get(), tcoursename.get(1.0, END).replace("\n", "")))
                        messagebox.showinfo("SUCCESS", "Course added!")
                        conn.commit()
                        clear()
                        searchCourse()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("ERROR", "Course ID already in database!")


#========== UPDATE COURSE ==========#


        def updateCourse():
            if key.get() == "":
                messagebox.showerror("ERROR", "Choose a course.")
                return
            elif courseid.get() == "" or tcoursename.get(1.0, END) == "":
                messagebox.showerror("ERROR", "Please fill out all fields")
                return
            else:
                if messagebox.askyesno("Update Course", "Update course information?"):
                    try:
                        if key.get() != courseid.get():
                            c.execute("UPDATE courseinfo SET C_CODE=?, C_NAME=? WHERE C_CODE=?",
                                      (courseid.get(), tcoursename.get(1.0, END).replace("\n", ""), key.get()))
                        else:
                            c.execute("UPDATE courseinfo SET C_NAME=? WHERE C_CODE=?",
                                      (tcoursename.get(1.0, END).replace("\n", ""), courseid.get()))
                        conn.commit()
                        messagebox.showinfo("SUCCESS", "Course information updated!")
                        key.set("")
                        clear()
                        searchCourse()

                    except sqlite3.IntegrityError:
                        messagebox.showerror("ERROR", "Course ID already in database.")
                        return


#========== SEARCH COURSE ==========#


        def searchCourse():
            if schccode.get() == "":
                c.execute("SELECT * FROM courseinfo")
            else:
                c.execute("SELECT * FROM courseinfo WHERE C_CODE LIKE ?", ('%' + schccode.get() + '%',))
            courses = c.fetchall()
            coursetable.delete(*coursetable.get_children())
            if not courses:
                return
            else:
                for z in courses:
                    coursetable.insert('', END, values=(z[0], z[1]))


#========== DELETE COURSE ==========#


        def deleteCourse():
            selco = coursetable.focus()
            cont = coursetable.item(selco)
            rows = cont['values']
            if rows == "":
                messagebox.showerror("ERROR", "Select a course first!")
                return
            else:
                if messagebox.askyesno("Delete Course", "Confirm deletion of course?"):
                    c.execute("DELETE FROM courseinfo WHERE C_CODE=?", (rows[0],))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", "Course deleted!")
                    clear()
                    searchCourse()
                else:
                    return


#========== CLEAR AND SELECT COURSE ==========#


        def clear():
            courseid.set("")
            tcoursename.delete(1.0, END)

        def selectCourse(ev):
            sel_row = coursetable.focus()
            selco = coursetable.item(sel_row)
            rows = selco['values']
            clear()
            key.set(rows[0])
            courseid.set(rows[0])
            tcoursename.insert(END, rows[1])


#======================================== COURSE LIST FEATURES =======================================#


        headlabel.config(text="COURSE INFORMATION SYSTEM")
        displayroot.config(text="    LIST OF COURSES   ", fg="black")
        courseroot.place(x=10, width=450, y=120, height=360)
        
        lcourseid = Label(courseroot, text=" COURSE CODE", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        ecourseid = Entry(courseroot, textvariable=courseid, font=("Arial", 12, "bold"))
        
        lcoursename = Label(courseroot, text=" COURSE NAME", fg="white", bg="violet", font=("Arial", 12, "bold"), anchor="w")
        tcoursename = Text(courseroot, font=("Arial", 12, "bold"))
        
        lcourseid.place(x=10, y=20, width=150, height=35)
        ecourseid.place(x=160, y=20, width=270, height=35)
        lcoursename.place(x=10, y=60, width=150, height=35)
        tcoursename.place(x=10, y=95, width=420, height=160)
        coursebutton.place_forget()
        studentroot.place_forget()
        studbutton.place(x=425, y=520, width=150, height=50)

        addbut = Button(courseroot, text="ADD", command=addCourse, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        updbut = Button(courseroot, text="UPDATE", command=updateCourse, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        delbut = Button(courseroot, text="DELETE", command=deleteCourse, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        clearbut = Button(courseroot, text="CLEAR", command=clear, font=("Arial", 14, "bold"), bg="violet", fg="white", activebackground="gold", activeforeground="black")
        addbut.place(x=25, y=270, width=90, height=35)
        updbut.place(x=125, y=270, width=90, height=35)
        delbut.place(x=225, y=270, width=90, height=35)
        clearbut.place(x=325, y=270, width=90, height=35)

        studlist.place_forget()
        coursetable.pack_forget()
        cy.pack_forget()
        courselist.place(x=5, y=65, height=300, width=710)
        slabel.config(text="Course ID: ", bg="violet")
        searchid.place_forget()
        searchcode.place(x=100, y=15, height=30, width=200)
        
        searchbut = Button(displayroot, text="SEARCH", command=searchCourse, relief=FLAT, font=("Arial", 12, "bold"), bg="violet", fg="white", activeforeground="violet", activebackground="white")
        searchbut.place(x=305, height=30, y=15, width=80)
        refreshbut = Button(displayroot, text="VIEW ALL", command=lambda: [schccode.set(""), searchCourse()], relief=FLAT, font=("Arial", 12, "bold"), bg="violet", fg="white", activeforeground="violet", activebackground="white")
        refreshbut.place(x=390, height=30, y=15, width=80)

        cy.pack(side=RIGHT, fill=Y)
        cy.config(command=coursetable.yview)
        coursetable.heading("course_code", text="COURSE CODE")
        coursetable.heading("course_name", text="COURSE NAME")
        coursetable['show'] = 'headings'
        
        coursetable.column("course_code", width=200, anchor="center")
        coursetable.column("course_name", width=485)
        coursetable.pack(fill=BOTH, expand=1)
        coursetable.bind("<ButtonRelease-1>", selectCourse)

        schccode.set("")
        clear()
        searchCourse()




#======================================== EXIT =======================================#


    def toexit():
        if messagebox.askyesno("EXIT", "Do you want to exit?"):
            top.destroy()
        else:
            return

#========== BUTTONS ==========#

    studbutton = Button(command=student, text="STUDENTS", fg="black", bg="pink", font=("Arial", 18, "bold"), activebackground="white", activeforeground="black")
    coursebutton = Button(command=course, text="COURSES", fg="black", bg="pink", font=("Arial", 18, "bold"), activebackground="white", activeforeground="black")
    exitbutton = Button(text="EXIT", command=toexit, fg="black", bg="pink", font=("Arial", 18, "bold"), activebackground="white", activeforeground="black")
    exitbutton.place(x=625, width=150, y=520, height=50)
    student()
    
    root.protocol("WM_DELETE_WINDOW", toexit)


ob = SSIS(top)
top.mainloop()


#========== END ==========#