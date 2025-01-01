from datetime import datetime

from django.utils.formats import date_format
from django.utils.html import format_html


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


class AdminExifMixin:
    def exif_make_and_model(self, obj):
        if obj.exif:
            make = obj.exif.get("make")
            model = obj.exif.get("model")
            return f"{make} {model}"
        return "-"

    exif_make_and_model.short_description = "Camera"

    def exif_lens(self, obj):
        if obj.exif:
            lens = obj.exif.get("lens")
            return lens
        return "-"

    exif_lens.short_description = "Lens"

    def exif_focal_length(self, obj):
        if obj.exif:
            focal_length = obj.exif.get("focal_length")
            return focal_length
        return "-"

    exif_focal_length.short_description = "Focal length"

    def exif_aperture(self, obj):
        if obj.exif:
            aperture = obj.exif.get("aperture")
            return format_html(f"&fnof;/{aperture}")
        return "-"

    exif_aperture.short_description = "Aperture"

    def exif_shutter(self, obj):
        if obj.exif:
            shutter = obj.exif.get("shutter")
            return shutter
        return "-"

    exif_shutter.short_description = "Shutter speed"

    def exif_iso(self, obj):
        if obj.exif:
            iso = obj.exif.get("iso")
            return iso
        return "-"

    exif_iso.short_description = "ISO"

    def exif_shot_at(self, obj):
        if obj.exif:
            shot_at = obj.exif.get("shot_at")
            return date_format(datetime.fromisoformat(shot_at), "DATETIME_FORMAT")
        return "-"

    exif_shot_at.short_description = "Shot at"

    def get_readonly_fields(self, *args, **kwargs):
        readonly_fields = super().get_readonly_fields(*args, **kwargs)
        return readonly_fields + (
            "exif_make_and_model",
            "exif_lens",
            "exif_focal_length",
            "exif_aperture",
            "exif_shutter",
            "exif_iso",
            "exif_shot_at",
        )

    def get_list_display(self, *args, **kwargs):
        list_display = super().get_list_display(*args, **kwargs)
        return list_display + (
            "exif_shot_at",
            "exif_make_and_model",
            "exif_lens",
        )
