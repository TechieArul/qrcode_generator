from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog,scrolledtext,messagebox
import qrcode,os,subprocess


qrhome = Tk()
qrhome.configure(bg="#585858")

#window Settings ----------------------------------------------------------------------

qrhome.iconbitmap("qricon.ico")

#assign window size
user_screen_width=1366
user_screen_height=768

my_window_width = user_screen_width-100
my_window_height = user_screen_height-100

x=(user_screen_width/2)-(my_window_width/2)
y=(user_screen_height/2)-(my_window_height/2)
qrhome.geometry("%dx%d+%d+%d" % (my_window_width,my_window_height,x,y))

qrhome.resizable(False,False)#disable maximize button
qrhome.title("QR Code Generator - Arul's Intelligent Softwares")#window name
#window Settings ----------------------------------------------------------------------

#Variables Session--------------------------------------------------------------------
bg_color = "#585858"
fg_color = "#b570ff"
light_bg_color = "#656565"


user_option = StringVar()
user_option.set("text")
current_selcted_button = "text"

temp_path = subprocess.check_output("echo %temp%",shell=True).decode()



#Variables Session--------------------------------------------------------------------

#function session----------------------------------------------------------------------

clicked_button_list = ["url","sms","text"]
qr_temp_name = "tempmyqr.png"

def exit_func():
    user_exit = messagebox.askyesno(title="Exit QR Code Generator",message="Do You Want To Exit ?")
    if user_exit:
        try:
            os.system('del "'+qr_temp_name+'"')
            qrhome.destroy()
        except:
            qrhome.destroy()

def get_user_dir(raw_dir):
    raw_dir=raw_dir.split("/")
    raw_dir.pop(-1)
    t_dir=""
    for i in raw_dir:
        t_dir+=i+"\\"
    return t_dir

def update_qr():
    new_qr_show = Image.open(qr_temp_name)
    new_qr_show=new_qr_show.resize((200,200))
    new_qr_show=ImageTk.PhotoImage(new_qr_show)
    qr_code_image.configure(image=new_qr_show)
    qr_code_image.image=new_qr_show

def save_qr_code():
    try:
        user_path_and_file_name = filedialog.asksaveasfile(title="Save QR Code",filetypes=(("PNG Files","*.png"),("JPG Files","*.jpg")),mode="w",defaultextension=".png").name
        directory_path = get_user_dir(user_path_and_file_name)
        
        f=open(qr_temp_name,"rb")
        temp_file_read = f.read()
        f.close()

        os.chdir(directory_path)
        w=open(user_path_and_file_name,"wb")
        w.write(temp_file_read)
        w.close()
        os.chdir(temp_path[:-2])

    except:pass
    


#global qr generator func
def generate_global_qr_code(qrdatas):
    qr_code_button.configure(state="normal")
    
    os.chdir(temp_path[:-2])

    if qrdatas[0]=="text" or qrdatas[0]=="url":
        text_qr_text_required = qrdatas[1]
        global gen_qr
        gen_qr = qrcode.make(text_qr_text_required)
        gen_qr.save(qr_temp_name)


    elif qrdatas[0]=="contact":
        contact_name_required = qrdatas[1]
        contact_mobileno_required = qrdatas[2]
        contact_template = f"BEGIN:VCARD\nVERSION:3.0\nN:{contact_name_required}\nFN:{contact_name_required}\nTEL;CELL:{contact_mobileno_required}\nEND:VCARD"
        gen_qr = qrcode.make(contact_template)
        gen_qr.save(qr_temp_name)


    elif qrdatas[0]=="sms":
        sms_phno_required = qrdatas[1]
        sms_msg_required = qrdatas[2]
        sms_template = f"SMSTO:{sms_phno_required}:{sms_msg_required}"
        gen_qr = qrcode.make(sms_template)
        gen_qr.save(qr_temp_name)

    elif qrdatas[0]=="wifi":
        wifi_ssid_required = qrdatas[1]
        wifi_password_required = qrdatas[2]
        wifi_template = f"WIFI:T:WPA;S:{wifi_ssid_required};P:{wifi_password_required};H:false;;"
        gen_qr = qrcode.make(wifi_template)
        gen_qr.save(qr_temp_name)

    elif qrdatas[0]=="phcall":
        phcall_mobileno_required = qrdatas[1]
        phcall_template = f"tel:{phcall_mobileno_required}"
        gen_qr = qrcode.make(phcall_template)
        gen_qr.save(qr_temp_name)
    
    update_qr()

