from PIL import Image, ImageTk
import os
import tkinter as tk
import tkinter.font as tkfont
from src.utils.image_helper import ImageHelper

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=kwargs.get("bg", "white"), highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get("bg", "white"))
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack Scrollbar FIRST to ensure it's visible
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mousewheel only when mouse is over the widget to prevent conflicts
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_enter(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_leave(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width=100, height=100, corner_radius=10, bg_color="white", **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent.cget("bg"), **kwargs)
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.base_height = height
        self.round_rect = self._draw_rounded_rect(0, 0, width, height, corner_radius, bg_color)
        self.inner_frame = tk.Frame(self, bg=bg_color)
        self.inner_window = self.create_window((width/2, height/2), window=self.inner_frame, anchor="center")
        
        self.bind("<Configure>", self._on_resize)
        self.inner_frame.bind("<Configure>", self._on_inner_configure)

    def _on_inner_configure(self, event):
        required_height = max(self.base_height, event.height + 24)
        current_height = int(float(self.cget("height")))
        if required_height != current_height:
            self.configure(height=required_height)

    def _on_resize(self, event):
        self.delete(self.round_rect)
        self.coords(self.inner_window, event.width/2, event.height/2)
        self.round_rect = self._draw_rounded_rect(0, 0, event.width, event.height, self.corner_radius, self.bg_color)
        self.tag_lower(self.round_rect)

    def _draw_rounded_rect(self, x, y, w, h, r, color):
        points = [
            x+r, y, x+w-r, y, x+w, y, x+w, y+r, x+w, y+h-r, x+w, y+h,
            x+w-r, y+h, x+r, y+h, x, y+h, x, y+h-r, x, y+r, x, y
        ]
        return self.create_polygon(points, smooth=True, fill=color)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg_color, fg_color, text, command=None, image_path=None, icon_size=(30, 30), font=("Segoe UI", 10, "bold"), text_align="left", **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent.cget("bg"), **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        self.rect = self._draw_rounded_rect(0, 0, width, height, corner_radius, bg_color)
        
        if image_path and os.path.exists(image_path):
            self.icon_image = ImageHelper.load_image(image_path, icon_size)
            if text_align == "center":
                font_obj = tkfont.Font(font=font)
                text_width = font_obj.measure(text)
                spacing = 8
                group_width = icon_size[0] + spacing + text_width
                start_x = max(8, (width - group_width) / 2)
                icon_x = start_x + (icon_size[0] / 2)
                text_x = start_x + icon_size[0] + spacing
                self.create_image(icon_x, height/2, image=self.icon_image, anchor="center")
                self.text = self.create_text(text_x, height/2, text=text, fill=fg_color, font=font, anchor="w")
            else:
                self.create_image(40, height/2, image=self.icon_image, anchor="center")
                self.text = self.create_text(70, height/2, text=text, fill=fg_color, font=font, anchor="w")
        else:
            self.text = self.create_text(width/2, height/2, text=text, fill=fg_color, font=font, anchor="center")
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self.tag_bind(self.text, "<Button-1>", self._on_click)
        self.tag_bind(self.text, "<Enter>", self._on_enter)
        self.tag_bind(self.text, "<Leave>", self._on_leave)

    def _draw_rounded_rect(self, x, y, w, h, r, color):
        points = [
            x+r, y, x+w-r, y, x+w, y, x+w, y+r, x+w, y+h-r, x+w, y+h,
            x+w-r, y+h, x+r, y+h, x, y+h, x, y+h-r, x, y+r, x, y
        ]
        return self.create_polygon(points, smooth=True, fill=color)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self._adjust_color(self.bg_color, 20))

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)

    def _adjust_color(self, hex_color, amount):
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            new_rgb = tuple(min(255, max(0, c + amount)) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
        except:
            return hex_color