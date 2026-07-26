from pathlib import Path
from uuid import uuid4
from PIL import Image
from config import ALLOWED_IMAGE_EXTENSIONS, MAX_UPLOAD_MB, UPLOAD_SUBDIRS, BASE_DIR

def save_uploaded_image(uploaded_file, category: str):
    if uploaded_file is None:
        return None
    if category not in UPLOAD_SUBDIRS:
        raise ValueError("Invalid upload category.")
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Only PNG, JPG, JPEG, and WEBP images are allowed.")
    data = uploaded_file.getvalue()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValueError(f"Image exceeds the {MAX_UPLOAD_MB} MB size limit.")
    try:
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as img:
            img.verify()
            fmt = (img.format or "").lower()
            if fmt not in {"png", "jpeg", "webp"}:
                raise ValueError("Unsupported or invalid image type.")
    except Exception as exc:
        raise ValueError("The uploaded file is not a valid image.") from exc
    filename = f"{uuid4().hex}{suffix}"
    destination = UPLOAD_SUBDIRS[category] / filename
    destination.write_bytes(data)
    return str(destination.relative_to(BASE_DIR))
