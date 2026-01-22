import os
from image_processing import ImageProcessor


def display_menu():
    print("\n" + "="*50)
    print("          IMAGE EDITOR")
    print("="*50)
    print("1. Compress image")
    print("2. Convert to grayscale")
    print("3. Adjust brightness")
    print("4. Combined processing")
    print("5. Show current image")
    print("6. Show statistics")
    print("7. Reset to original")
    print("8. Save result")
    print("9. Load new image")
    print("0. Exit")
    print("-"*50)


def load_image_interactive():
    while True:
        print("\nLoad image")
        print("1. Use default image")
        print("2. Specify custom path")
        
        choice = input("Choose option (1-2): ").strip()
        
        if choice == "1":
            explore = os.path.dirname(__file__)
            image_path = os.path.join(explore, "images", "image.jpg")
            
            if os.path.exists(image_path): return image_path
            else:
                print(f"File not found: {image_path}")
                print("Please place image in images/ folder")
                
        elif choice == "2":
            custom_path = input("Enter full image path: ").strip()
            
            if os.path.exists(custom_path): return custom_path
            else: print(f"File not found: {custom_path}")
        
        else: print("Invalid choice. Try again.")


def main():
    image_path = load_image_interactive()
    
    processor = ImageProcessor(image_path)
    print(f"\nImage loaded: {image_path}")
    
    while True:
        display_menu()
        choice = input("Choose action (0-9): ").strip()
        
        if choice == "0":
            print("Exiting program. Goodbye!")
            break
        
        elif choice == "1":
            print("\n=== IMAGE COMPRESSION ===")
            try:
                factor = int(input("Enter compression factor (2, 3, 4...): "))
                if factor > 1:
                    processor.compress(factor=factor)
                    print(f"Image compressed {factor} times")
                    
                else: print("Factor must be greater than 1")
                
            except ValueError: print("Error: enter integer number")
        
        elif choice == "2":
            print("\n=== GRAYSCALE CONVERSION ===")
            print("Use standard weights (0.5, 0.3, 0.2) or custom?")
            weight_choice = input("1 - standard, 2 - custom: ").strip()
            
            if weight_choice == "1": processor.to_grayscale(weights=(0.5, 0.3, 0.2))
            
            elif weight_choice == "2":
                try:
                    r = float(input("Weight for red channel (R): "))
                    g = float(input("Weight for green channel (G): "))
                    b = float(input("Weight for blue channel (B): "))
                    processor.to_grayscale(weights=(r, g, b))
                    
                except ValueError: print("Error: enter numbers")
                
            else: processor.to_grayscale()
            
            print("Image converted to grayscale")
        
        elif choice == "3":
            print("\n=== BRIGHTNESS ADJUSTMENT ===")
            try:
                percent = int(input("Enter brightness percentage (-100 to 100): "))
                if -100 <= percent <= 100:
                    processor.adjust_brightness(percent)
                    print(f"Brightness adjusted by {percent}%")
                    
                else: print("Percentage must be from -100 to 100")
                
            except ValueError: print("Error: enter integer number")
        
        elif choice == "4":
            print("\n=== COMBINED PROCESSING ===")
            print("Available options:")
            print("1. Grayscale → +30% brightness → 2x compression")
            print("2. 2x compression → Grayscale → +20% brightness")
            print("3. +50% brightness → Grayscale")
            print("4. Configure custom chain")
            
            combo_choice = input("Choose option (1-4): ").strip()
            
            if combo_choice == "1":
                (processor
                 .to_grayscale()
                 .adjust_brightness(30)
                 .compress(2))
                print("Applied chain: Grayscale → +30% brightness → 2x compression")
            
            elif combo_choice == "2":
                (processor
                 .compress(2)
                 .to_grayscale()
                 .adjust_brightness(20))
                print("Applied chain: 2x compression → Grayscale → +20% brightness")
            
            elif combo_choice == "3":
                (processor
                 .adjust_brightness(50)
                 .to_grayscale())
                print("Applied chain: +50% brightness → Grayscale")
            
            elif combo_choice == "4":
                chain = []
                while True:
                    print("\nCurrent chain:", chain if chain else "empty")
                    print("Add operation:")
                    print("1. Compression")
                    print("2. Grayscale")
                    print("3. Brightness")
                    print("4. Finish configuration")
                    
                    op_choice = input("Choose operation (1-4): ").strip()
                    
                    if op_choice == "1":
                        try:
                            factor = int(input("Compression factor: "))
                            chain.append(("compress", factor))
                            
                        except ValueError: print("Input error")
                    
                    elif op_choice == "2":
                        chain.append(("grayscale", None))
                        print("Added grayscale conversion")
                    
                    elif op_choice == "3":
                        try:
                            percent = int(input("Brightness percentage: "))
                            chain.append(("brightness", percent))
                            
                        except ValueError: print("Input error")
                    
                    elif op_choice == "4": break
                    else: print("Invalid choice")
                
                for operation, param in chain:
                    if operation == "compress": processor.compress(param)
                    elif operation == "grayscale": processor.to_grayscale()
                    elif operation == "brightness": processor.adjust_brightness(param)
                
                print(f"Applied custom chain of {len(chain)} operations")
            
            else: print("Invalid choice")
        
        elif choice == "5":
            print("\nOpening image...")
            processor.show()
        
        elif choice == "6":
            print("\n=== IMAGE STATISTICS ===")
            stats = processor.get_stats()
            if stats:
                print(f"Size: {stats['size']}")
                print(f"Array shape: {stats['shape']}")
                print(f"Minimum RGB values: {stats['min_values']}")
                print(f"Maximum RGB values: {stats['max_values']}")
                print(f"Average RGB values: {[round(x, 2) for x in stats['mean_values']]}")
        
        elif choice == "7":
            print("\n=== RESET ===")
            confirm = input("Are you sure? All changes will be lost. (y/n): ").lower()
            if confirm == 'y':
                processor.reset()
                print("Image reset to original")
        
        elif choice == "8":
            print("\n=== SAVE ===")
            print("1. Save near original (auto name)")
            print("2. Specify custom path")
            
            save_choice = input("Choose option (1-2): ").strip()
            
            if save_choice == "1":
                saved_path = processor.save()
                print(f"Saved: {saved_path}")
            
            elif save_choice == "2":
                custom_path = input("Enter full save path: ").strip()
                saved_path = processor.save(custom_path)
                print(f"Saved: {saved_path}")
            
            else: print("Invalid choice")
        
        elif choice == "9":
            print("\n=== LOAD NEW IMAGE ===")
            new_path = load_image_interactive()
            processor.load_image(new_path)
            print(f"New image loaded: {new_path}")
        
        else: print("Invalid choice. Try again.")
        
        input("\nPress Enter to continue...")


