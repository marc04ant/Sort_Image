import os       #I used os package to allow python to work with operating system
from tkinter import Tk, Label, Button, Canvas, filedialog # tkinter is used to create the graphic interface
from PIL import Image, ImageTk, ImageOps # Pillow package is used for image processing and display

class ImageViewer: # We create this class to handle the main window and allow displaying image
    def __init__(self, root, image_paths, destination_folder): # The __init__ method initialize the imageViewer with providing, image path, destination folder and tkinter window
        self.root = root # We define the root of the window
        self.image_paths = image_paths
        self.current_image_index = 0 # The index is defined at 0 at the begining to start displaying the first image of the directory
        self.destination_folder = destination_folder

        self.image_label = Label(root) # to define the Label where images will be displaying
        self.image_label.pack()

        self.prev_button = Button(root, text="Previous", command=self.show_prev_image) # To create the previous button
        self.prev_button.pack(side="left")

        self.next_button = Button(root, text="Next", command=self.show_next_image) # To create the next button
        self.next_button.pack(side="right")

        self.select_button = Button(root, text="Select", command=self.select_image) # To create the select button
        self.select_button.pack()

        self.deselect_button = Button(root, text="deselect", command=self.deselect_image, state="disabled") # To create the deselct button
        self.deselect_button.pack()

         # Canva section where we create the small green circle.
        self.canvas = Canvas(root, width=30, height=30)
        self.canvas.create_oval(10, 10, 20, 20, fill="green", state="hidden")
        self.canvas.pack()

        self.show_current_image()

    def show_current_image(self): # This function display the image at a specific index.
        image_path = self.image_paths[self.current_image_index] # We define which image will display.
        image = Image.open(image_path) # To open the image
        image = ImageOps.exif_transpose(image)  # Manage orientation issues
        image = image.resize((400, 400))  # resize image
        photo = ImageTk.PhotoImage(image) # To create a compatible object between tkinter and Pillow package. We convert photo into a Tkinter PHotoImage.
        self.image_label.config(image=photo) # To set the property of image to the label.
        self.image_label.image = photo # Here we update the image attribute of the label to the tkinter PhotoImage.

        # update of the green symbol.
        if self.is_image_selected(image_path):
            self.canvas.itemconfig(1, state="normal") # to display the small green circle if image is selected.
        else:
            self.canvas.itemconfig(1, state="hidden") # to hide the small green circle if image isn't selected.

    def show_next_image(self): # we define what function will do the next button
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths) #To navigate between the different images we use the modulo methode which is really useful because when we reach the last index it restart from the begining. Here we add 1 to the current index to go to the next image.
        self.show_current_image()
        self.update_deselect_button_state()

    def show_prev_image(self): #function of previous button
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths) #we substract 1 to the current index to go to the previous image.
        self.show_current_image()
        self.update_deselect_button_state()

    def select_image(self): # This function copies the current displayed image into an other folder where we store the selected images.
        image_path = self.image_paths[self.current_image_index] # We set the full path of the current image
        self.copy_image_to_specific_folder(image_path)
        self.show_current_image()
        self.update_deselect_button_state()

    def deselect_image(self):
        image_path = self.image_paths[self.current_image_index]
        image_name = os.path.basename(image_path) # here we just define the name of the folder
        destination_path = os.path.join(self.destination_folder, image_name) # here we add the name of the folder to full destination path. Like that we get the full path of the copied folder.
        try:
            os.remove(destination_path) # to remove the image from the storage folder.
            print(f"Image '{image_name}' deselected and deleted of the directory : {self.destination_folder}") # To insure the operation worked well.
            self.show_current_image()
            self.update_deselect_button_state()
        except FileNotFoundError: #if there isn't such a file in the storage directory we display this message.
            print(f"Impossible to deselect '{image_name}'. Image doesn't exist in the directory : {self.destination_folder}")

    def copy_image_to_specific_folder(self, image_path):
        image_name = os.path.basename(image_path) # to specify just the name of the folder
        destination_path = os.path.join(self.destination_folder, image_name) # to create the full destination path
        with open(image_path, 'rb') as src, open(destination_path, 'wb') as dest: # to copy the file in the destination folder. We use the with methode to insure that the program will open and close the file automaticly even if an exception occur. rb stand for read binary(read the file) and wb stand for write binary(to copy the flie).
            dest.write(src.read()) # We copy the file
        print(f"Image '{image_name}' selected and copied : {self.destination_folder}") # to show us that the image copied successfully.

    def update_deselect_button_state(self): # This function make sure that the deselct button work only when the current image is copied in the destination folder.
        if self.destination_folder:
            self.deselect_button["state"] = "normal"
        else:
            self.deselect_button["state"] = "disabled"

    def is_image_selected(self, image_path): #to check whether the image corresponding to a given image_path is present in the destination folder.
        image_name = os.path.basename(image_path)
        destination_path = os.path.join(self.destination_folder, image_name)
        return os.path.exists(destination_path) # We return if the image exist or no and if the image already exist in the destination folder, the small green circle will appear.

def get_image_paths(folder_path): #to define the full path of the current image in the list of all images in the directory.
    image_extensions = [".jpg", ".jpeg", ".png", ".gif"] # We only allow these images extensions because pillow and tkinter package can only cover these extension.
    image_paths = []
    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in image_extensions): # We check if the filename ends with any of the image extensions in the image_extensions.
            image_paths.append(os.path.join(folder_path, filename)) # if the condition is satisfied, we build the full path of the file.
    return image_paths

if __name__ == "__main__": # To be sure that this part of the program will run only if we run the this specific program.
    # To ask guess to select directory.
    root = Tk()
    root.withdraw()  # Hid tkinter window
    folder_path = filedialog.askdirectory(title="Select directory with the images to sort ")
    if not folder_path:
        print("No specific directory. The program will end")
    else:
        image_paths = get_image_paths(folder_path) # to pick the storage directory
        if not image_paths:
            print("No image found in the directory")
        else:
            root.deiconify()  # Display main tkinter window
            root.title("Image viewer")
            destination_folder = filedialog.askdirectory(title="Select destination directory") # to define destination folder
            if not destination_folder:
                print("No destination directory specified. Program will end")
                root.destroy()
            else:
                image_viewer = ImageViewer(root, image_paths, destination_folder) #to execute the class ImageViewer
                root.mainloop()



