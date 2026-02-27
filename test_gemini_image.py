import traceback
from vertexai.preview.vision_models import ImageGenerationModel
from google import genai
import os

print("Testing ImageGenerationModel with gemini-2.5-flash-image")
try:
    model1 = ImageGenerationModel.from_pretrained("gemini-2.5-flash-image")
    print("Success load gemini-2.5-flash-image via vertex")
except Exception as e:
    print(f"Error vertex: {e}")

print("Testing GenAI API")
try:
    client = genai.Client() # Assumes GOOGLE_CLOUD_PROJECT is set
    resp = client.models.generate_images(
        model="gemini-2.5-flash-image",
        prompt="A cute cat"
    )
    print("Success load via GenAI API")
except Exception as e:
    print(f"Error GenAI: {e}")

print("Testing imagen-3.0-generate-002")
try:
    model1 = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    print("Success load imagen-3.0-generate-002 via vertex")
except Exception as e:
    print(f"Error vertex: {e}")
