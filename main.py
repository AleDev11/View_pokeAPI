import customtkinter
import requests
import json

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    def GetAllPokemon(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    def GetPokemon(self, name):
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        data = json.loads(response.text)

        self.entry.delete(0, "end")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Information general")
        self.tabview.tab("Information general").grid_columnconfigure(0, weight=1)
        self.tabview.add("Evolutions")
        self.tabview.tab("Evolutions").grid_columnconfigure(0, weight=1)
        self.tabview.add("Stats")
        self.tabview.tab("Stats").grid_columnconfigure(0, weight=1)
        self.tabview.add("Abilities")
        self.tabview.tab("Abilities").grid_columnconfigure(0, weight=1)
        self.tabview.add("JSON")
        self.tabview.tab("JSON").grid_columnconfigure(0, weight=1)

        # Information general
        self.label = customtkinter.CTkLabel(self.tabview.tab("Information general"), text=f"Name: {data['name']}")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label = customtkinter.CTkLabel(self.tabview.tab("Information general"), text=f"Height: {data['height']}")
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label = customtkinter.CTkLabel(self.tabview.tab("Information general"), text=f"Weight: {data['weight']}")
        self.label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.label = customtkinter.CTkLabel(self.tabview.tab("Information general"), text=f"Base experience: {data['base_experience']}")
        self.label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.label = customtkinter.CTkLabel(self.tabview.tab("Information general"), text=f"Order: {data['order']}")
        self.label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Evolutions

        # Stats

        # Abilities

        # JSON
        self.textboxJson = customtkinter.CTkTextbox(self.tabview.tab("JSON"), width=1000, height=400, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.textboxJson.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.textboxJson.insert("end", json.dumps(data, indent=4))

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Poke API")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Poke API", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="View All Pokemon")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Search Pokemon...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"), text="Search", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                     command=lambda : self.GetPokemon(self.entry.get()))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=200, height=1000, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # get all pokemon
        data = self.GetAllPokemon()
        for pokemon in data["results"]:
            self.textbox.insert("end", pokemon["name"] + "\n")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        self.tabview.destroy()
        self.textbox = customtkinter.CTkTextbox(self, width=200, height=1000, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        data = self.GetAllPokemon()
        for pokemon in data["results"]:
            self.textbox.insert("end", pokemon["name"] + "\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
