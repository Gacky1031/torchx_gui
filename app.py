import customtkinter as tk
from customtkinter import filedialog
from PIL import Image, ImageTk
import util
import torchxrayvision as xrv

class ImageClassifierApp(tk.CTk):
    def __init__(self):
        super().__init__()
        tk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.title("Image Classifier")
        self.geometry("800x800")
        
        self.left_frame = tk.CTkFrame(self, width=450, height=800)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.CTkFrame(self, width=350, height=800)
        self.right_frame.pack(side=tk.LEFT, padx=10)


        self.load_image_button = tk.CTkButton(self.left_frame, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=50)
        
        self.blank_img = ImageTk.PhotoImage(Image.new("L",(250,250),0))

        self.image_label = tk.CTkLabel(self.left_frame,text="",image=self.blank_img)
        self.image_label.pack(expand=True,padx=100,pady=20)
        
        self.heatmap_label = tk.CTkLabel(self.left_frame,text="",image=self.blank_img)
        self.heatmap_label.pack(expand=True,padx=100,pady=20)
        # Create buttons for each class
        self.button_prediction = dict()
        self.class_buttons = dict()
        self.prediction_dict = dict()
        
        for class_name in util.model.pathologies:
            self.button_prediction[class_name] = tk.CTkFrame(self.right_frame)
            self.class_buttons[class_name] = tk.CTkButton(self.button_prediction[class_name], text=class_name, command=lambda name=class_name: self.show_heatmap(name))
            self.prediction_dict[class_name] = tk.CTkLabel(self.button_prediction[class_name], text="__ %")
            self.class_buttons[class_name].pack(side=tk.LEFT)
            self.prediction_dict[class_name].pack(side=tk.LEFT,padx=10)
            self.button_prediction[class_name].pack(pady = 5)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Imagefiles", "*.jpg;*.jpeg;*.png")])
        self.raw_img, self.raw_img_pl = util.load_file(file_path)
        
        self.img_tk = ImageTk.PhotoImage(image=self.raw_img_pl)
        self.image_label.configure(image=self.img_tk)  
        self.heatmap_label.configure(image= self.blank_img)

        
        processed_img, probabilities = util.prediction(self.raw_img)
        for k,v in probabilities.items():
            self.prediction_dict[k].configure(text=v)
        self.processed_img = processed_img
        

    def show_heatmap(self, class_name):
        result_img = util.get_heatmap(self.processed_img,self.raw_img_pl,class_name)
        self.heatmap_tk = ImageTk.PhotoImage(image=result_img)
        self.heatmap_label.configure(image= self.heatmap_tk)


if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
