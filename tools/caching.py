import os

CACHE_DIR = ".aoc_cache"


def _make_cache_dir() -> None:
    """Create the cache directory if it doesn't exist."""
    if not os.path.exists(os.path.join(os.getcwd(), CACHE_DIR)):
        os.mkdir(os.path.join(os.getcwd(), CACHE_DIR))


def _cache_filename(year: int, day: int) -> str:
    """Get the filename for cached data."""
    return os.path.join(os.getcwd(), CACHE_DIR, f"{year}_{day:02d}.txt")


def _data_is_cached(year: int, day: int) -> bool:
    """Check if the data for a given day is cached."""
    return os.path.exists(_cache_filename(year, day))


def _load_cached_data(year: int, day: int) -> str:
    """Load data from the cache."""
    with open(_cache_filename(year, day), "r") as f:
        return "".join(f.readlines())


def _cache_data(year: int, day: int, data: str) -> None:
    """Cache data for a given day."""
    with open(_cache_filename(year, day), "w") as f:
        f.write(data)
