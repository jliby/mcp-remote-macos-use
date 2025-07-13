"""Utility module for screenshot management."""
import os
from threading import Lock

class ScreenshotCounter:
    """A thread-safe counter for generating screenshot indices."""
    _instance = None
    _lock = Lock()
    _count = 0
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of ScreenshotCounter."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def get_next_index(self):
        """Get the next screenshot index in a thread-safe manner."""
        with self._lock:
            self._count += 1
            return self._count
    
    def reset(self):
        """Reset the counter (mainly for testing)."""
        with self._lock:
            self._count = 0
    
    @property
    def current_count(self):
        """Get the current count without incrementing."""
        with self._lock:
            return self._count


def get_next_screenshot_index():
    """Get the next screenshot index."""
    return ScreenshotCounter.get_instance().get_next_index()


def initialize_screenshot_counter():
    """Initialize the screenshot counter based on existing files."""
    screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Find all existing screenshot files
    existing_indices = []
    for filename in os.listdir(screenshots_dir):
        if filename.startswith("screenshot_") and filename.endswith(".png"):
            try:
                # Extract the index from filenames in format screenshot_YYYYMMDD_HHMMSS_index_uniqueid.png
                parts = filename.split("_")
                if len(parts) >= 4:  # We need at least 4 parts for the new format
                    index_str = parts[3]  # The index should be the 4th part (0-indexed)
                    if index_str.isdigit():
                        existing_indices.append(int(index_str))
            except Exception:
                # Skip files that don't match our expected format
                pass
    
    # Set the counter to the highest existing index (or 0 if none found)
    max_index = max(existing_indices) if existing_indices else 0
    counter = ScreenshotCounter.get_instance()
    counter._count = max_index  # Direct access for initialization only
    
    return max_index
