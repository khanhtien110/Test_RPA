import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from simplification.cutil import simplify_coords
import numpy as np
from shapely.geometry import Polygon

class ImageEditor:
    def __init__(self, root, file_path=None):
        self.root = root
        self.root.title("도형이 있는 이미지 편집기")

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        # self.open_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image)
        # self.open_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.file_path = file_path

        self.type_var = tk.StringVar(value="추적 영역")  # Giá trị mặc định
        self.type_menu = ttk.Combobox(self.button_frame, textvariable=self.type_var, state="readonly")
        self.type_menu["values"] = ("제한 영역", "추적 영역")
        self.type_menu.pack(side=tk.LEFT, padx=5, pady=5)
        self.type_menu.bind("<<ComboboxSelected>>", self.update_color)  # Gán sự kiện khi chọn

        self.mode_var = tk.StringVar(value="자유 손그림")
        self.mode_menu = tk.OptionMenu(self.button_frame, self.mode_var, "자유 손그림", "사각형", "원")
        self.mode_menu.pack(side=tk.LEFT, padx=5, pady=5)

        self.undo_button = tk.Button(self.button_frame, text="실행 취소", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="좌표 저장", command=self.save_coordinates)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.color = "orange"
        self.image = None
        self.image_tk = None
        self.start_x = None
        self.start_y = None
        self.coordinates = []  # Lưu tọa độ vẽ
        self.shapes = []  # Lưu ID của các hình trên canvas (để Undo)
        self.temp_shape = None  # Hình tạm thời khi vẽ
        self.background_image_id = None  # Lưu ID hình nền

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.root.bind("<Control-z>", lambda event: self.undo())  # Thêm phím tắt Ctrl + Z
        if self.file_path:
            self.open_image(self.file_path)

    def update_color(self, event=None):
        selected_type = self.type_var.get()
        if selected_type == "제한 영역":
            self.color = "red"
        elif selected_type == "추적 영역":
            self.color = "orange"
            
    def open_image(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)

            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.delete("all")  # Xóa canvas trước khi vẽ hình mới
            self.background_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.temp_shape = None  # Reset hình tạm thời
        shape_type = self.type_var.get() 
        if self.mode_var.get() == "자유 손그림":
            self.current_line = []
            self.coordinates.append(("Freehand", self.current_line, "Restrict Area" if shape_type == "제한 영역" else "Tracking Area"))  # Bắt đầu một đường vẽ mới

    def paint(self, event):
        x, y = event.x, event.y
        mode = self.mode_var.get()
    
        if mode == "자유 손그림":
            line = self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=2)
            self.shapes.append(line)  # Lưu ID để Undo
            self.current_line.append((self.start_x, self.start_y, x, y))  # Lưu điểm vẽ
            self.start_x, self.start_y = x, y  # Cập nhật vị trí cuối

        elif mode in ["사각형", "원"]:
            # Xóa hình tạm thời trước khi vẽ lại
            if self.temp_shape:
                self.canvas.delete(self.temp_shape)

            if mode == "사각형":
                self.temp_shape = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.color, width=2)
            else:  # 원 mode
                self.temp_shape = self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.color, width=2)

    def end_draw(self, event):
        x, y = event.x, event.y
        mode = self.mode_var.get()
        shape_type = "Restrict Area" if self.type_var.get() == "제한 영역" else "Tracking Area"
        if mode == "자유 손그림" and len(self.current_line) > 2:  # Chỉ xử lý nếu có hơn 2 điểm
            points = np.array(self.current_line, dtype=np.float32)[:, :2]  # Lấy (x, y)

            # Làm mượt nét vẽ (độ chính xác epsilon = 2.0)
            simplified_points = simplify_coords(points, 10.0).tolist()

            self.coordinates.pop()
            self.coordinates.append(("Freehand", simplified_points, shape_type))
            
            self.redraw_coordonates()

        if mode == "사각형":
            rect = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.color, width=2)
            self.coordinates.append(("Rectangle", (self.start_x, self.start_y, x, y), shape_type))  # Lưu thêm type
            self.shapes.append(rect)  # Lưu ID để Undo

        elif mode == "원":
            circle = self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.color, width=2)
            self.coordinates.append(("Circle", (self.start_x, self.start_y, x, y), shape_type))
            self.shapes.append(circle)  # Lưu ID để Undo
        if len(self.coordinates) > 1:
            
            if self.check_overlap(self.coordinates[-1]):
                self.coordinates.pop()                
                self.redraw_coordonates()
                messagebox.showwarning("겹침 감지", "도형이 기존 도형과 겹칩니다!")
    def undo(self):
        """Undo the last drawn shape while keeping the background image intact."""
        if self.shapes and self.coordinates:
            last_shape = self.coordinates.pop()
            
            # Remove drawn shape from the canvas
            if last_shape[0] == "자유 손그림":
                for _ in range(len(last_shape[1]) - 1):  # Each segment of 자유 손그림 drawing
                    self.canvas.delete(self.shapes.pop())
            else:
                self.canvas.delete(self.shapes.pop())  # Remove 사각형 or 원

        self.redraw_coordonates()

    def save_coordinates(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for shape in self.coordinates:
                    shape_type, shape_data, area_type = shape  # Lấy thêm loại vùng
                    f.write(f"{shape_type}, {shape_data}, {area_type}\n")  # Ghi vào file
            print(f"✅ Coordinates saved to: {file_path}")


    def redraw_coordonates(self):
        # Redraw background image
        self.canvas.delete("all")
        if self.image_tk:
            self.background_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        # Re-draw all remaining shapes
        self.shapes.clear()
        for shape in self.coordinates:
            shape_type, shape_data, type_area= shape  # Extract type and coordinates
            color = "red" if type_area == "Restrict Area" else "orange"
            if shape_type == "Freehand":
                if len(shape_data) > 1:
                    for i in range(len(shape_data) - 1):
                        x1,y1, = shape_data[i]
                        x2, y2 = shape_data[i + 1]
                        line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                        self.shapes.append(line)

                    # **Nối điểm đầu và điểm cuối nếu chưa khép kín**
                    first_x, first_y = shape_data[0]
                    last_x1, last_y1 = shape_data[-1]
                    if (abs(first_x - last_x1) > 5 or abs(first_y - last_y1) > 5):  # Kiểm tra khoảng cách
                        closing_line = self.canvas.create_line(last_x1, last_y1,first_x, first_y, fill=color, width=2)
                        self.shapes.append(closing_line)

            elif shape_type == "Rectangle":
                x1, y1, x2, y2 = shape_data
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=2)
                self.shapes.append(rect)

            elif shape_type == "Circle":
                x1, y1, x2, y2 = shape_data
                circle = self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=2)
                self.shapes.append(circle)

    def check_overlap(self, new_shape):
        new_type, new_coords, _ = new_shape  # Bỏ qua type_area
        
        if new_type == "Rectangle":
            x1, y1, x2, y2 = new_coords
            new_polygon = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
        elif new_type == "Freehand":
            if len(new_coords) < 3:
                return True
            new_polygon = Polygon(new_coords)  # 자유 손그림 đã có sẵn dạng danh sách (x, y)
        else:
            return False  # Chưa hỗ trợ kiểm tra 원

        for shape in self.coordinates[:-1]:
            shape_type, shape_data, _ = shape
            if shape_type == "Rectangle":
                x1, y1, x2, y2 = shape_data
                existing_polygon = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
            elif shape_type == "Freehand":
                existing_polygon = Polygon(shape_data)
            else:
                continue

            if new_polygon.intersects(existing_polygon):
                return True  # Có chồng chéo

        return False  # Không chồng chéo