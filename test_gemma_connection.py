from pathlib import Path

from backend.services.gemma_service import analyze_civic_issue


# Change this to an actual image on your computer
IMAGE_PATH = Path("OIP.jpg")


if not IMAGE_PATH.exists():
    raise FileNotFoundError(
        f"Put a test image at: {IMAGE_PATH.absolute()}"
    )


image_bytes = IMAGE_PATH.read_bytes()

result = analyze_civic_issue(
    image_bytes=image_bytes,
    mime_type="image/jpeg",
    description="There appears to be a damaged area on the road.",
    location="Lucknow, Uttar Pradesh"
)

print("\n================ GEMMA ANALYSIS ================\n")
print(result)
print("\n=================================================\n")