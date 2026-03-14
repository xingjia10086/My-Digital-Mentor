import os
import sys
import traceback

try:
    from fish_audio_sdk import Session, TTSRequest
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

FISH_AUDIO_API_KEY = os.environ.get("FISH_AUDIO_API_KEY", "")


def test_fish_audio():
    if not FISH_AUDIO_API_KEY:
        print("Missing FISH_AUDIO_API_KEY environment variable.")
        return

    print("Initialize Fish Audio Session...")
    try:
        session = Session(FISH_AUDIO_API_KEY)
        text_to_speak = "你好，星佳导师！这是重新测试。"

        print("Generating audio...")
        with open("test_fish_audio.mp3", "wb") as f:
            for chunk in session.tts(TTSRequest(text=text_to_speak, reference_id=None)):
                f.write(chunk)

        print("Success! Audio saved as test_fish_audio.mp3")

    except Exception as e:
        print("Expected Exception Details:")
        print(f"Error Type: {type(e)}")
        print(f"Error Message: {str(e)}")
        import httpx

        if isinstance(e, httpx.HTTPError):
            print(
                "Response Content: "
                f"{e.response.text if hasattr(e, 'response') and e.response else 'No response content'}"
            )
        traceback.print_exc()


if __name__ == "__main__":
    test_fish_audio()
