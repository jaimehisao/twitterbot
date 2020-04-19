import re


def process_text(text) -> str:
    """Removes text from tweets that can impact the model negatively."""
    text = re.sub(r'http\S+', '', text)  # Removes URLs included in the Tweet
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)  # Remove @ mentions in Tweets
    text = text.strip(" ")  # Remove whitespace characters resulting from previus operations
    text = re.sub(r' +', ' ', text)  # Remove redundant spaces (extra)

    # Handle and remove common HTML entities
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    return text
