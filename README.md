# Sort_Image
Main function : This python program is designed to facilitate the selection of images in a folder and to stock them into a storage folder.

**What's happening when you run the code :** 
1. When you run this program, a window will appear allowing you to choose the folder you want to sort.
2. Next, another window will appear, allowing you to select the folder where you want to store the selected images.
3. A Tkinter window will then open, displaying the first image from the chosen folder.
4. You can use the "Next" button to view the next image and the "Previous" button to go back to the previous image.
5. There are also "Select" and "Deselect" buttons. Clicking "Select" will copy the image to the storage folder and display a small green circle to indicate it's selected. Clicking "Deselect" will remove the image from the storage folder and hide the green circle, indicating it's not selected.
6. When you're finished sorting all the images in the folder, simply close the program by clicking the small red cross at the top of the window.

**How the program work :**

First of all we import necessary packages, such as **os** for working with the operating system, **tkinter** for creating the graphic interface, and **Pillow** for image processing and display.
The code defines a class called **ImageViewer**, which handles the main window and allows for image display.
The __init__ method initializes the ImageViewer object by providing the root (Tkinter window), image paths, and destination folder.
Various buttons and a canvas with a green circle are created using the **Label, Button, and Canvas widgets from tkinter**.
The **show_current_image** method displays the image at a specific index.
The **show_next_image** and **show_prev_image** methods navigate to the next and previous images.
The **select_image** method copies the current displayed image into the destination folder.
The **deselect_image** method removes the image from the storage folder and hides the green circle.
The **copy_image_to_specific_folder** method copies an image to the destination folder.
The **update_deselect_button_state** method enables or disables the deselect button based on whether the current image is in the destination folder.
The **is_image_selected** method checks if the image corresponding to a given image path is present in the destination folder.
The **get_image_paths** function returns the full path of the current image in the list of all images in the directory.
The __name__ == "__main__" block runs the program if it is executed as the main module.
The program prompts the user to select directories using file dialogs from tkinter.
The ImageViewer class is called, and the tkinter main loop (root.mainloop()) is started to display the graphical interface.
