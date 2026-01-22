import numpy as np
import os
from PIL import Image


class ImageProcessor:
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.original_image = None
        self.processed_image = None
        self.arr = None
        
        if image_path: self.load_image(image_path)
    
    def load_image(self, image_path):
        self.image_path = image_path
        self.original_image = Image.open(image_path)
        self.arr = np.array(self.original_image)
        self.processed_image = self.original_image.copy()
        print(f"Image loaded. Size: {self.original_image.size}")
        
        return self
    
    def compress(self, factor=2):
        if self.arr is None: raise ValueError("Load image first!")
        
        height, width = self.arr.shape[:2]
        
        new_height = height - (height % factor)
        new_width = width - (width % factor)
        arr_cropped = self.arr[:new_height, :new_width]
        
        new_shape = (new_height // factor, factor, new_width // factor, factor, 3)
        arr_reshaped = arr_cropped.reshape(new_shape)
        
        self.arr = arr_reshaped.mean(axis=(1, 3)).astype(np.uint8)
        
        self.processed_image = Image.fromarray(self.arr)
        print(f"Image compressed. New size: {self.processed_image.size}")
        
        return self
    
    def to_grayscale(self, weights=(0.5, 0.3, 0.2)):
        if self.arr is None: raise ValueError("Load image first!")
        
        r_weight, g_weight, b_weight = weights
        grayscale = (
            self.arr[:, :, 0] * r_weight +
            self.arr[:, :, 1] * g_weight +
            self.arr[:, :, 2] * b_weight
        ).astype(np.uint8)
        
        self.arr[:, :, 0] = grayscale
        self.arr[:, :, 1] = grayscale
        self.arr[:, :, 2] = grayscale
        
        self.processed_image = Image.fromarray(self.arr)
        print("Image converted to grayscale")
        
        return self
    
    def adjust_brightness(self, percent):
        if self.arr is None: raise ValueError("Load image first!")
        if not (-100 <= percent <= 100): raise ValueError("Percentage must be from -100 to 100")
        
        factor = 1 + percent / 100
        
        for channel in range(3):
            channel_data = self.arr[:, :, channel].astype(np.float32)
            channel_data = channel_data * factor
            channel_data = np.clip(channel_data, 0, 255)
            self.arr[:, :, channel] = channel_data.astype(np.uint8)
        
        self.processed_image = Image.fromarray(self.arr)
        print(f"Brightness changed by {percent}%")
        
        return self
    
    def save(self, output_path=None):
        if self.processed_image is None: raise ValueError("No processed image to save!")
        
        if output_path is None:
            if self.image_path:
                dir_name = os.path.dirname(self.image_path)
                file_name = os.path.basename(self.image_path)
                name, ext = os.path.splitext(file_name)
                output_path = os.path.join(dir_name, f"{name}_processed{ext}")
                
            else: output_path = "processed_image.jpg"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        self.processed_image.save(output_path)
        print(f"Image saved: {output_path}")
        
        return output_path
    
    def show(self):
        if self.processed_image: self.processed_image.show()
        
        return self
    
    def reset(self):
        if self.original_image:
            self.arr = np.array(self.original_image)
            self.processed_image = self.original_image.copy()
            print("Image reset to original")
            
        return self
    
    def get_stats(self):
        if self.arr is None: return None
        
        stats = {
            "size": self.processed_image.size if self.processed_image else None,
            "shape": self.arr.shape,
            "dtype": self.arr.dtype,
            "min_values": [self.arr[:, :, i].min() for i in range(3)],
            "max_values": [self.arr[:, :, i].max() for i in range(3)],
            "mean_values": [self.arr[:, :, i].mean() for i in range(3)],
        }
        
        return stats