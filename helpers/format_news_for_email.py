from pydantic_types.NewsResults import NewsResults

def format_news_for_email(news_results: NewsResults, current_date: str) -> str:

    email_body = f"<h2>Today's Summary!!! {current_date}</h2>\n"
    email_body += "<p>Here are the latest updates:</p>\n"

    for idx, news in enumerate(news_results.results, start=1):

        email_body += f"<h3>{idx}. {news.headline}</h3>\n"
        email_body += f"<p>{news.description}</p>\n"
        email_body += "<p><strong>Sources:</strong> "

        source_links = []
        for source in news.source:
            source_links.append(f"<a href='{source.url}'>{source.name}</a>")

        email_body += ", ".join(source_links) + "</p>\n"
        email_body += "<hr>\n"