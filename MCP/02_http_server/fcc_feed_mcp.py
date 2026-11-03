from fastmcp import FastMCP
import feedparser


mcp = FastMCP(name="Free Code Camp Feed Searcher MCP")

@mcp.tool(name="search_fcc_feed")
def search_fcc_feed(query: str, max_results: int = 3) -> list[dict]:
    """Searches the Free Code Camp feed for articles matching the query via RSS by Title/Description.

    Args:
        query (str): The search query.
        max_results (int, optional): The maximum number of results to return. Defaults to 3.

    Returns:
        list[str]|dict: A list of article titles matching the query, or a dictionary with a message if no articles are found.
    """
    feed_url = "https://www.freecodecamp.org/news/rss/"
    feed = feedparser.parse(feed_url)
    results = []

    for entry in feed.entries:
        if query.lower() in entry.title.lower() or query.lower() in entry.description.lower():
            results.append({"title": entry.title, "link": entry.link})

        if len(results) >= max_results:
            break

    return results or [{"message": "No articles found matching the query."}]


@mcp.tool(name="search_fcc_youtube_feed")
def search_fcc_youtube_feed(query: str, max_results: int = 3) -> list[dict]:
    """Searches the Free Code Camp YouTube feed for videos matching the query via RSS by Title.

    Args:
        query (str): The search query.
        max_results (int, optional): The maximum number of results to return. Defaults to 3.

    Returns:
        list[str]|dict: A list of video titles matching the query, or a dictionary with a message if no videos are found.
    """
    feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ"
    feed = feedparser.parse(feed_url)
    results = []

    for entry in feed.entries:
        if query.lower() in entry.title.lower():
            results.append({"title": entry.title, "link": entry.link})

        if len(results) >= max_results:
            break

    return results or [{"message": "No videos found matching the query."}]


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
