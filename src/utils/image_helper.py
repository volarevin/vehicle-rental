from PIL import Image, ImageTk
import os

class ImageHelper:
    @staticmethod
    def load_resized_image(path, size=(150, 100)):
        """
        Loads an image from the path, resizes it to the specified size,
        and returns a ImageTk.PhotoImage object.
        If the image is not found, returns None or a placeholder if you have one.
        """
        if not os.path.exists(path):
            # You might want to return a default placeholder image here
            # For now, we'll just return None so the UI can handle it (e.g. show text)
            return None
            
        try:
            img = Image.open(path)
            # Resize using LANCZOS for high quality downsampling
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
