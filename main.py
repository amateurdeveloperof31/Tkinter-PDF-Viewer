# ------------------------------------------------------ Imports -------------------------------------------------------
from tkinter import * # Tkinter
from tkinter import filedialog # Tkinter
import pymupdf # PyMuPDF
from PIL import Image, ImageTk # Pillow
# -------------------------------------------- Global Variables / Settings ---------------------------------------------
width = 600
height = 600
# ----------------------------------------------------- Main Class -----------------------------------------------------
class MyOwnPDFViewer:
    def __init__(self):

        # Window Configuration
        self.windows = Tk()
        self.windows.title("My Own PDF Viewer!!")
        self.windows.minsize(width, height)
        self.windows.resizable(False, False)
        self.windows.config(bg='white')

        self.document_size = None

        # Widgets
        self.toolbar_frame = Frame(self.windows, height=50, width=width, bg='#373737')
        self.toolbar_frame.place(relx=0, rely=0)

        self.open_file_button = Button(self.toolbar_frame, text="Open", width=12, bg='#4e4e4e', fg='white',
                                       command=self.open_pdf_file)
        self.open_file_button.place(relx=0.1, rely=0.5, anchor=CENTER)

        self.next_page_button = Button(self.toolbar_frame, text="Next Page", width=12, bg='#4e4e4e', fg='white',
                                       command=self.next_page)
        self.next_page_button.place(relx=0.28, rely=0.5, anchor=CENTER)

        self.previous_page_button = Button(self.toolbar_frame, text="Previous Page", width=12, bg='#4e4e4e', fg='white',
                                       command=self.prev_page)
        self.previous_page_button.place(relx=0.46, rely=0.5, anchor=CENTER)

        self.zoom_in_button = Button(self.toolbar_frame, text="Zoom In", width=8, bg='#4e4e4e', fg='white',
                                       command=self.zoom_in)
        self.zoom_in_button.place(relx=0.62, rely=0.5, anchor=CENTER)

        self.zoom_out_button = Button(self.toolbar_frame, text="Zoom Out", width=8, bg='#4e4e4e', fg='white',
                                       command=self.zoom_out)
        self.zoom_out_button.place(relx=0.74, rely=0.5, anchor=CENTER)

        self.main_canvas_frame = Frame(self.windows, width=width, height=height-50)
        self.main_canvas_frame.place(relx=0, rely=0.08)

        self.main_canvas = Canvas(self.main_canvas_frame, bg='white', width=width-15, height=height-72)
        self.main_canvas.place(relx=0, rely=0)

        self.v_scroll = Scrollbar(self.main_canvas_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.v_scroll.place(relx=0.97, rely=0, relheight=0.97)

        self.h_scroll = Scrollbar(self.windows, orient=HORIZONTAL, command=self.main_canvas.xview)
        self.h_scroll.place(relx=0, rely=0.966, relwidth=1)

        self.main_canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        self.windows.bind("<Configure>", self.on_resize)

        self.windows.mainloop()

# ------------------------------------------------------- Methods ------------------------------------------------------
# ------------------------------------------------------ Open File -----------------------------------------------------
    def open_pdf_file(self):

        file_pathe =filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_pathe:
            self.document_size = pymupdf.open(file_pathe)
            self.page_images = []
            self.current_page = 0
            self.zoom_factor = 1.0

            self.page_number_label = Label(self.toolbar_frame, text="Page: 0/0", width=8, bg='#4e4e4e', fg='white')
            self.page_number_label.place(relx=0.95, rely=0.5, anchor=CENTER)

            for page in self.document_size:
                pixelas = page.get_pixmap(dpi=150)
                page_image = Image.frombytes("RGB", [pixelas.width, pixelas.height], pixelas.samples)
                self.page_images.append(page_image)

            self.show_page()

# ----------------------------------------------------- Display Page ---------------------------------------------------
    def show_page(self):
        if self.document_size:
            total = len(self.page_images)
            img = self.page_images[self.current_page]

            # Fit to width
            canvas_width = self.main_canvas.winfo_width()
            ratio = (canvas_width / img.width) * self.zoom_factor
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            self.tk_img = ImageTk.PhotoImage(resized_img)
            self.main_canvas.delete("all")
            self.main_canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
            self.main_canvas.config(scrollregion=self.main_canvas.bbox(ALL))

            self.page_number_label.config(text=f"Page: {self.current_page + 1}/{total}")

# ------------------------------------------------- Next / Previous Page -----------------------------------------------
    def next_page(self):
        if self.document_size and self.current_page < len(self.page_images) - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.document_size and self.current_page > 0:
            self.current_page -= 1
            self.show_page()

# ---------------------------------------------------- Zoom In / Out ---------------------------------------------------
    def zoom_in(self):
        if self.document_size:
            self.zoom_factor *= 1.2
            self.show_page()

    def zoom_out(self):
        if self.document_size:
            self.zoom_factor /= 1.2
            self.show_page()

# ---------------------------------------------------- Resize Window ---------------------------------------------------
    def on_resize(self, event):
        if self.document_size:
            self.show_page()

# -------------------------------------------------- Run the Program ---------------------------------------------------
if __name__ == "__main__":
    MyOwnPDFViewer()
