from ocr import read_image, preprocess_image, extract_text

def main():
    image_path = 'path_to_your_image.jpg'  # Change this to your image path
    image = read_image(image_path)
    processed_image = preprocess_image(image)
    text = extract_text(processed_image)
    print(text)

if __name__ == "__main__":
    main()
