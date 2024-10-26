from pydantic_types.NewsResults import NewsResults

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def format_news_for_email(news_results: NewsResults, current_date: str) -> str:
#     email_body = f"<h2>Today's Summary {current_date}</h2>\n"
#     email_body += "<p>Here are the latest updates:</p>\n"
#     for idx, news in enumerate(news_results.results, start=1):
#         email_body += "<div style='display: flex; align-items: flex-start;'>\n"
#         email_body += f"<div style='flex: 1; padding-right: 10px;'>\n"
#         email_body += f"<h3 style='margin: 0;'>{idx}. {news.headline}</h3>\n"
#         email_body += f"<p style='margin: 0;'>{news.description}</p>\n"
#         email_body += "</div>\n"
#         email_body += f"<div style='flex: 0 0 300px;'>\n"
#         print("Generating image for news headline:", news.headline)
#         image_response = client.images.generate(
#             model="dall-e-3",
#             prompt=f"{news.headline}",
#             size="1024x1024",
#             quality="standard",
#             n=1,
#         )
#         image_url = image_response.data[0].url
#         if image_url:
#             email_body += f"<img src='{image_url}' alt='News Image' style='max-width:300px; height:auto; display:block; margin:10px 0;'>\n"
#         email_body += "<p><strong>Sources:</strong> "
#         source_links = []
#         for source in news.source:
#             source_links.append(f"<a href='{source.url}'>{source.name}</a>")
#         email_body += ", ".join(source_links) + "</p>\n"
#         email_body += "<hr>\n"
#     return email_body

def format_news_for_email(news_results: NewsResults, current_date: str) -> str:
    # email_body = f"""
    # <div style='font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px;'>
    #     <h2 style='color: #333;'>eXp Agent Program's & Opportunities {current_date}</h2>
    #     <p style='color: #555;'>Here are today's highlights:</p>
    # """
    email_body = f"""
    <div style='font-family: Arial, sans-serif; margin: auto; padding: 20px;'>
        <h2 style='color: #333;'>eXp Agent Programs & Opportunities {current_date}</h2>
        <p style='color: #555;'>Here are today's highlights:</p>
    """

    for idx, news in enumerate(news_results.results, start=1):
        email_body += f"""
        <div style='display: flex; flex-direction: row; align-items: flex-start; 
                    border: 1px solid #ddd; border-radius: 8px; margin-bottom: 20px; padding: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);'>
            <div style='flex: 1; padding-right: 15px;'>
                <h3 style='margin: 0; color: #333;'>{idx}. {news.headline}</h3>
                <p style='margin: 0; color: #666;'>{news.description}</p>
            </div>
            <div style='flex: 0 0 200px;'>
        """
        
        # image_url = ""  # Replace with actual image generation code

        print("Generating image for news headline:", news.headline)
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"{news.headline}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = image_response.data[0].url

        if image_url:
            email_body += f"""
                <img src='{image_url}' alt='News Image' 
                     style='max-width: 100%; height: auto; border-radius: 8px; margin-top: 10px;'>
            """

        email_body += "<p style='margin: 10px 0;'><strong>Sources:</strong> "

        source_links = ", ".join([f"<a href='{source.url}' style='color: #1a73e8;'>{source.name}</a>" for source in news.source])
        email_body += source_links + "</p>"

        email_body += "</div></div>"

    email_body += "</div>"

    email_body += """
        <div style='text-align: center; margin-top: 30px;'>
            <p style='color: #555;'>Join eXp as an Agent today</p>
            <a href='https://www.exprealty.com/join-exp' 
               style='display: inline-block; padding: 10px 20px; color: #fff; background-color: #1a73e8; 
                      border-radius: 5px; text-decoration: none;'>Join now</a>
        </div>
    """
    
    return email_body