def batch_processing_example():
    print("\n=== BATCH PROCESSING EXAMPLE ===")
    
    image_dir = os.path.join(os.path.dirname(__file__), "images")
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        print(f"Created folder: {image_dir}")
        print("Place images in this folder and run again.")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    images = []
    
    for file in os.listdir(image_dir):
        if any(file.lower().endswith(ext) for ext in image_extensions): images.append(os.path.join(image_dir, file))
    
    if not images:
        print("No images found in images folder.")
        return
    
    print(f"Images found: {len(images)}")
    
    for i, image_path in enumerate(images, 1):
        print(f"\nProcessing {i}/{len(images)}: {os.path.basename(image_path)}")
        
        processor = ImageProcessor(image_path)
        
        (processor
         .to_grayscale()
         .adjust_brightness(10)
         .compress(2))
        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(image_dir, f"processed_{base_name}.jpg")
        processor.save(output_path)
        
        print(f"  → Saved: {output_path}")


print("="*60)
print("    WELCOME TO IMAGE EDITOR")
print("="*60)
    
print("\nWorking modes:")
print("1. Interactive mode (main)")
print("2. Batch processing of all images in folder")
    
mode_choice = input("Choose mode (1-2): ").strip()
    
if mode_choice == "1": main()
elif mode_choice == "2": batch_processing_example()
else: print("Invalid choice. Starting interactive mode...")