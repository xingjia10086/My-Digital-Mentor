from vertexai.preview.vision_models import ImageGenerationModel
import traceback

def test_model(model_name):
    print(f"Trying {model_name}...")
    try:
        model = ImageGenerationModel.from_pretrained(model_name)
        print(f"Success loading {model_name}")
        # Test generation
        resp = model.generate_images("A cute cat", number_of_images=1)
        print(f"Generation successful for {model_name}")
    except Exception as e:
        print(f"Error for {model_name}: {type(e).__name__}: {e}")

test_model("gemini-2.5-flash-image")
test_model("gemini-2.5-flash-image-preview")
test_model("imagen-3.0-generate-001")
test_model("imagegeneration@006")
test_model("imagegeneration@005")