#generate qr button
def generate_button():

    if current_selcted_button=="text":
        #error detection
        text_input_data = text_qr_input_entry.get("1.0",END)
        if text_input_data=="\n":
            messagebox.showerror("Input Error","Please Provide The Text !")
        else:
            generate_global_qr_code(["text",text_input_data])

    elif current_selcted_button=="url":
        url_input_data = url_qr_input_entry.get("1.0",END)
        #error detection
        if url_input_data=="\n":
            messagebox.showerror("Input Error","Please Provide Proper URL Link !")   

        else:
            generate_global_qr_code(["url",url_input_data])

    elif current_selcted_button=="contact":
        contact_name_input_data = contact_qr_input_name_entry.get()
        contact_number_input_data = contact_qr_input_phno_entry.get()
        #error detection
        try:
            int(contact_number_input_data)
        except:
            messagebox.showerror("Input Error","Please Provide Valid Data !")
            return ""
        if contact_name_input_data=="" and contact_name_input_data=="":
            messagebox.showerror("Input Error","Please Provide Valid Data !")
        else:
            generate_global_qr_code(["contact",contact_name_input_data,contact_number_input_data])

    elif current_selcted_button=="sms":
        sms_phno_input_data = sms_qr_input_phno_entry.get()
        sms_msg_input_data = sms_qr_input_msg_entry.get("1.0",END)
        try:
            int(sms_phno_input_data)
        except:
            messagebox.showerror("Input Error","Please Provide Valid Data !")
            return ""
        generate_global_qr_code(["sms",sms_phno_input_data,sms_msg_input_data])
        
    elif current_selcted_button=="wifi":
        wifi_ssid_name_input_data = wifi_qr_input_name_entry.get()
        wifi_password_input_data = wifi_qr_input_password_entry.get()
        if wifi_ssid_name_input_data=="":
            messagebox.showerror("Input Error","Please Provide SSID/WIFI Name !")
        else:
            generate_global_qr_code(["wifi",wifi_ssid_name_input_data,wifi_password_input_data])

    elif current_selcted_button=="phcall":
        phcall_number_input_data = phcall_qr_input_number_entry.get()
        try:
            int(phcall_number_input_data)
        except:
            messagebox.showerror("Input Error","Please Provide Valid Data !")
            return ""
        generate_global_qr_code(["phcall",phcall_number_input_data])
        

def button_click_lisener(clicked_button):
    if clicked_button!=clicked_button_list[-1]:
        clicked_button_list.append(clicked_button)
        global current_selcted_button
        global old_selcted_button
        current_selcted_button =clicked_button_list[-1]
        old_selcted_button = clicked_button_list[-2]
        clicked_button_list.pop(0)

        frame_tittle.configure(text= myapp_buttons[current_selcted_button][2])
        myapp_buttons[current_selcted_button][0].configure(fg="#585858",bg="#b570ff")

        myapp_buttons[old_selcted_button][1].pack_forget()
        myapp_buttons[current_selcted_button][1].pack(fill="both",side=LEFT,expand=True)
        myapp_buttons[current_selcted_button][3].focus_set()
        
        myapp_buttons[old_selcted_button][0].configure(fg="#b570ff",bg="#585858")
    

    
#function session----------------------------------------------------------------------


#button and ui session-----------------------------------------------------------------

#frames and canvas
buttons_window = Frame(qrhome,pady=20,padx=20,bg="#585858",width=my_window_width,background=bg_color)#all button window frame
buttons_window.pack()

body_frame = Frame(qrhome,width=my_window_width,bg=bg_color,background=bg_color,highlightbackground=bg_color)#body frame
body_frame.pack(fill="both",expand=True)



text_qr_frame = Canvas(body_frame,bg=bg_color,width=my_window_width*0.8,background=bg_color,highlightbackground=bg_color)#text qr frame

url_qr_frame = Canvas(body_frame,bg=bg_color,background=bg_color,highlightbackground=bg_color)#url qr frame
contact_qr_frame = Canvas(body_frame,bg=bg_color,background=bg_color,highlightbackground=bg_color)#contact qr frame
sms_qr_frame = Canvas(body_frame,bg=bg_color,background=bg_color,highlightbackground=bg_color)#sms qr frame
wifi_qr_frame = Canvas(body_frame,bg=bg_color,background=bg_color,highlightbackground=bg_color)#wifi qr frame
phcall_qr_frame = Canvas(body_frame,bg=bg_color,background=bg_color,highlightbackground=bg_color)#email qr frame


qr_shower_frame = Canvas(body_frame,width=my_window_width*0.2,bg=bg_color,height=my_window_height,background=bg_color,highlightbackground=bg_color)#qrcode shower canvas

