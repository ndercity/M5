import customtkinter as ctk
from logic import RFID_Logic, AppState
from PIL import Image
#import pywinstyles as #pws

class AppUI:
    def __init__(self, root): 
        self.root = root
        self.state = AppState()
        #self.logic = RFID_Logic()
        self.root.title("Pic-a-Pi RFID")
        self.root.geometry("800x480")
        
        self.container = ctk.CTkFrame(self.root)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {} #container ito ng page states
        for PageClass in (HomePage, ScanPage, OperationsPage, CompeleteOperation):
            page_name = PageClass.__name__
            frame = PageClass(self.container, self, self.state)
            self.pages[page_name] = frame
            frame.grid(row= 0, column = 0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()
        if hasattr (frame, "refresh"):
            frame.refresh()
        

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        super().__init__(parent)
        self.button_height = 60
        self.button_width = 200

        self.bg_image = ctk.CTkImage(light_image = Image.open('images/home_design.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.scan_button = ctk.CTkButton(self, height = self.button_height, width = self.button_width,
                                            text = "Scan RFID",
                                            text_color = "#000000",
                                            font = ("Helvetica", 15),
                                            #corner_radius = 20,
                                            fg_color = "#99FFD0",
                                            bg_color="transparent",
                                            border_color = "#FFFFFF",
                                            border_width=4,
                                            command=lambda: controller.show_page("ScanPage"))

        self.scan_button.place(x=(800/2) - 100, y=350)
        ##pws.set_opacity(self.scan_button, color="#000001")


class ScanPage(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        self.controller = controller
        self.state = state

        super().__init__(parent)

        self.bg_image = ctk.CTkImage(light_image = Image.open('images/scan_design.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0)

        self.bg_panel = ctk.CTkFrame(self, width=683, height=149,
                                     fg_color="#99FFD0", #corner_radius=20,
                                     border_color = "#FFFFFF", border_width=4,
                                     bg_color="transparent",)    
        self.bg_panel.place(x=(800/2) - (683/2), y=52)
        ##pws.set_opacity(self.bg_panel, color="#000001")

        self.scan_label = ctk.CTkLabel(self.bg_panel,
                                       text = "Scan the RFID in the scanner ",
                                       font = ("Helvetica", 30),
                                       text_color = "#000000")
        self.scan_label.place(relx=0.5, rely=0.5, anchor="center")

        self.rfid_image = ctk.CTkImage(light_image = Image.open('images/rfid_icon.png'), size = (167,129))
        self.bg_image_label = ctk.CTkLabel(self, image = self.rfid_image, text = "", bg_color="#000001")
        self.bg_image_label.place(x=(800/2) - (167/2), y=223)
        ##pws.set_opacity(self.bg_image_label, color="#000001")

        self.rfid_logic = RFID_Logic(self.on_rfid_scanned)

        self.back_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Back", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.go_back)
        self.back_button.place(x=(800/2) - (181/2), y=378)
        ##pws.set_opacity(self.back_button, color="#000001")

        #will delete this button
        self.x_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="next", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: controller.show_page("OperationsPage"))
        self.x_button.place(x=(800/2) - (181/2), y=400)
        #pws.set_opacity(self.x_button, color="#000001")

        self.rfid_logic = RFID_Logic(self.on_rfid_scanned)
        self.rfid_logic.turn_on_rfid()

    def on_rfid_scanned(self, rfid):
        self.state.set_rfid(rfid)
        self.rfid_logic.turn_off_rfid()
        self.controller.show_page("OperationsPage")

    def go_back(self):
        self.controller.show_page("HomePage")
        self.rfid_logic.turn_off_rfid()

class OperationsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        self.controller = controller
        self.state = state
        super().__init__(parent)

        self.bg_image = ctk.CTkImage(light_image = Image.open('images/scan_design.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0)

        self.bg_panel = ctk.CTkFrame(self, width=683, height=204,
                                     fg_color="#99FFD0", #corner_radius=20,
                                     border_color = "#FFFFFF", border_width=4,
                                     bg_color="transparent",)    
        self.bg_panel.place(x=(800/2) - (683/2), y=52)
        #pws.set_opacity(self.bg_panel, color="#000001")

        self.text_container = ctk.CTkFrame(self.bg_panel, fg_color="transparent")
        self.text_container.place(relx=0.5, rely=0.5, anchor="center")

        self.scan_label = ctk.CTkLabel(self.text_container,
                                       text = "Scan Complete ",
                                       font = ("Helvetica", 15),
                                       text_color = "#000000")
        self.scan_label.pack()   

        self.rfid_num_label = ctk.CTkLabel(self.text_container,
                                       text = f"RFID Number: ",
                                       font = ("Helvetica", 15),
                                       text_color = "#000000")
        self.rfid_num_label.pack()

        self.rfid_status_label = ctk.CTkLabel(self.text_container,
                                       text = "Status: ",
                                       font = ("Helvetica", 15),
                                       text_color = "#000000")
        self.rfid_status_label.pack()

        self.rfid_display  = None
        self.rfid_status = None

        self.register_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Register/Reactivate", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.rfid_operation(self.rfid_display, True)) #iibahin ito
        self.register_button.place(x=207, y=289)
        #pws.set_opacity(self.register_button, color="#000001")

        self.deactivate_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Deactivate", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.rfid_operation(self.rfid_display, False)) #iibahin ito
        self.deactivate_button.place(x=412, y=289)
        #pws.set_opacity(self.deactivate_button, color="#000001")

        self.back_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Back", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.clear)
        self.back_button.place(x=(800/2) - (181/2), y=378)
        #pws.set_opacity(self.back_button, color="#000001")

        #will delete this button
        self.x_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="next", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: controller.show_page("CompeleteOperation"))
        self.x_button.place(x=(800/2) - (181/2), y=400)
        #pws.set_opacity(self.x_button, color="#000001")

    def rfid_operation(self, rfid, isUpdate):
        self.state.manipulate_rfid(rfid, isUpdate)
        self.controller.show_page("CompeleteOperation")

    def clear(self):
        self.state.clear_details()
        self.controller.show_page("ScanPage")
    
    def get_current_rfid(self):
        self.rfid_display, self.rfid_status = self.state.get_current_rfid_details()
        return self.rfid_display
    
    def refresh(self):
        self.rfid_display,self.rfid_status = self.state.get_current_rfid_details()
        self.rfid_num_label.configure(text = f"RFID Number: {self.rfid_display}")
        self.rfid_status_label.configure(text = f"Status: {self.rfid_status}")



class CompeleteOperation(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        super().__init__(parent)
        self.controller = controller
        self.state = state
        self.rfid_display, self.rfid_status = self.state.get_current_rfid_details()


        self.bg_image = ctk.CTkImage(light_image = Image.open('images/scan_design.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0)

        self.bg_panel = ctk.CTkFrame(self, width=683, height=204,
                                     fg_color="#99FFD0", #corner_radius=20,
                                     border_color = "#FFFFFF", border_width=4,
                                     bg_color="transparent",)    
        self.bg_panel.place(x=(800/2) - (683/2), y=52)
        #pws.set_opacity(self.bg_panel, color="#000001")

        self.text_container = ctk.CTkFrame(self.bg_panel, fg_color="transparent")
        self.text_container.place(relx=0.5, rely=0.5, anchor="center")

        self.scan_label = ctk.CTkLabel(self.text_container,
                                       text = "Operation Complete",
                                       font = ("Helvetica", 15),
                                       text_color = "#000000")
        self.scan_label.pack()   

        self.rfid_num_label = ctk.CTkLabel(self.text_container,
                                       text = f"RFID Number: {self.rfid_display if self.rfid_display else '0000000'}",
                                       font = ("Helvetica", 15),
                                       text_color = "#000000")
        self.rfid_num_label.pack()

        self.rfid_status_label = ctk.CTkLabel(self.text_container,
                                       text = f"RFID Status: {self.rfid_status}",
                                       font = ("Helvetica", 15),
                                       text_color = "#000000")
        self.rfid_status_label.pack()


        self.rescan_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Scan Again", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.clear("ScanPage"))
        self.rescan_button.place(x=(800/2) - (181/2), y=289)
        #pws.set_opacity(self.rescan_button, color="#000001")

        self.back_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Back", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.clear("HomePage"))
        self.back_button.place(x=(800/2) - (181/2), y=378)
        #pws.set_opacity(self.back_button, color="#000001")

    def clear(self, page):
        self.state.clear_details()
        self.controller.show_page(page)
