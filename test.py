import tkinter as tk
from Modules.GetCoordinatesImage import GetCoordinatesImage
root = tk.Tk()
file_path = "C:\\Users\\KhanhTien\\Desktop\\Untitled.png"
app = GetCoordinatesImage.ImageEditor(root, file_path)
root.mainloop()
