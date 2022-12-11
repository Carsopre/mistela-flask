import math
from pathlib import Path

from PIL import Image


def image_rescale(img_path: str, down_factor: float) -> Path:
    """
    Rescales the size of an image in the most optimal way so that its weight its reduced without giving up too much of its qualities.

    Args:
        img_path (str): Image path source.
        down_factor (float): Float factor to apply when rescaling.

    Returns:
        Path: Location of the new generated image.
    """
    # Verify input arguments
    assert img_path, "No image path provided."
    assert down_factor, "No downsizing factor provided."

    _img_path = Path(img_path)
    assert _img_path.is_file(), "No image found at {}".format(img_path)

    assert down_factor > 0, "Downsize factor needs to be greater than 0."

    _out_img_path = _img_path.with_stem(f"{_img_path.stem}_downsized")

    # Define auxiliar methods.
    def _to_new_factor(value: int) -> int:
        return math.ceil(value * down_factor)

    # Do action.
    with Image.open(_img_path) as _img_data:
        _img_width, _img_height = _img_data.size
        _new_img_data = _img_data.resize(
            (_to_new_factor(_img_width), _to_new_factor(_img_height))
        )
        _new_img_data.save(_out_img_path, optimize=True, quality=95)

    # Verify result.
    assert _out_img_path.is_file(), "Image was not downsized."
    return _out_img_path


def image_opacity(img_path: str, opacity_factor: int) -> Path:
    """
    Applies an alpha layer with a factor of `opacity_Factor` to the provided image at `img_path`.

    Args:
        img_path (str): Image path source.
        opacity_factor (int): Value of opacity as integer.

    Returns:
        Path: Location of the new generated image.
    """
    # Verify input arguments
    assert img_path, "No image path provided."
    assert opacity_factor, "No opacity factor provided."

    _img_path = Path(img_path)
    assert _img_path.is_file(), "No image found at {}".format(img_path)

    assert (
        opacity_factor > 0
    ), "Opacity factor needs to be an integer value greater than 0."

    _out_img_path = _img_path.with_name(f"{_img_path.stem}_opacity.png")

    # Do action
    with Image.open(_img_path) as _img_data:
        _rgba_img_data = _img_data.convert("RGBA")
        _rgba_img_data.putalpha(opacity_factor)
        # _rgb_img_data = _rgba_img_data.convert("RGB")
        _rgba_img_data.save(_out_img_path)

    # Verify result.
    assert _out_img_path.is_file(), "Opacity was not applied to image."
    return _out_img_path


_static_dir = Path(__file__).parent.parent / "static"
_hd_bck = _static_dir / "img" / "original.jpg"

_hd_opacity = image_opacity(_hd_bck, 170)
_hd_downsized = image_rescale(_hd_opacity, 0.25)