#---------------------------------------------------








text_qrcode = Button(buttons_window,text="Text   QR",font=("impact",15),padx=30,bg="#b570ff",fg="#585858",border=1,command=lambda:button_click_lisener("text"),activebackground=fg_color,activeforeground=bg_color)

url_qrcode = Button(buttons_window,text="URL   QR",font=("impact",15),padx=30,bg="#585858",fg="#b570ff",border=1,command=lambda:button_click_lisener("url"),activebackground=fg_color,activeforeground=bg_color)

save_contact_qrcode = Button(buttons_window,text="Save   Contact   QR",font=("impact",15),padx=30,bg="#585858",fg="#b570ff",border=1,command=lambda:button_click_lisener("contact"),activebackground=fg_color,activeforeground=bg_color)

sms_send_qrcode = Button(buttons_window,text="Send   SMS   QR",font=("impact",15),padx=30,bg="#585858",fg="#b570ff",border=1,command=lambda:button_click_lisener("sms"),activebackground=fg_color,activeforeground=bg_color)

wifi_qrcode = Button(buttons_window,text="Connect   WIFI   QR",font=("impact",15),padx=30,bg="#585858",fg="#b570ff",border=1,command=lambda:button_click_lisener("wifi"),activebackground=fg_color,activeforeground=bg_color)

phno_qrcode = Button(buttons_window,text="Ph   Call   QR",font=("impact",15),padx=30,bg="#585858",fg="#b570ff",border=1,command=lambda:button_click_lisener("phcall"),activebackground=fg_color,activeforeground=bg_color)



#button and ui session-----------------------------------------------------------------

#Packing session-------------------------------------------------------------------------------

text_qrcode.pack(side=LEFT)
space = Label(buttons_window,padx=15,bg="#585858").pack(side=LEFT)
url_qrcode.pack(side=LEFT)
space = Label(buttons_window,padx=15,bg="#585858").pack(side=LEFT)
save_contact_qrcode.pack(side=LEFT)
space = Label(buttons_window,padx=15,bg="#585858").pack(side=LEFT)
sms_send_qrcode.pack(side=LEFT)
space = Label(buttons_window,padx=15,bg="#585858").pack(side=LEFT)
wifi_qrcode.pack(side=LEFT)
space = Label(buttons_window,padx=15,bg="#585858").pack(side=LEFT)
phno_qrcode.pack(side=LEFT)


#Packing session-------------------------------------------------------------------------------



#text qr ui design----------------------------------------------------------------------

text_qr_input_label = Label(text_qr_frame,text="Enter   Texts : ",font=("impact",18),bg=bg_color,fg=fg_color)
text_qr_input_label.place(x=100,y=100)

