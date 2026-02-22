import os
import json
# import asyncio
from dotenv import load_dotenv


load_dotenv()

model = os.getenv("model_to_be_used")

from litellm import acompletion


social_media_content_types = [
    # --- Original Topical Niches ---
    "Vlogging & Day in the Life",
    "Parenting & Family",
    "Home Decor & DIY",
    "Minimalism & Intentional Living",
    "Fitness & Training",
    "Mental Health & Wellness",
    "Nutrition & Diet",
    "Beauty & Skincare",
    "Coding & Software Development",
    "Career & Productivity",
    "Language Learning",
    "Science & History",
    "Personal Finance",
    "Entrepreneurship & Startups",
    "Tech Reviews & Gadgets",
    "Culinary Arts & Baking",
    "Travel & Exploration",
    "Outdoor & Survival",
    "Photography & Videography",
    "Art & Illustration",
    "Music & Audio Production",
    "Gaming & Esports",
    "Comedy & Skits",
    "Literature",
    "Media Commentary",
    "Fashion & Style",
    
    # --- Events, News & Promotions ---
    "Event Announcements & Save-the-Dates",
    "Product Drops & Launch Teasers",
    "Industry News & Real-Time Updates",
    "Company Milestones & Celebrations",
    "Live Streams & Webinars",
    
    # --- Education & Problem Solving ---
    "Brain Teasers, Puzzles & Logic Problems", 
    "Niche Problem Solving & Life Hacks",
    "Step-by-Step Tutorials & How-To Guides",
    "Infographics & Data Visualizations",
    "Myth Busting & Fact Checking",
    "Resource Roundups & Tool Recommendations",
    "Case Studies & Deep Dives",
    
    # --- Community & Interaction ---
    "Ask Me Anything (AMA) & Q&A Sessions",
    "Polls, Surveys & Quizzes",
    "Giveaways, Contests & Challenges",
    "User-Generated Content (UGC) Highlights",
    "Collaborations & Influencer Takeovers",
    "Customer Testimonials & Success Stories",
    
    # --- Entertainment & Engagement ---
    "Behind the Scenes (BTS) & Bloopers",
    "Memes, GIFs & Trend Jacking",
    "Unboxings & First Impressions",
    "Before & After Transformations",
    "Inspirational Quotes & Motivational Speaking",
    "Hot Takes & Unpopular Opinions"
]

async def call(data: dict):
    system_prompt = (
        "You are an expert Social Media Analyst. Your goal is to process video metadata "
        "and return high-quality, structured insights. You must respond ONLY with a "
        "valid JSON object."
    )

    user_prompt = f"""Analyze the following video metadata:
    ---
    DATA: 
    {json.dumps(data, indent=2)}
    ---

    Perform the following tasks:
    1. **Auto-Tag**: Categorize the content into exactly one of these labels: {social_media_content_types}.
    2. **Summarize**: Provide a high-impact, 1-sentence summary of the content.
    3. **Fact**: Provide a deep, engaging, and elaborate piece of trivia or a "neat fact" related to the content. Do not be brief; make it interesting and educational.

    OUTPUT FORMAT:
    Your response must be a JSON object with these exact keys:
    {{
    "autotag": "string",
    "summary": "string",
    "fact": "string"
    }}"""
    try:
        response = await acompletion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            response_format={"type": "json_object"},
        )
        tokens = response.usage.total_tokens
        processed_response = json.loads(response.choices[0].message.content)
        return {"model_used": model, "tokens": tokens, 'processed_response':processed_response}
    except Exception as e:
        print(f'Ai part failed due to {e}')

# resp = asyncio.run(
#     call(
#         {
#             "title": "Paper delivery gone wrong! | Manish Kharage #shorts",
#             "full_title": "Paper delivery gone wrong! | Manish Kharage #shorts",
#             "description": "",
#             "direct_url": "https://www.youtube.com/shorts/veSRXLDgcSs",
#             "link": "https://www.youtube.com/shorts/veSRXLDgcSs",
#             "thumbnail": "https://i.ytimg.com/vi/veSRXLDgcSs/maxresdefault.jpg",
#             "hashes": [],
#         }
#     )
# )
# print(resp)