from PIL import Image, ImageTk
import os

class ImageHelper:
    _cache = {}

    @staticmethod
    def load_image(path, size=None):
        # Create a cache key from the path and size
        cache_key = (path, size)
        
        # Check if the image is already in the cache
        if cache_key in ImageHelper._cache:
            return ImageHelper._cache[cache_key]

        if not os.path.exists(path):
            # Return a placeholder image if the path does not exist
            # Create a simple colored image
            if size:
               img = Image.new('RGB', size, color='#bdc3c7')
            else:
               img = Image.new('RGB', (100, 100), color='#bdc3c7')
        else:
            try:
                img = Image.open(path)
                if size:
                    # Use LANCZOS for high-quality downsampling
                    img = img.resize(size, Image.Resampling.LANCZOS)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                if size:
                   img = Image.new('RGB', size, color='#e74c3c')
                else:
                   img = Image.new('RGB', (100, 100), color='#e74c3c')

        # Convert the PIL image to a Tkinter PhotoImage
        photo = ImageTk.PhotoImage(img)
        
        # Add the PhotoImage to the cache
        ImageHelper._cache[cache_key] = photo
        
        return photo

    @staticmethod
    def load_resized_image(path, size=(150, 100)):
        return ImageHelper.load_image(path, size)

    @staticmethod
    def get_vehicle_image_path(model):
        # Construct the base path relative to this file
        base_path = os.path.join(os.path.dirname(__file__), "..", "img", "vehicles")
        # Ensure base_path is absolute
        base_path = os.path.abspath(base_path)

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
            # Fallback
            image_path = os.path.join(base_path, "default.png")
            if not os.path.exists(image_path):
                 # Try absolute fallback if relative fail
                 pass
            
        return image_path

    @staticmethod
    def get_vehicle_image(model, size=(150, 100)):
        path = ImageHelper.get_vehicle_image_path(model)
        return ImageHelper.load_image(path, size)
