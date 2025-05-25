import customtkinter as ctk
from logic import AppState
from logic import RFID_Logic
from tkinter import messagebox
from PIL import Image

#import pywinstyles as #pws

class AppUI:
    def __init__(self, root): 
        self.root = root
        self.state = AppState()
        #self.logic = RFID_Logic()
        self.root.title("Pic-a-Pi RFID")
        self.root.geometry("800x480")

        self.root.bind("<Escape>", lambda event: self.quit_app())
        
        self.container = ctk.CTkFrame(self.root)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {} #container ito ng page states
        self.current_page = None

        for PageClass in (HomePage, ScanPage, CustomerOperationsPage, AdminOperationsPage, CompeleteOperation, HistoryPage):
            page_name = PageClass.__name__
            frame = PageClass(self.container, self, self.state)
            self.pages[page_name] = frame
            frame.grid(row= 0, column = 0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name):
        self.current_page = page_name
        frame = self.pages[page_name]
        frame.tkraise()
        if hasattr (frame, "refresh"):
            frame.refresh()

    def quit_app(self):
        if self.current_page == "HomePage":
            print("Escape pressed on HomePage. Quitting app.")
            self.root.destroy()
        

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        super().__init__(parent)
        self.controller = controller
        self.button_height = 45
        self.button_width = 144
        self.state = state

        self.bg_image = ctk.CTkImage(light_image = Image.open('images/home_design.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.close_image = ctk.CTkImage(light_image = Image.open('images/close_button.png'), size = (40,40))
        self.bg_image_label = ctk.CTkLabel(self, image = self.close_image, text = "", bg_color="#000001")
        self.bg_image_label.place(x=740, y=21)
        self.bg_image_label.bind("<Button-1>", self.exit_app)


        self.ad_cards_button = ctk.CTkButton(self, height = self.button_height, width = self.button_width,
                                            text = "Admin Cards",
                                            text_color = "#000000",
                                            font = ("Helvetica", 15),
                                            #corner_radius = 20,
                                            fg_color = "#99FFD0",
                                            bg_color="transparent",
                                            border_color = "#FFFFFF",
                                            border_width=4,
                                            command=lambda: self.set_target_page("AdminOperationsPage"))
        self.ad_cards_button.place(x=162, y=351)

        self.customer_button = ctk.CTkButton(self, height = self.button_height, width = self.button_width,
                                            text = "Customer",
                                            text_color = "#000000",
                                            font = ("Helvetica", 15),
                                            #corner_radius = 20,
                                            fg_color = "#99FFD0",
                                            bg_color="transparent",
                                            border_color = "#FFFFFF",
                                            border_width=4,
                                            command=lambda: self.set_target_page("CustomerOperationsPage"))
        self.customer_button.place(x=328, y=351)
        ##pws.set_opacity(self.scan_button, color="#000001")


        self.history_button = ctk.CTkButton(self, height = self.button_height, width = self.button_width,
                                            text = "History",
                                            text_color = "#000000",
                                            font = ("Helvetica", 15),
                                            #corner_radius = 20,
                                            fg_color = "#99FFD0",
                                            bg_color="transparent",
                                            border_color = "#FFFFFF",
                                            border_width=4,
                                            command=lambda: self.set_target_page("HistoryPage"))
        self.history_button.place(x=494, y=351)

    def exit_app(self, event=None):
        self.controller.root.destroy()

    def set_target_page(self, page):
        self.state.set_page_destination(page)
        self.controller.show_page("ScanPage")

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
                                        command=lambda: self.go_back())
        self.back_button.place(x=(800/2) - (181/2), y=378)
        ##pws.set_opacity(self.back_button, color="#000001")
        self.rfid_logic = RFID_Logic(self.on_rfid_scanned)
        self.rfid_logic.turn_on_rfid()

        #will remove this shit
        '''

        self.next_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="next", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.next_page())
        self.next_button.place(x=(800/2) - (181/2), y=378 + 20)
        '''

    def on_rfid_scanned(self, rfid):
        self.state.set_rfid(rfid)
        self.rfid_logic.turn_off_rfid()
        #self.controller.show_page("OperationsPage")

        page_dest = self.state.get_page_destination()
        is_exist = self.state.verify_rfid_exist(rfid)

        if page_dest == "HistoryPage" and is_exist:
            self.controller.show_page("HistoryPage")
        elif page_dest != "HistoryPage":
            self.controller.show_page(page_dest)
        else:
            print("RFID not found. Cannot go to HistoryPage.")

    
    def refresh(self):
        self.rfid_logic.turn_on_rfid()

    def go_back(self):
        self.controller.show_page("HomePage")
        #self.rfid_logic.turn_off_rfid()
        
    #test 
        '''

    def next_page(self):
        page_dest = self.state.get_page_destination()
        self.controller.show_page(page_dest)
        '''
        

class CustomerOperationsPage(ctk.CTkFrame):
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

        self.rfid_num_label = ctk.CTkLabel(self.text_container,
                                       text = f"RFID Number: ",
                                       font = ("Helvetica", 25),
                                       text_color = "#000000")
        self.rfid_num_label.pack()

        self.rfid_status_label = ctk.CTkLabel(self.text_container,
                                       text = "Status: ",
                                       font = ("Helvetica", 25),
                                       text_color = "#000000")
        self.rfid_status_label.pack()

        self.customer_name_label = ctk.CTkLabel(self.text_container,
                                                text="Customer Name:",
                                                font=("Helvetica", 25),
                                                text_color="#000000")
        self.customer_name_label.pack(pady=(10, 0))  # Add spacing above

        # Customer Name Text Entry
        vcmd = (self.register(self.validate_name_input), '%P')
        self.customer_name_entry = ctk.CTkEntry(self.text_container,
                                                font=("Helvetica", 20),
                                                width=300,
                                                height=35,
                                                text_color="#000000",
                                                validate="key",
                                                validatecommand=vcmd)
        self.customer_name_entry.pack(pady=(5, 0))  # Add small gap between label and entry


        self.rfid_display  = None
        self.rfid_status = None
        self.cust_status = None

        self.register_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Use Card", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.use_rfid()) 
        self.register_button.place(x=207, y=289)
        #pws.set_opacity(self.register_button, color="#000001")

        self.deactivate_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Void Card", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.void_rfid_session()) 
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
                                        command=lambda: self.clear())
        self.back_button.place(x=(800/2) - (181/2), y=378)
        #pws.set_opacity(self.back_button, color="#000001")
        '''

        self.next_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Back", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.clear())
        self.next_button.place(x=(800/2) - (181/2) + 20, y=378)
        '''
    def validate_name_input(self, new_value):
        # Allow empty input
        if new_value == "":
            return True

        # Max length of 25
        if len(new_value) > 25:
            return False

        # Only allow letters, periods, spaces
        for char in new_value:
            if not (char.isalpha() or char in ['.', ' ']):
                return False

        return True
    
    def get_current_rfid(self):
        self.rfid_display, self.rfid_status = self.state.get_current_rfid_details()
        return self.rfid_display
    
    def clear(self):
        self.state.clear_details()
        self.controller.show_page("HomePage")

    def use_rfid(self):
        cust_name = self.customer_name_entry.get()
        if cust_name: 
            self.state.use_card(cust_name, self.rfid_display)
            self.controller.show_page("CompeleteOperation")


    def void_rfid_session(self):
        cust_name = self.customer_name_entry.get()
        if cust_name: 
            self.state.void_card(cust_name, self.rfid_display)
            self.controller.show_page("CompeleteOperation")


    def refresh(self):
        self.customer_name_entry.delete(0, 'end')

        self.rfid_display, self.rfid_status = self.state.get_current_rfid_details()

        self.cust_name, self.cust_status = self.state.get_customer_name(self.rfid_display)
        self.rfid_num_label.configure(text=f"RFID Number: {self.rfid_display}")
        self.rfid_status_label.configure(text=f"Status: {self.cust_status}")

        if self.cust_name != "d":
            self.customer_name_entry.insert(0, self.cust_name)


class AdminOperationsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        self.controller = controller
        self.state = state
        super().__init__(parent)

        self.rfid_display  = None
        self.rfid_status = None
        self.admin_name = None
        self.admin_cont_number = None


        self.button_width = 180
        self.button_height = 56

        self.bg_image = ctk.CTkImage(light_image = Image.open('images/scan_design.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0)

        # Main panel
        self.bg_panel = ctk.CTkFrame(self, width=683, height=203,
                                    fg_color="#99FFD0",
                                    border_color="#FFFFFF", border_width=4,
                                    bg_color="transparent")
        self.bg_panel.grid_propagate(False)  # Just in case
        self.bg_panel.pack_propagate(False)
        self.bg_panel.place(x=(800/2) - (683/2), y=52)

        # Stack everything vertically in this container
        self.text_container = ctk.CTkFrame(self.bg_panel, fg_color="transparent")
        self.text_container.pack(expand=True)

        # RFID Number label
        self.rfid_num_label = ctk.CTkLabel(self.text_container,
                                        text="RFID Number: ",
                                        font=("Helvetica", 25),
                                        text_color="#000000")
        self.rfid_num_label.pack(pady=(10, 0))

        # Status label
        self.rfid_status_label = ctk.CTkLabel(self.text_container,
                                            text="Status: Doesn’t Exist",
                                            font=("Helvetica", 25, "bold"),
                                            text_color="#000000")
        self.rfid_status_label.pack(pady=(0, 10))

        # Admin Name (Label + Entry in one row)
        self.admin_name_container = ctk.CTkFrame(self.text_container, fg_color="transparent")
        self.admin_name_container.pack(pady=(0, 5))

        self.admin_name_label = ctk.CTkLabel(self.admin_name_container,
                                            text="Admin Name:",
                                            font=("Helvetica", 22),
                                            text_color="#000000")
        self.admin_name_label.pack(side="left", padx=(0, 10))

        vcmd = (self.register(self.validate_name_input), '%P')
        self.admin_name_entry = ctk.CTkEntry(self.admin_name_container,
                                            font=("Helvetica", 20),
                                            width=300,
                                            height=35,
                                            text_color="#000000",
                                            validate="key",
                                            validatecommand=vcmd)
        self.admin_name_entry.pack(side="left")

        # Contact (Label + Entry in one row)
        self.admin_cont_container = ctk.CTkFrame(self.text_container, fg_color="transparent")
        self.admin_cont_container.pack(pady=(0, 10))

        self.admin_cont_label = ctk.CTkLabel(self.admin_cont_container,
                                            text="Contact:",
                                            font=("Helvetica", 22),
                                            text_color="#000000")
        self.admin_cont_label.pack(side="left", padx=(0, 10))

        vcmd = (self.register(self.validate_number_input), "%P")
        self.admin_cont_entry = ctk.CTkEntry(self.admin_cont_container,
                                            font=("Helvetica", 20),
                                            width=300,
                                            height=35,
                                            text_color="#000000",
                                            validate="key",
                                            validatecommand=vcmd)
        self.admin_cont_entry.pack(side="left")

        self.register_button = ctk.CTkButton(self, width = self.button_width, height = self.button_height, 
                                        text="Register", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.insert_admin()) 
        self.register_button.place(x=105, y=293)
        #pws.set_opacity(self.register_button, color="#000001")

        self.update_button = ctk.CTkButton(self, width = self.button_width, height = self.button_height, 
                                        text="Update", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.update_admin()) 
        self.update_button.place(x=309, y=293)
        #pws.set_opacity(self.deactivate_button, color="#000001")

        self.status_button = ctk.CTkButton(self, width = self.button_width, height = self.button_height, 
                                        text="Activate/Deactivate", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.rfid_operation(self.rfid_display)) 
        self.status_button.place(x=515, y=293)
        #pws.set_opacity(self.deactivate_button, color="#000001")

        self.back_button = ctk.CTkButton(self, width = self.button_width, height = self.button_height, 
                                        text="Back", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.clear())
        self.back_button.place(x=309, y=378)
        #pws.set_opacity(self.back_button, color="#000001")

        '''
        self.next_button = ctk.CTkButton(self, height = 54, width = 181, 
                                        text="Back", 
                                        text_color = "#000000",
                                        font = ("Helvetica", 15),
                                        #corner_radius = 20,
                                        fg_color = "#99FFD0",
                                        bg_color="transparent",
                                        border_color = "#FFFFFF",
                                        border_width=4,                                         
                                        command=lambda: self.clear())
        self.next_button.place(x=309 + 20, y=378)
        '''

    def validate_name_input(self, new_value):
        # Allow empty input
        if new_value == "":
            return True

        # Max length of 25
        if len(new_value) > 25:
            return False

        # Only allow letters, periods, spaces
        for char in new_value:
            if not (char.isalpha() or char in ['.', ' ']):
                return False

        return True
    
    def validate_number_input(self, value_if_allowed):
        """Allow only digits and max 11 characters."""
        if value_if_allowed.isdigit() and len(value_if_allowed) <= 11:
            return True
        elif value_if_allowed == "":  # Allow backspace
            return True
        else:
            return False

    def rfid_operation(self, rfid):
        self.state.manipulate_rfid(rfid, self.rfid_status)
        self.controller.show_page("CompeleteOperation")

    def insert_admin(self):
        admin_name = self.admin_name_entry.get()
        admin_cont = self.admin_cont_entry.get()
        if admin_name and admin_cont:
            self.state.insert_admin(admin_name, admin_cont, self.rfid_display)
            self.controller.show_page("CompeleteOperation")

    def update_admin(self):
        admin_name = self.admin_name_entry.get()
        admin_cont = self.admin_cont_entry.get()
        if admin_name and admin_cont:
            self.state.update_admin_details(admin_name, admin_cont, self.rfid_display)
            self.controller.show_page("CompeleteOperation")

    def clear(self):
        self.state.clear_details()
        self.controller.show_page("HomePage")
    
    def get_current_rfid(self):
        self.rfid_display, self.rfid_status = self.state.get_current_rfid_details()
        return self.rfid_display
    
    def refresh(self):
        self.admin_name_entry.delete(0, 'end')
        self.admin_cont_entry.delete(0, 'end') 

        self.rfid_display,self.rfid_status = self.state.get_current_rfid_details()
        self.admin_name, self.admin_cont_number,_,_= self.state.get_rfid_details(self.rfid_display)
        
        if self.rfid_status == None:
            self.rfid_status = "Doesn't Exist"
        else:
            self.admin_name_entry.insert(0, self.admin_name)
            self.admin_cont_entry.insert(0, self.admin_cont_number)

        self.rfid_num_label.configure(text = f"RFID Number: {self.rfid_display}")
        self.rfid_status_label.configure(text = f"Status: {self.rfid_status}")


class CompeleteOperation(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        super().__init__(parent)
        self.controller = controller
        self.state = state

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
                                       font = ("Helvetica", 25),
                                       text_color = "#000000")
        self.scan_label.pack()   

        self.rfid_num_label = ctk.CTkLabel(self.text_container,
                                       text = f"RFID Number: ",
                                       font = ("Helvetica", 25),
                                       text_color = "#000000")
        self.rfid_num_label.pack()

        self.rfid_status_label = ctk.CTkLabel(self.text_container,
                                       text = f"RFID Status: ",
                                       font = ("Helvetica", 25),
                                       text_color = "#000000")
        self.rfid_status_label.pack()

        self.rfid_display = None
        self.rfid_status = None


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

    def refresh(self):
        self.rfid_display,self.rfid_status = self.state.get_current_rfid_details()
        self.rfid_num_label.configure(text = f"RFID Number: {self.rfid_display}")
        self.rfid_status_label.configure(text = f"Status: {self.rfid_status}")

class HistoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, state):
        super().__init__(parent)
        self.controller = controller
        self.state = state
        self.ad_name = None
        self.ad_number = None
        self.ad_rfid = None
        self.current_index = 0         # where the visible slice starts
        self.page_size = 4             # how many cards to show at a time

        self.bg_image = ctk.CTkImage(light_image = Image.open('images/light_green.png'), 
                                                                size = (800,480)) #just to make sure
        
        self.bg_image_label = ctk.CTkLabel(self, image = self.bg_image, text = "")
        self.bg_image_label.place(x=0, y=0)

        self.back_image = ctk.CTkImage(light_image = Image.open('images/back_button.png'), size = (53,20))
        self.back_image_label = ctk.CTkLabel(self, image = self.back_image, text = "", bg_color = "#198050")
        self.back_image_label.place(x=15, y=25)
        self.back_image_label.bind("<Button-1>", self.go_back)


        ####################
        #Admin Details Display
        ####################
        self.admin_details_bg = ctk.CTkFrame(self, width = 469, height = 83,
                                            fg_color="#99FFD0",
                                            border_color="#FFFFFF", border_width=2,
                                            bg_color="transparent")
        self.admin_details_bg.place(x=315,y=12)


        self.text_container = ctk.CTkFrame(self.admin_details_bg, fg_color = "transparent")
        self.text_container.pack(expand=True)

        self.admin_name_cont = ctk.CTkFrame(self.text_container, fg_color="transparent")

        self.admin_name = ctk.CTkLabel(self.text_container,
                                   text="Admin Name: ",
                                   font=("Helvetica", 20),
                                   text_color="#000000")
        self.admin_name.pack()

        self.admin_number = ctk.CTkLabel(self.text_container,
                                   text="Contact Number: ",
                                   font=("Helvetica", 20),
                                   text_color="#000000")
        self.admin_number.pack()

        self.admin_rfid = ctk.CTkLabel(self.text_container,
                                   text="RFID Key: ",
                                   font=("Helvetica", 20),
                                   text_color="#000000")
        self.admin_rfid.pack()

        ##############################
        # Customer Details
        ##############################
        self.cust_details_bg = ctk.CTkFrame(self, width = 770, height = 358,
                                            fg_color="#198050",
                                            border_color="#000000", border_width=0,
                                            bg_color="transparent")
        self.cust_details_bg.place(x=15,y=110)

        self.cust_details_header_bg = ctk.CTkFrame(self, width = 759, height = 41,
                                                fg_color = "#99FFD0",
                                                border_color="#000000", border_width=1,
                                                bg_color="transparent")
        self.cust_details_header_bg.place(x=21,y=118)

        self.cust_details_header = ctk.CTkLabel(self, text="Transactions",
                                                font=("Helvetica", 25),
                                                fg_color = "#99FFD0",
                                                text_color="#000000")
        self.cust_details_header.place(x = 321,y =121 ) 

        #up button for navigation
        self.navigate_up_db_image = ctk.CTkImage(light_image = Image.open('images/navigate_up.png'), size = (53,20))
        self.bg_up_image_label = ctk.CTkLabel(self, image = self.navigate_up_db_image, text = "", bg_color = "#198050")
        self.bg_up_image_label.place(x=387, y=182)
        self.bg_up_image_label.bind("<Button-1>", self.scroll_up)

        #down button for navigation
        self.navigate_down_db_image = ctk.CTkImage(light_image = Image.open('images/navigate_down.png'), size = (53,20))
        self.bg_down_image_label = ctk.CTkLabel(self, image = self.navigate_down_db_image, text = "", bg_color = "#198050")
        self.bg_down_image_label.place(x=387, y=439)
        self.bg_down_image_label.bind("<Button-1>", self.scroll_down)


        self.card_container = ctk.CTkFrame(self, width = 759, height = 215,
                                            bg_color = "#198050")
        self.card_container.place(x = 20,y =216) 

    def refresh(self):
        rfid_key,_= self.state.get_current_rfid_details()
        self.ad_name, self.ad_number,_,self.ad_rfid = self.state.get_rfid_details(rfid_key)
        self.admin_name.configure(text = f"Admin Name: : {self.ad_name}")
        self.admin_number.configure(text = f"Contact Number: : : {self.ad_number}")
        self.admin_rfid.configure(text = f"RFID Key: : {self.ad_rfid}")
        self.refresh_table()

    def refresh_table(self):
        for widget in self.card_container.winfo_children():
            widget.destroy()

        results = self.state.get_customer_details(self.ad_rfid, self.current_index, self.page_size)
        for i, row in enumerate(results):
            email, session_id, name, status, date = row
            card = CustomerDetailsCard(self.card_container, session_id = session_id, date=date, name=name, email=email, status=status)
            card.place(x=0, y=i * 55)

        self.last_page_empty = len(results) < self.page_size  # Track end of data


    def scroll_up(self, event=None):
        if self.current_index - self.page_size >= 0:
            self.current_index -= self.page_size
            print("hehe up")
            self.refresh_table()

    def scroll_down(self, event=None):
        if not getattr(self, 'last_page_empty', False):  # Avoid going past last page
            self.current_index += self.page_size
            print("hehe down")
            self.refresh_table()

    def go_back(self, event=None):
        self.current_index = 0         # where the visible slice starts
        self.page_size = 4             # how many cards to show at a time
        self.controller.show_page("HomePage")

#this is for the customer cards
class CustomerDetailsCard(ctk.CTkFrame):
    def __init__(self, parent, session_id, date, name, email, status, *args, **kwargs):
        super().__init__(parent, width=758, height=49, *args, **kwargs)
        self.configure(fg_color="#99FFD0", border_color="black", border_width=1)
        self.state = AppState()
        self.sess_id = session_id

        # Create and place Date label
        self.date_label = ctk.CTkLabel(self, text=f"Date:\n{date}", font=("Helvetica", 12), text_color="#000000", anchor="w")
        self.date_label.place(x=10, y=5)

        # Name label
        self.name_label = ctk.CTkLabel(self, text=f"Name:\n{name}", font=("Helvetica", 12), text_color="#000000", anchor="w")
        self.name_label.place(x=150, y=5)

        # Email label
        self.email_label = ctk.CTkLabel(self, text=f"E-mail:\n{email}", font=("Helvetica", 12), text_color="#000000", anchor="w")
        self.email_label.place(x=300, y=5)

        # Status label
        self.status_label = ctk.CTkLabel(self, text=f"Status:\n{status}", font=("Helvetica", 12), text_color="#000000", anchor="w")
        self.status_label.place(x=550, y=5)

        # Print Button
        self.print_button = ctk.CTkButton(self, text="Print", width=60, height=30, font=("Helvetica", 12), fg_color="#00695C", command=lambda: self.print_with_overlay())
        self.print_button.place(x=680, y=9)

        self.overlay = ctk.CTkFrame(self, width=758, height=49, fg_color="#000000", bg_color="transparent")
        self.overlay.place(x=0, y=0)
        self.overlay.lower()  # Start hidden

        self.overlay_label = ctk.CTkLabel(self.overlay, text="Printing...", font=("Helvetica", 16),
                                          text_color="#FFFFFF")
        self.overlay_label.place(relx=0.5, rely=0.5, anchor="center")

    def print_with_overlay(self):
        printer_status = self.state.get_printer_status("test_printer")
        if printer_status == 3:
            self.print_card(self.sess_id)
        else:
            messagebox.showerror("Failure", "Printer is disconnected.")


    def print_card(self, session_id):
        #self.state.print_image_admin(session_id)
        success = self.state.print_image_admin(session_id)
        if success:
            messagebox.showinfo("Success", "Printing completed!")
        else:
            messagebox.showerror("Failure", "Printing failed.")


