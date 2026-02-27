import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "gen-lang-client-0834352502"
LOCATION = "us-central1"

print("Initializing Vertex AI...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

print("Loading Imagen 3 model...")
model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

print("Generating image...")
try:
    images = model.generate_images(
        prompt="A minimalist business desk with a coffee cup and a laptop, highly detailed, photorealistic, cinematic lighting",
        number_of_images=1,
        aspect_ratio="1:1"
    )
    
    images[0].save(location="test_image_vertex.jpg")
    print("Success! Image saved as test_image_vertex.jpg.")
except Exception as e:
    print(f"Error generating image: {e}")
