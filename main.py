print("Starting...\nIt wil take a minute")
from tkinter import font
from pywhatkit import text_to_handwriting
from tkinter import *  
from tkinter import filedialog as fd, colorchooser, messagebox as tmsg
import smtplib
import pyautogui as pg
from time import sleep
import sys
import webbrowser
from platform import system
import screen_brightness_control as sbc
import datetime
from tkinter.ttk import *

# print(sys.getrecursionlimit())
sys.setrecursionlimit(1500)

class Appwindow(Tk):
        def __init__(self):
            super().__init__()
            self.geometry('1000x600+194+51')  #+194+51
            self.title('Untiteled - Text to handwritting coverter')
            self.focus_force()
            self.style = Style(self)
        
        # Textvariables
            self.hs = IntVar()
            self.hs.set(1)
            self.nifgtmode_var = IntVar()
            self.theme_var = StringVar()
            self.size_var = IntVar(value=10)

        # self.Text_input
            self.fsize = self.size_var.get()
            self.label = Label(self, text="Enter your text",font="lucida 18 underline bold",borderwidth=0)
            self.label.pack(side=TOP)
            self.scrollbar = Scrollbar(self)
            self.scrollbar.pack(side=RIGHT, fill=Y)
            self.Text_input = Text(self, yscrollcommand = self.scrollbar.set,undo=True,font=self.fsize)
            self.Text_input.pack(fill=BOTH,expand=True)
            self.scrollbar.config(command=self.Text_input.yview)    
   
        # MenuBars
            self.mainmenu = Menu(self)
                        
            self.file_menu = Menu(self.mainmenu, tearoff=0)
            self.file_menu.add_command(label="Open file                    Ctrl+O", command=self.open_file)
            self.file_menu.add_separator()  
            self.file_menu.add_command(label="Save                            Ctrl+S", command= lambda : self.save(event=None))
            self.file_menu.add_command(label="Save as                       Ctrl+Shit+S", command= lambda : self.saveas(event=None))
            self.file_menu.add_separator()   
            self.file_menu.add_command(label="New                            Ctrl+N",command=self.new)
            self.file_menu.add_command(label="New Window            Ctrl+Shift+N",command=Appwindow)
            self.file_menu.add_separator()
            self.menu_recent = Menu(self.file_menu)
            self.file_menu.add_cascade(menu=self.menu_recent, label='Open Recent')
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Exit                               Escape",command=lambda: self.destroy())
            self.file_menu.add_command(label="Close                            Escape",command=lambda: self.destroy())
            self.config(menu=self.mainmenu)
            self.mainmenu.add_cascade(label="File", menu=self.file_menu)

            self.edit_menu = Menu(self.mainmenu,tearoff=0)
            self.edit_menu.add_command(label="Choose font colour and save", command=self.cfc)
            self.edit_menu.add_command(label="Clear              Ctrl+Alt+C", command= self.clear)
            self.edit_menu.add_separator()
            self.edit_menu.add_command(label="Cut                 Ctrl+X", command= lambda: pg.hotkey("ctrl","x"))
            self.edit_menu.add_command(label="Copy               Ctrl+C", command= lambda: pg.hotkey("ctrl","c"))
            self.edit_menu.add_command(label="Paste               Ctrl+V", command= lambda: pg.hotkey("ctrl","v"))
            self.edit_menu.add_command(label="Select all          Ctrl+A", command= lambda: pg.hotkey("ctrl","a"))
            self.edit_menu.add_command(label="Delete               Del", command= lambda: pg.hotkey("del"))
            self.edit_menu.add_separator()
            self.edit_menu.add_command(label="Find                  Ctrl+F", command= self.find)
            self.edit_menu.add_separator()
            self.edit_menu.add_command(label="Undo                Ctrl+Z",command= self.Text_input.edit_undo)
            self.edit_menu.add_command(label="Redo                 Ctrl+Y",command= self.Text_input.edit_redo)
            self.edit_menu.add_separator()
            self.edit_menu.add_command(label="Date/Time               F5",command= self.insert_datetime)
            self.config(menu=self.mainmenu)
            self.mainmenu.add_cascade(label="Edit", menu=self.edit_menu)
            self.format_menu = Menu(self.mainmenu,tearoff=0)
            self.format_menu.add_checkbutton(label="Word wrap", command= lambda : self.Text_input.config(wrap=WORD))
            self.mainmenu.add_cascade(label="Format", menu=self.format_menu)
        
            self.view_menu = Menu(self.mainmenu,tearoff=0)
            self.view_menu.add_checkbutton(label="Status bar    ", onvalue=1,offvalue=0,variable=self.hs,command=self.hs_statusbar)
            self.view_menu.add_command(label="Fullscreen        ",command=self.fullscreen)
            self.mainmenu.add_cascade(label="View", menu=self.view_menu)

            self.menu_zoom = Menu(self.view_menu,tearoff=0)
            self.menu_zoom.add_command(label='Zoom in                    Ctrl+plus',command=self.zoomin)
            self.menu_zoom.add_command(label='Zoom out                   Ctrl+plus',command=self.zoomout)
            self.menu_zoom.add_command(label='Restore default zoom         Ctrl+0',command=self.reset)
            self.view_menu.add_cascade(menu=self.menu_zoom, label='Zoom')

            self.theme_menu = Menu(self.mainmenu,tearoff=0)
            for self.theme_name in self.style.theme_names():
                 self.theme_menu.add_radiobutton(label=self.theme_name,variable=self.theme_var,value=self.theme_name,command=self.change_theme)                                                                                   
            self.theme_menu.add_command(label="more Themes",command=self.nextupdate)  #More themes are awailable please check on web
            self.mainmenu.add_cascade(label="Theme", menu=self.theme_menu)        

            self.option_menu = Menu(self.mainmenu,tearoff=0)
            self.option_menu.add_command(label="Survey",command=lambda : webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSe9FW90ZYxmEQOTBt-V4bTpiK26CK77mXVH3Cn0MwWrhCcbvg/viewform?usp=sf_link"))
            self.option_menu.add_checkbutton(label="Night mode", onvalue=1,offvalue=0,variable=self.nifgtmode_var,command=self.nightmode)
            self.mainmenu.add_cascade(label="Options", menu=self.option_menu)

            self.help_menu = Menu(self.mainmenu,tearoff=0)
            self.help_menu.add_command(label="Contact us", command=self.qrcode)
            self.help_menu.add_separator()
            self.help_menu.add_command(label="feedback", command=self.feedback)
            self.help_menu.add_separator()
            self.help_menu.add_command(label="Help", command=lambda: tmsg.showinfo('Help',"To save file click save and file save in 'C:\Handritting converter'.fore more help contact us or email."))
            self.help_menu.add_command(label="About", command=lambda: tmsg.showinfo("About","This apllication is made by Krishna."))
            self.config(menu=self.mainmenu)
            self.mainmenu.add_cascade(label="Help", menu=self.help_menu)

        # Status bar
            self.statusbar_frame = Frame(self,borderwidth=1,relief=SUNKEN)
            self.statusbar_frame.pack(side=BOTTOM, fill=X)
            self.statusvar = StringVar()
            self.statusvar.set("Ready ")
            self.sbar = Label(self.statusbar_frame, textvariable=self.statusvar, anchor="w",borderwidth=0)
            self.sbar.pack(side=LEFT)
            self.inlabel = StringVar()
            self.u_label = Label(self.statusbar_frame,text="UTF-8", anchor="w",borderwidth=0)
            self.u_label.pack(side=RIGHT,padx=7)
            self.w_label = Label(self.statusbar_frame,text=f"{system()}(CRLF)", anchor="w",borderwidth=0)
            self.w_label.pack(side=RIGHT,padx=7)            
            self.fontsize_label = Label(self.statusbar_frame,text="100%", anchor="w",borderwidth=0)
            self.fontsize_label.pack(side=RIGHT,padx=7)
            self.curosor_label = Label(self.statusbar_frame,textvariable=self.inlabel, anchor="w",borderwidth=0)
            self.curosor_label.pack(side=RIGHT,padx=7)
            self.rowcol() 

        # Key Binndings
            self.Text_input.bind("<Control-s>",self.save)
            self.Text_input.bind("<Control-Shift-s>",self.saveas)
            self.Text_input.bind("<Control-o>",self.open_file)
            self.Text_input.bind("<Control-n>",self.new)
            self.Text_input.bind("<Control-a>",lambda e: pg.hotkey("ctrl","a"))
            self.Text_input.bind("<Control-Shift-n>",Appwindow)
            self.Text_input.bind("<Control-F2>",self.clear)
            self.Text_input.bind("<Control-f>",self.find)
            self.Text_input.bind("<KeyPress>", self.keydown)
            self.Text_input.bind("<KeyRelease>", self.keyup)
            self.Text_input.bind("<F5>", self.insert_datetime)
            self.Text_input.bind("<Button-1>", self.rowcol)
            self.Text_input.bind("<Escape>",lambda e: self.destroy())    

        def zoomin(self,event=None):
                a = self.fsize + 2
                self.size_var.set(a)
                self.Text_input.config(font=a)
                

        def zoomout(self,event=None):
                size = self.size_var.get()
                size -= 2
                self.size_var.set(size)
                self.Text_input.config(font=size)
                self.Text_input.update()

        def reset(self,event=None):
                pass

        def nextupdate(self):
                tmsg.showwarning("Themes","More themes are not awailaible")
                tmsg.showinfo("Update","More themes are comming soon in next update")

        def insert_datetime(self,event=None):
                timedate  = datetime.datetime.now().strftime("%d-%m-%y %I:%M %p")
                self.Text_input.insert(INSERT,timedate)

        def change_theme(self):
                self.style.theme_use(self.theme_var.get())
                print("Theme changed")
                # self.update()
                # self.update_idletasks()
                
        def rowcol(self ,event = None ):
                self.r, self.c = self.Text_input.index( 'insert' ).split( '.' )
                self.inlabel.set(f'Ln {self.r}, Col {self.c}')
                self.update_idletasks()

        def nightmode(self):
                v = self.nifgtmode_var.get()
                if v == 1:
                        sbc.set_brightness(25)
                        self.Text_input.config(bg="#322624",fg="white",insertbackground="white")
                        self.config(bg="#322624")
                        self.mainmenu.config(bg="#322624",fg="white")
                        self.file_menu.config(bg="#322624",fg="white")
                        self.edit_menu.config(bg="#322624",fg="white")
                        self.option_menu.config(bg="#322624",fg="white")
                        self.view_menu.config(bg="#322624",fg="white")
                        self.help_menu.config(bg="#322624",fg="white")
                        self.format_menu.config(bg="#322624",fg="white")
                        self.label.config(bg="#322624",fg="white")
                else:
                        sbc.set_brightness(50)
                        self.Text_input.config(bg="white",fg="black",insertbackground="black")
                        self.config(bg="white")
                        self.mainmenu.config(bg="white",fg="black")
                        self.file_menu.config(bg="white",fg="black")
                        self.edit_menu.config(bg="white",fg="black")
                        self.option_menu.config(bg="white",fg="black")
                        self.view_menu.config(bg="white",fg="black")
                        self.help_menu.config(bg="white",fg="black")
                        self.format_menu.config(bg="white",fg="black")
                        self.label.config(bg="white",fg="black")
                
        def fullscreen(self):
                self.view_menu.entryconfigure(2, label="Exit fullscreen",command=self.exit_fullscreen)
                self.attributes("-fullscreen",True)

        def exit_fullscreen(self):
                self.view_menu.entryconfigure(2, label="Fullscreen",command=self.fullscreen)
                self.attributes("-fullscreen",False)

        def hs_statusbar(self):
                v = self.hs.get()
                if v == 1:
                        self.statusbar_frame.pack(side=BOTTOM, fill=X)
                else:
                        self.statusbar_frame.pack_forget()

        def find(self,event=None):
                root = Toplevel(self)
                fram = Frame(root)
                edit = Entry(fram)
                edit.pack(side=LEFT, fill=BOTH, expand=1)
                edit.focus_set()
                butt = Button(fram, text='Find') 
                butt.pack(side=RIGHT)
                fram.pack(side=TOP)

                def find(e=None):               
                        #remove tag 'found' from index 1 to END
                        self.Text_input.tag_remove('found', '1.0', END)
                        
                        #returns to widget currently in focus
                        s = edit.get()
                        if s:
                                self.idx = '1.0'
                                while 1:
                                        #searches for desired string from index 1
                                        self.idx = self.Text_input.search(s, self.idx, nocase=1,
                                                        stopindex=END)
                                        if not self.idx: break
                                        
                                        #last index sum of current index and
                                        #length of text
                                        self.lastidx = '%s+%dc' % (self.idx, len(s))
                                        
                                        #overwrite 'Found' at self.idx
                                        self.Text_input.tag_add('found', self.idx, self.lastidx)
                                        self.idx = self.lastidx
                                        
                                        #mark located string as red
                                        self.Text_input.tag_config('found', foreground='red')
                
                edit.focus_set()
                butt.config(command=find)
                edit.bind("<KeyPress>",find)
                root.mainloop()

        def clear(self,event=None):
                cl = self.Text_input.delete("1.0",END)

        def qrcode(self):
                window = Toplevel()
                window.geometry('500x400')
                window.title('Qr code generater')

                Label(window,text="Scan qr code and contact with us.",font="Calibri 25 bold").pack(side=TOP)

                photo = PhotoImage(window,file="myqr.png")
                label = Label(image=photo)
                label.pack()

                window.mainloop()

        def sendEmail(self,id,password,to,sub,content):
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(id, password)
                server.sendmail(id, to, f"Subject: {sub}\n\n{content}")
                server.close()

        def process(self):
                try:
                        id = idvar.get()
                        password = passvar.get()
                        sub = self.Text_input.get()     
                        content = "Test"
                        to = "naitiksinghal679@gmail.com"
                        self.sendEmail(id,password,to,sub,content)
                        tmsg.showinfo("Feedback","Your feedback has been sent.")
                except smtplib.SMTPServerDisconnected:
                         tmsg.showerror("Eror","Unable to connect to the Internet. Please check your internet connection.")
                except smtplib.SMTPConnectError:
                        tmsg.showerror("Eror","Unable to connect to the Internet. Please check your internet connection.")
                except smtplib.SMTPAuthenticationError:
                        tmsg.showerror("Erorr","Invalid Id or password.Please enter valid details")
                except Exception as e:
                        tmsg.showerror("error","Unaible to send.")
                        print(e) 

        def mainentry(self):
                feedwindow = Toplevel()
                feedwindow.geometry('500x230')
                feedwindow.title('Login')
                global idvar,passvar
                idvar = StringVar()
                passvar = StringVar()
                f1 = Frame(feedwindow)
                f2 = Frame(feedwindow)
                f1.pack(pady=6,anchor="w")
                f2.pack(pady=6,anchor="w")

                Label(f1,text="Enter you gmail id-",font="lucida 15 bold").pack(anchor="w")
                Identry = Entry(f1,textvariable=idvar,width=32,font="lucida 20",bd=2,relief=SUNKEN).pack(anchor="w")

                Label(f2,text="Enter you gmail id password",font="lucida 15 bold").pack(anchor="w")
                Passwordentry = Entry(f2,textvariable=passvar,width=32,font="lucida 20",bd=2,relief=SUNKEN).pack(anchor="w")

                Button(feedwindow,text="Submit",font="lucida 12",padx=5,command=self.process).pack(anchor="se")

                Label(feedwindow, text="Note:-We do not save your accont details you can trust us!",font="lucida 8",fg="red").pack(side=BOTTOM)
                feedwindow.mainloop()

        def feedback(self):
                self.statusvar.set("Busy..")
                self.sbar.update()
                sleep(10)
                self.master = Toplevel()
                self.master.geometry("800x600")
                self.master.title("Feedback")
                self.Label(self.master,text="Enter your feedback",font="lucida 20 bold").pack(side=TOP)
                self.self.Text_input = Text(self)  
                self.self.Text_input.pack(fill=BOTH)
                self.sendbutton = Button(self.master,text="Send",borderwidth=5,relief=SUNKEN,command=self.mainentry)
                self.sendbutton.pack(anchor="e")

        def open_file(self,event=None):                
                self.file = fd.askopenfile(mode="r",filetype=[("Text file","*.txt")])
                self.filename = self.file
                self.Text_input.insert('END',self.filename)
                self.title(f"{self.filename} - Text to handwritting coverter")

        def cfc(self):
                tmsg.showerror("Error","Soory, this feature maybe not working correctly please wait for the next update maybe it will be repair.")

                # choosecolor = colorchooser.askcolor(title="Choose Color")

                # savfilename = "Handwritting.png"
                # loc = fd.asksaveasfilename(filetypes = [("All files","*."),("Png files","*.png"),("Jpg files","*.jpg")],defaultextension = savfilename)
                # inp = self.Text_input.get("1.0",END)
                # text_to_handwriting("Handwritting",loc,rgb=choosecolor)  

        def saveas(self,event=None):
                self.loc = fd.asksaveasfilename(filetypes=[("Png file","*.png"),("Jpg file","*.jpg"),("All files","*.")],defaultextension=".png")
                self.inp = self.Text_input.get("1.0",END)
                text_to_handwriting(self.inp,self.loc) 
                tmsg.showinfo("Saved",f"You image succesfully saved in {self.inp}")

        def save(self,event=None):
                import os,random,string
                self.s1 = string.ascii_lowercase
                self.s2 = string.ascii_uppercase
                self.s3 = string.digits
                self.s4 = string.punctuation
                self.s = []
                self.s.extend(list(self.s1))
                self.s.extend(list(self.s2))
                self.s.extend(list(self.s3))
                self.s.extend(list(self.s4))
                self.a = ("".join(random.sample(self.s, 6)))
                self.inp = self.Text_input.get("1.0",END)
                self.saved_file_name = f"C:\Handritting converter\{self.a}.png"

                if not os.path.exists("C:\\Handritting converter"):
                        os.makedirs('C:\\Handritting converter')

                text_to_handwriting(self.inp,self.saved_file_name)  
                self.title(f"{self.saved_file_name} - Text to handwritting coverter")
                ask = tmsg.askquestion("Saved","Your image will be saved. You want to see it ?")
                if ask == "yes":
                        self.statusvar.set("Opening..")
                        self.sbar.update()
                        os.startfile(self.saved_file_name)
                        sleep(5)
                        self.statusvar.set("Opening..")
                        self.sbar.update()

        def new(self,event=None):
                self.clear()
                self.title('Untiteled - Text to handwritting coverter')
        
        def keyup(self,event=None):
                sleep(0.1)    
                self.statusvar.set("Ready")
                self.sbar.update()

        def keydown(self,event=None):
                self.rowcol()
                self.statusvar.set("Typing..")
                self.sbar.update()

if __name__ == '__main__':
        window = Appwindow()
        window.mainloop()
