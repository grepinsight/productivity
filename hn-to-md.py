import requests
from bs4 import BeautifulSoup


def convert_to_markdown(url):
    # Send a GET request to the Hacker News page
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the comment and related data
    comment_section = soup.find_all("tr", class_="athing")  # Find all comment sections

    if not comment_section:
        print("No comment found!")
        return

    # Prepare Markdown file content
    markdown_content = []

    for comment in comment_section:
        # Extract the comment text
        comment_text = comment.find("div", class_="comment").text.strip()
        # Extract the author name
        author = comment.find("a", class_="hnuser")
        author_name = author.text if author else "Anonymous"

        # Add comment and author information to markdown content
        markdown_content.append(f"### Comment by {author_name}\n")
        markdown_content.append(f"```\n{comment_text}\n```\n")

    # Save the content to a markdown file
    with open("hacker_news_comment.md", "w") as file:
        file.write("\n".join(markdown_content))

    print("Markdown file has been created: hacker_news_comment.md")


# Example URL of a Hacker News comment
url = "https://news.ycombinator.com/item?id=42838700"
convert_to_markdown(url)
