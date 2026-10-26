import argparse
import asyncio
import logging
import os
import datetime
import feedparser
from telethon import TelegramClient
from telethon.sessions import StringSession
from google import genai
from dataStorage2megaNZ import MegaNZClient

# --- Logging Setup ---

def _setup_logger() -> logging.Logger:
    """Configures a logger that appends to a daily log file and stdout."""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Filename prefix includes today's date
    date_prefix = datetime.date.today().strftime("%Y-%m-%d")
    log_path = os.path.join(log_dir, f"{date_prefix}_news_channel.log")

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )

    # Standard FileHandler in 'a' (append) mode. 
    # It automatically creates the file or appends if it already exists for that date.
    file_handler = logging.FileHandler(
        log_path,
        mode="a",
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    logger = logging.getLogger("news_channel")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    # Prevent root-logger duplication
    logger.propagate = False
    return logger

logger = _setup_logger()

# --- Configuration ---
NYT_SOURCES = {
    "NYT Economy": "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
    "NYT Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "NYT YourMoney": "https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
    "NYT Tech": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "NYT Science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
}
FT_SOURCES = {
    "myFT": "https://www.ft.com/myft/following/8d600a4d-f007-42fa-be49-445e335d1ec7.rss"
}

def _get_required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


API_ID = int(_get_required_env("TELEGRAM_API_ID"))
API_HASH = _get_required_env("TELEGRAM_API_HASH")
SESSION_STRING = _get_required_env("TELEGRAM_SESSION_STRING")
CHANNEL_ID = int(_get_required_env("TELEGRAM_CHANNEL_ID"))
GEMINI_API_KEY = _get_required_env("GEMINI_API_KEY")

GEMINI_SUMMARY_PROMPT = (
    "You are a market analyst who does research on market trends, "
    "today's key news articles are as follow, summarize in bullet point in a concise way, "
    "remove duplicated news, eg if you have multiple US vs Iran news, merge them into one line, "
    "for macro economic news, provide some short term trend analysis "
    "for individual company news also provide the company ticker or note it as private company "
    "at the end of the bullet point"
)

# --- Logic ---

def fetch_rss_entries(source_name, url, filter_keywords=None):
    """Parses an RSS feed and returns a list of matching entries."""
    logger.info(f"Fetching from {source_name}...")
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        logger.error(f"Error parsing {url}: {e}")
        return []

    results = []
    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", "N/A")
        summary = entry.get("summary", "")
        
        # Apply filtering if keywords are provided
        if filter_keywords:
            content_to_search = (title + " " + summary).lower()
            if not any(kw.lower() in content_to_search for kw in filter_keywords):
                continue
        
        results.append({
            "source": source_name,
            "title": title,
            "link": link,
            "published": published
        })
    
    logger.info(f"Found {len(results)} items in {source_name}.")
    return results


def summarize_with_gemini(items):
    """Uses Gemini (gemma-4-31b-it) to summarize all news items into key bullet points."""
    if not items:
        return None

    # Build a text block of all headlines for the model
    news_block = "\n".join(
        f"- [{item['source']}] {item['title']}" for item in items
    )
    full_prompt = f"{GEMINI_SUMMARY_PROMPT}\n\n{news_block}"

    logger.info("Generating Gemini summary...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=full_prompt,
        )
        summary_text = response.text
        logger.info("Summary generated successfully.")
        return summary_text
    except Exception as e:
        logger.error(f"Error generating Gemini summary: {e}")
        return None

async def send_to_telegram(items, summary_only=False, no_ai=False):
    """Initializes Telegram client, checks for duplicates, and sends new items."""
    if not items:
        logger.warning("No items to send.")
        return

    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        logger.info("Scanning channel history for duplicates...")
        history = await client.get_messages(CHANNEL_ID, limit=150)
        
        # Build a set of normalized links already in the channel
        existing_links = set()
        for msg in history:
            # Check entities for hidden links (like [Read Article](url))
            if msg.entities:
                for entity in msg.entities:
                    url = getattr(entity, 'url', None)
                    if url:
                        # Normalize: remove query params and trailing slash
                        existing_links.add(url.split('?')[0].rstrip('/'))
            
            # Also check if raw URL was pasted in message text
            if msg.message:
                for word in msg.message.split():
                    if word.startswith('http'):
                        existing_links.add(word.split('?')[0].rstrip('/'))
        
        logger.info(f"Found {len(existing_links)} unique links in recent history.")
        
        # Reverse the list so the oldest news is sent first
        items.reverse()
        
        # Filter for only new items
        new_items = []
        for item in items:
            clean_link = item['link'].split('?')[0].rstrip('/')
            if clean_link not in existing_links:
                new_items.append(item)
                existing_links.add(clean_link)
            else:
                logger.debug(f"Skipping (Already posted or duplicated): {item['title'][:50]}...")

        if not new_items:
            logger.info("No new items to send or summarize.")
            return

        if summary_only:
            logger.info("Summary-only mode enabled. Skipping individual news items.")
        else:
            sent_count = 0
            for item in new_items:
                message = (
                    f"📰 **{item['source']}**\n\n"
                    f"**{item['title']}**\n"
                    f"🕒 {item['published']}\n\n"
                    f"🔗 [Read Article]({item['link']})"
                )
                
                try:
                    await client.send_message(CHANNEL_ID, message, link_preview=False)
                    logger.info(f"Sent: {item['title'][:50]}...")
                    sent_count += 1
                    await asyncio.sleep(1.5)
                except Exception as e:
                    logger.error(f"Error sending to Telegram: {e}")
            
            logger.info(f"Broadcast complete. Shared {sent_count} new updates.")

        # Send to Telegram channel
        summary = summarize_with_gemini(new_items) if not no_ai else None
        if not no_ai and summary:
            summary_message = (
                "🤖 **AI Market Summary (Gemma 4)**\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{summary}"
            )
            try:
                await client.send_message(CHANNEL_ID, summary_message, link_preview=False)
                logger.info("Summary posted to channel.")
            except Exception as e:
                logger.error(f"Error sending summary to Telegram: {e}")
        
        # --- Save to Markdown and Upload to Mega.nz ---
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            md_filename = f"{timestamp}_news_summary.md"
            md_filepath = os.path.join(os.path.dirname(__file__), md_filename)
            
            with open(md_filepath, "w", encoding="utf-8") as f:
                f.write(f"# News Summary - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                if not no_ai and summary:
                    f.write("## AI Summary\n\n")
                    f.write(summary + "\n\n")
                f.write("## Articles\n\n")
                # Need to use the items, they are already reversed in chronological order above
                # which is fine.
                for item in new_items:
                    f.write(f"* **[{item['source']}]** [{item['title']}]({item['link']}) ({item['published']})\n")
                    
            logger.info(f"Generated markdown file: {md_filepath}")
            
            # Load MEGA credentials from environment variables
            email = os.getenv("MEGA_YAHOO_USERNAME")
            pwd = os.getenv("MEGA_YAHOO_PASSWORD")
            
            if email and pwd:
                mega_client = MegaNZClient(email, pwd)
                logger.info("Logging into MEGA via MegaNZClient...")
                mega_client.login()
                logger.info(f"Uploading {md_filename} to MEGA 'news' folder...")
                mega_client.upload(md_filepath, "news")
                logger.info("MEGA upload successful.")
            else:
                logger.error("Could not find MEGA_YAHOO_USERNAME/MEGA_YAHOO_PASSWORD in environment.")
                
            # Clean up local file
            if os.path.exists(md_filepath):
                os.remove(md_filepath)
                logger.info(f"Cleaned up local file {md_filepath}.")
                
        except Exception as e:
            logger.error(f"Failed to upload markdown summary: {e}")
            raise


async def main():
    # Setup CLI arguments
    parser = argparse.ArgumentParser(description="Fetch news from myFT/NYT and broadcast to Telegram.")
    parser.add_argument(
        "--source", 
        choices=["ft", "nyt", "all"], 
        default="all", 
        help="Select feed source (default: all)"
    )
    parser.add_argument(
        "--filter", 
        help="Comma-separated keywords to filter titles/summaries (e.g., 'airline,boeing')"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        help="Limit number of items per source"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        default=False,
        help="Send AI summary only"
    )
    parser.add_argument(
        "--noAI", 
        action="store_true",
        default=False,
        help="Skip AI summary generation"
    )

    args = parser.parse_args()

    # Parse keywords
    keywords = [k.strip() for k in args.filter.split(",")] if args.filter else None
    
    all_results = []

    # Map sources to fetch
    sources_to_fetch = []
    if args.source in ["ft", "all"]:
        sources_to_fetch.extend(FT_SOURCES.items())
    if args.source in ["nyt", "all"]:
        sources_to_fetch.extend(NYT_SOURCES.items())

    # Fetch data
    for name, url in sources_to_fetch:
        entries = fetch_rss_entries(name, url, keywords)
        if args.limit:
            entries = entries[:args.limit]
        all_results.extend(entries)

    # Broadcast
    if all_results:
        await send_to_telegram(all_results, summary_only=args.summary, no_ai=args.noAI)
    else:
        logger.info("Done. No matching articles found.")

if __name__ == "__main__":
    asyncio.run(main())