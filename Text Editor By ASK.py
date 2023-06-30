from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog,messagebox
import os
import tempfile
from datetime import datetime


#-----------  Funtionality Section --------

def date_time(event=None):
    currentdatetime=datetime.now()
    formatteddatetime=currentdatetime.strftime('%b-%d-%y %H:%M:%S')
    textarea.insert(1.0,formatteddatetime)


def printout(event=None):
    file=tempfile.mktemp('.txt')
    open(file,'w').write(textarea.get(1.0,END))
    os.startfile(file,'print')


def change_theme(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color)

def toolbarFunc():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    if show_toolbar.get()==True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH,expand=1)

def statusbarFunc():
    if show_statusbar.get()==False:
        status_bar.pack_forget()
    else:
        status_bar.pack()


def statusBarFunction(event):
    # if textarea.edit_modified():
        words=len(textarea.get(0.0,END).split())
        characters=len(textarea.get(0.0,'end-1c').replace(' ','')) #1.0
        status_bar.config(text=f'Charecters: {characters} Words: {words}')

        textarea.edit_modified(False)


url=''
def new_file(event=None):
    global url
    url=''
    textarea.delete(0.0,END)

def open_file(event=None):
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title='Select File',filetypes=(('Text File','txt'),
                                                                                     ('All Files','*.*')))
    if url != '':
        data=open(url,'r')
        textarea.insert(0.0,data.read())
    root.title(os.path.basename(url))

def save_file(event=None):
    if url =='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),
                                                                             ('All Files','*.*')))
        if save_url is None:
            pass
        else:
            content=textarea.get(0.0,END)
            save_url.write(content)
            save_url.close()

    else:
        content=textarea.get(0.0,END)
        file=open(url,'w')
        file.write(content)

def saveas_file(event=None):
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                      ('All Files', '*.*')))

    content = textarea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url !='':
        os.remove(url)

def iexit(event=None):
    if textarea.edit_modified():
        result=messagebox.askyesnocancel('Warning','Do you want to save the file?')
        if result is True:
            if url!='':
                content=textarea.get(0.0,END)
                file=open(url,'w')
                file.write(content)
                root.destroy()
            else:
                content=textarea.get(0.0,END)
                save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                                  ('All Files', '*.*')))

                save_url.write(content)
                save_url.close()
                root.destroy()

        elif result is False:
            root.destroy()

        else:
            pass

    else:
        root.destroy()



fontSize=16
fontStyle='arial'
def font_style(event):
    global fontStyle
    fontStyle=font_family_variable.get()
    textarea.config(font=(fontStyle,fontSize))

def font_size(event):
    global fontSize
    fontSize=size_variable.get()
    textarea.config(font=(fontStyle,fontSize))

def bold_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['weight']=='normal':
        textarea.config(font=(fontStyle,fontSize,'bold'))

    if text_property['weight']=='bold':
        textarea.config(font=(fontStyle,fontSize,'normal'))

def italic_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['slant']=='roman':
        textarea.config(font=(fontStyle,fontSize,'italic'))

    if text_property['slant']=='italic':
        textarea.config(font=(fontStyle,fontSize,'roman'))

def underline_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['underline']==0:
        textarea.config(font=(fontStyle,fontSize,'underline'))

    if text_property['underline']==1:
        textarea.config(font=(fontStyle,fontSize,))

def color_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])


#------ Main Root (Main) window -------

root=Tk()
root.title('Text Editor')
root.geometry('1200x620')
root.iconbitmap('icon.ico')
root.resizable(False,False)
menubar=Menu(root)
root.config(menu=menubar)


#------- Toolbar section -------

tool_bar=Label(root)
tool_bar.pack(side=TOP,fill=X)
font_families=font.families()
font_family_variable=StringVar()
fontfamily_Combobox=Combobox(tool_bar,width=30,values=font_families,state='readonly',textvariable=font_family_variable)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0,column=0,padx=5)
size_variable=IntVar()
font_size_Combobox=Combobox(tool_bar,width=14,textvariable=size_variable,state='readonly',values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=1,padx=5)

fontfamily_Combobox.bind('<<ComboboxSelected>>',font_style)
font_size_Combobox.bind('<<ComboboxSelected>>',font_size)

#------------ Buttons Section -------------
boldImg=PhotoImage(file='bold.png')
boldBtn=Button(tool_bar,image=boldImg,command=bold_text)
boldBtn.grid(row=0,column=2,padx=5)

italicImg=PhotoImage(file='italic.png')
italicBtn=Button(tool_bar,image=italicImg,command=italic_text)
italicBtn.grid(row=0,column=3,padx=5)

underlineImg=PhotoImage(file='underline.png')
underlineButton=Button(tool_bar,image=underlineImg,command=underline_text)
underlineButton.grid(row=0,column=4,padx=5)

fontColorwheelImg=PhotoImage(file='color_wheel.png')
fontColorBtn=Button(tool_bar,image=fontColorwheelImg,command=color_select)
fontColorBtn.grid(row=0,column=5,padx=5)

scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)
textarea=Text(root,yscrollcommand=scrollbar.set,font=('arial',16),undo=True)
textarea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textarea.yview)

status_bar=Label(root,text='Status Bar')
status_bar.pack(side=BOTTOM)


textarea.bind('<<Modified>>',statusBarFunction)

editmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Edit',menu=editmenu)
editmenu.add_command(label='Undo',accelerator='Ctrl+Z')
editmenu.add_command(label='Cut',accelerator='Ctrl+X',command=lambda :textarea.event_generate('<Control x>'))
editmenu.add_command(label='Copy',accelerator='Ctrl+C',command=lambda :textarea.event_generate('<Control c>'))
editmenu.add_command(label='Paste',accelerator='Ctrl+V',command=lambda :textarea.event_generate('<Control v>'))

editmenu.add_command(label='Select All',accelerator='Ctrl+A')

editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',command=lambda :textarea.delete(0.0,END))
editmenu.add_command(label='Time/Date',accelerator='Ctrl+D',command=date_time)
menubar.add_cascade(label='Edit',menu=editmenu)

#----------- View Menu Section  -------------
show_toolbar=BooleanVar()
show_statusbar=BooleanVar()
viewmenu=Menu(menubar,tearoff=False)
viewmenu.add_checkbutton(label='Tool Bar',variable=show_toolbar,onvalue=True,offvalue=False,command=toolbarFunc)
show_toolbar.set(True)
viewmenu.add_checkbutton(label='Status Bar',variable=show_statusbar,onvalue=True,offvalue=False,command=statusbarFunc)
show_statusbar.set(True)
menubar.add_cascade(label='View',menu=viewmenu)

#----------- Themes Menu Section ---------
themesmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Themes',menu=themesmenu)
theme_choice=StringVar()
themesmenu.add_radiobutton(label='Light Default',variable=theme_choice,compound=LEFT
                           ,command=lambda :change_theme('white','black'))
themesmenu.add_radiobutton(label='Dark',variable=theme_choice,compound=LEFT
                           ,command=lambda :change_theme('gray20','white'))
themesmenu.add_radiobutton(label='Pink',variable=theme_choice,compound=LEFT
                           ,command=lambda :change_theme('pink','blue'))


root.bind("<Control-o>",open_file)
root.bind("<Control-n>",new_file)
root.bind("<Control-s>",save_file)
root.bind("<Control-Alt-s>",saveas_file)
root.bind("<Control-q>",iexit)
root.bind("<Control-p>",printout)
root.bind("<Control-d>",date_time)

root.mainloop()