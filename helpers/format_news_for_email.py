from pydantic_types.NewsResults import NewsResults

from openai import OpenAI

client = OpenAI()

def format_news_for_email(news_results: NewsResults, current_date: str) -> str:
    email_body = f"<h2>Today's Summary!!! {current_date}</h2>\n"
    email_body += "<p>Here are the latest updates:</p>\n"
    
    for idx, news in enumerate(news_results.results, start=1):
        email_body += f"<h3>{idx}. {news.headline}</h3>\n"
        email_body += f"<p>{news.description}</p>\n"
    
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"{news.headline}",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = image_response.data[0].url
        
        if image_url:
            email_body += f"<img src='{image_url}' alt='News Image' style='max-width:600px; height:auto; display:block; margin:10px 0;'>\n"
        
        email_body += "<p><strong>Sources:</strong> "
        
        source_links = []
        for source in news.source:
            source_links.append(f"<a href='{source.url}'>{source.name}</a>")
        
        email_body += ", ".join(source_links) + "</p>\n"
        email_body += "<hr>\n"
    
    return email_body