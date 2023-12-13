def validate_coords(coords: list[str], size: int) -> tuple:
    """Validate given coordinates so that they are Ints in a given range."""
    if len(coords) != 2:
        raise ValueError("Invalid value. Use the following format: 'X Y'")

    try:
        coords = tuple(int(x) for x in coords)
    except ValueError as ex:
        raise ValueError("Please provide two numbers.") from ex

    if not all([True if 0 <= x < size else False for x in coords]):
        raise ValueError(
            f"Values out of range. Please provide values from the range <0,{size})"
        )
    return coords


def validate_size(size: str) -> int:
    """Validate board size ,so it isn't too small or negative."""
    try:
        size = int(size)
    except ValueError as ex:
        raise ValueError("Please provide a number") from ex

    if size >= 3:
        return size
    raise ValueError("Size should be at least 3 or greater.")