text_qr_input_entry = scrolledtext.ScrolledText(text_qr_frame,width=50,height=7,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
text_qr_input_entry.place(x=100,y=150)
text_qr_input_entry.insert(INSERT,"// Welcome To Arul's Intelligent Softwares !")
text_qr_input_entry.focus_set()

#text qr ui design----------------------------------------------------------------------

#url qr ui design----------------------------------------------------------------------

url_qr_input_label = Label(url_qr_frame,text="Enter   a   URL   Link : ",font=("impact",18),bg=bg_color,fg=fg_color)
url_qr_input_label.place(x=100,y=100)
url_qr_input_entry = scrolledtext.ScrolledText(url_qr_frame,width=50,height=7,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
url_qr_input_entry.place(x=100,y=150)

#url qr ui design----------------------------------------------------------------------

#contact qr ui design----------------------------------------------------------------------

contact_qr_input_label = Label(contact_qr_frame,text="Enter   Contact   Name : ",font=("impact",18),bg=bg_color,fg=fg_color)
contact_qr_input_label.place(x=100,y=100)
contact_qr_input_name_entry = Entry(contact_qr_frame,width=30,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
contact_qr_input_name_entry.place(x=100,y=150)

contact_qr_input_phno_label = Label(contact_qr_frame,text="Enter   Phone   No : ",font=("impact",18),bg=bg_color,fg=fg_color)
contact_qr_input_phno_label.place(x=100,y=250)
contact_qr_input_phno_entry = Entry(contact_qr_frame,width=30,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
contact_qr_input_phno_entry.place(x=100,y=300)

#contact qr ui design----------------------------------------------------------------------

#sms qr ui design----------------------------------------------------------------------

sms_qr_input_label = Label(sms_qr_frame,text="Enter   Phone   No : ",font=("impact",18),bg=bg_color,fg=fg_color)
sms_qr_input_label.place(x=100,y=50)
sms_qr_input_phno_entry = Entry(sms_qr_frame,width=30,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
sms_qr_input_phno_entry.place(x=100,y=100)

sms_qr_input_msg_label = Label(sms_qr_frame,text="Enter   Message   : ",font=("impact",18),bg=bg_color,fg=fg_color)
sms_qr_input_msg_label.place(x=100,y=200)
sms_qr_input_msg_entry = scrolledtext.ScrolledText(sms_qr_frame,width=50,height=5,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
sms_qr_input_msg_entry.place(x=100,y=250)

#sms qr ui design----------------------------------------------------------------------

#wifi qr ui design----------------------------------------------------------------------

wifi_qr_input_label = Label(wifi_qr_frame,text="Enter   Wifi   NetWork   Name   : ",font=("impact",18),bg=bg_color,fg=fg_color)
wifi_qr_input_label.place(x=100,y=100)
wifi_qr_input_name_entry = Entry(wifi_qr_frame,width=30,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
wifi_qr_input_name_entry.place(x=100,y=150)

wifi_qr_input_password_label = Label(wifi_qr_frame,text="Enter   Wifi   NetWork   Password   : ",font=("impact",18),bg=bg_color,fg=fg_color)
wifi_qr_input_password_label.place(x=100,y=250)
wifi_qr_input_password_entry = Entry(wifi_qr_frame,width=30,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
wifi_qr_input_password_entry.place(x=100,y=300)

#wifi qr ui design----------------------------------------------------------------------

#phcall qr ui design----------------------------------------------------------------------

phcall_qr_input_label = Label(phcall_qr_frame,text="Enter   Phone   Number   : ",font=("impact",18),bg=bg_color,fg=fg_color)
phcall_qr_input_label.place(x=100,y=100)
phcall_qr_input_number_entry = Entry(phcall_qr_frame,width=30,font=("segoe ui",15,"bold"),bg=light_bg_color,fg="white")
phcall_qr_input_number_entry.place(x=100,y=150)

#phcall qr ui design----------------------------------------------------------------------

#qr display frame-------------------------------------------------------------------------

img = Image.open("startup_qr.png")
img=img.resize((200,200))
img=ImageTk.PhotoImage(img)
qr_code_image = Label(qr_shower_frame,image=img,borderwidth=3,relief=RIDGE,)
qr_code_image.place(x=25,y=25)

qr_code_button = Button(qr_shower_frame,text="Save   QR   Code",font=("impact",15),padx=30,bg="#585858",fg=fg_color,border=1,activebackground=fg_color,activeforeground=bg_color,command=save_qr_code,state="disabled")
qr_code_button.place(x=36,y=400)




#qr display frame-------------------------------------------------------------------------


#auto runner----------------------------------------------------------------------------------

myapp_buttons = {"text":[text_qrcode,text_qr_frame,"T E X T      Q R      C O D E      G E N E R A T O R",text_qr_input_entry],
                "sms":[sms_send_qrcode,sms_qr_frame,"S M S       Q R       C O D E       G E N E R A T O R",sms_qr_input_phno_entry],
                "url":[url_qrcode,url_qr_frame,"U R L       Q R       C O D E       G E N E R A T O R",url_qr_input_entry],
                "phcall":[phno_qrcode,phcall_qr_frame,"P H O N E       C A L L       Q R       C O D E       G E N E R A T O R",phcall_qr_input_number_entry],
                "contact":[save_contact_qrcode,contact_qr_frame,"C O N T A C T       Q R       C O D E       G E N E R A T O R",contact_qr_input_name_entry],
                "wifi":[wifi_qrcode,wifi_qr_frame,"W I F I       Q R       C O D E       G E N E R A T O R",wifi_qr_input_name_entry]}


frame_tittle = Label(body_frame,text=myapp_buttons[current_selcted_button][2],bg="#656565",fg="#b570ff",font=("Impact",15),height=1,width=my_window_height)
frame_tittle.pack()
qr_genrate_button = Button(body_frame,text="Generate QR",height=0,width=12,bg=bg_color,fg="green2",font=("segoe ui",13,"bold"),command=generate_button)
qr_genrate_button.pack(side=BOTTOM,pady=10)

text_qr_frame.pack(fill="both",side=LEFT,expand=True)
qr_shower_frame.pack(side=RIGHT)
#auto runner----------------------------------------------------------------------------------

qrhome.protocol("WM_DELETE_WINDOW",exit_func)
qrhome.mainloop()
