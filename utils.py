import os
from itertools import zip_longest
from .constants import CHROME_DRIVER, FIREFOX_DRIVER


def grouper(iterable, n, fill_value=None):
    """
    Iterate data into fixed-length chunks or blocks.

    Example:
    Iterating array with n = 2
    [N1, N2, N3, N4, N5, N6]

    Iterations:
    (N1, N2) -> (N3, N4) -> (N5, N6)
    Args:
        iterable: base iterable
        n: the fixed-length of the chunks or blocks that will be iterated by
        fill_value: constant value to fill chunks with less data then the fixed-value

    Returns:

    """
    args = [iter(iterable)] * n

    return zip_longest(*args, fillvalue=fill_value)


def path_browser_driver(is_chrome: bool, path: str) -> str:
    """
    Checking if the driver is correctly located on the path
    Args:
        is_chrome: Boolean indicating if the selected browser is Chrome
        path: Path of the browser driver

    Returns:
        Optional[str]: The path on which the driver is located, None if not found
    """
    driver_name = CHROME_DRIVER if is_chrome else FIREFOX_DRIVER

    if driver_name not in path and not os.path.isdir(path):
        raise ValueError(f'{driver_name} not found in path')
    elif os.path.isdir(path):
        path = os.path.join(path, driver_name)

    if not os.path.isfile(path):
        raise FileNotFoundError(f'{path} not found.')

    return path
