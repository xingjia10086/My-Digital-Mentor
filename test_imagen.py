import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GOOGLE_API_KEY", "")
client = genai.Client(api_key=API_KEY)

print("Testing Imagen 3...")
try:
    result = client.models.generate_images(
        model='imagen-3.0-generate-001',
        prompt='A minimalist business desk with a coffee cup and a laptop, highly detailed, photorealistic, cinematic lighting',
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
            aspect_ratio="1:1"
        )
    )
    
    for i, generated_image in enumerate(result.generated_images):
        with open(f"test_image_{i}.jpg", "wb") as f:
            f.write(generated_image.image.image_bytes)
    print("Success! Image saved as test_image_0.jpg.")
except Exception as e:
    print(f"Error generating image: {e}")
