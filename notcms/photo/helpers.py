from datetime import datetime


def get_fractional_value(formatted: str) -> float:
    if "/" in formatted:
        numerator, denominator = map(float, formatted.split("/"))
        return numerator / denominator
    return float(formatted)


def format_focal_length(focal_length: str) -> str:
    if not focal_length:
        return "N/A"

    focal_length_value = get_fractional_value(focal_length)
    return f"{round(focal_length_value, 0)}mm"


def format_aperture(aperture: str) -> str:
    if not aperture:
        return "N/A"

    aperture_value = get_fractional_value(aperture)
    return f"{round(aperture_value, 1)}"


def format_shutter_speed(shutter_speed: str) -> str:
    if not shutter_speed:
        return "N/A"

    shutter_speed_value = get_fractional_value(shutter_speed)
    if (1 / shutter_speed_value) > 1:
        return f"1/{int(1 / shutter_speed_value)}"
    return f"{shutter_speed_value:.2f} sec"


def reformat_exif_datetime(exif_shot_at: str) -> str:
    if not exif_shot_at:
        return "N/A"
    parsed_datetime = datetime.strptime(exif_shot_at, "%Y:%m:%d %H:%M:%S")
    return parsed_datetime.isoformat()


def filter_exif(tags):
    return {
        "make": tags.get("Image Make"),
        "model": tags.get("Image Model"),
        "lens": tags.get("EXIF LensModel"),
        "focal_length": format_focal_length(tags.get("EXIF FocalLength")),
        "aperture": format_aperture(tags.get("EXIF FNumber")),
        "shutter": format_shutter_speed(tags.get("EXIF ExposureTime")),
        "iso": tags.get("EXIF ISOSpeedRatings"),
        "shot_at": reformat_exif_datetime(tags.get("EXIF DateTimeOriginal")),
    }
