from PIL import Image, ImageTk
import os
import tkinter as tk

class ImageHelper:
    _cache = {}

    @staticmethod
    def load_image(path, size=None):
        """
        Load an image from path, resize it if size is provided (width, height),
        and return a ImageTk.PhotoImage. Caches the result.
        """
        cache_key = (path, size)
        if cache_key in ImageHelper._cache:
            return ImageHelper._cache[cache_key]

        if not os.path.exists(path):
            # Return a placeholder
            img = Image.new('RGB', size if size else (100, 100), color='#bdc3c7')
        else:
            try:
                img = Image.open(path)
                if size:
                    img = img.resize(size, Image.Resampling.LANCZOS)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                img = Image.new('RGB', size if size else (100, 100), color='#e74c3c')

        photo = ImageTk.PhotoImage(img)
        ImageHelper._cache[cache_key] = photo
        return photo

    @staticmethod
    def get_vehicle_image(model, size=(150, 100)):
        """
        Smart lookup for vehicle images based on model name.
        """
        base_path = os.path.join(os.path.dirname(__file__), "..", "img", "vehicles")
        
        # Clean model name for filename matching
        clean_model = model.replace(" ", "")
        
        candidates = [
            f"{model}.jpg", f"{model}.png",
            f"{model.lower()}.jpg", f"{model.lower()}.png",
            f"{clean_model}.jpg", f"{clean_model}.png",
            f"{clean_model.lower()}.jpg", f"{clean_model.lower()}.png"
        ]
        
        image_path = None
        for c in candidates:
            p = os.path.join(base_path, c)
            if os.path.exists(p):
                image_path = p
                break
        
        if not image_path:
            # Fallback to a default image if available, or just use the first candidate path (which will trigger placeholder)
            image_path = os.path.join(base_path, "default.png")

        return ImageHelper.load_image(image_path, size)

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=kwargs.get("bg", "white"), highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get("bg", "white"))

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg_color, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent.cget("bg"), **kwargs)
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.width = width
        self.height = height
        
        # Draw the rounded background
        self.round_rect = self._draw_rounded_rect(0, 0, width, height, corner_radius, bg_color)
        
        # Container for widgets
        self.inner_frame = tk.Frame(self, bg=bg_color)
        self.create_window((width/2, height/2), window=self.inner_frame, anchor="center")

    def _draw_rounded_rect(self, x, y, w, h, r, color):
        points = [
            x+r, y,
            x+w-r, y,
            x+w, y,
            x+w, y+r,
            x+w, y+h-r,
            x+w, y+h,
            x+w-r, y+h,
            x+r, y+h,
            x, y+h,
            x, y+h-r,
            x, y+r,
            x, y
        ]
        return self.create_polygon(points, smooth=True, fill=color)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg_color, fg_color, text, command=None, font=("Segoe UI", 10, "bold"), **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent.cget("bg"), **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        self.rect = self._draw_rounded_rect(0, 0, width, height, corner_radius, bg_color)
        self.text = self.create_text(width/2, height/2, text=text, fill=fg_color, font=font)
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Bind click on text as well
        self.tag_bind(self.text, "<Button-1>", self._on_click)
        self.tag_bind(self.text, "<Enter>", self._on_enter)
        self.tag_bind(self.text, "<Leave>", self._on_leave)

    def _draw_rounded_rect(self, x, y, w, h, r, color):
        points = [
            x+r, y,
            x+w-r, y,
            x+w, y,
            x+w, y+r,
            x+w, y+h-r,
            x+w, y+h,
            x+w-r, y+h,
            x+r, y+h,
            x, y+h,
            x, y+h-r,
            x, y+r,
            x, y
        ]
        return self.create_polygon(points, smooth=True, fill=color)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        # Lighten the color slightly
        self.itemconfig(self.rect, fill=self._adjust_color(self.bg_color, 20))

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)

    def _adjust_color(self, hex_color, amount):
        # Simple color adjustment
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            new_rgb = tuple(min(255, max(0, c + amount)) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
        except:
            return hex_color
