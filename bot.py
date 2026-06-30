import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN", "")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("Please add BOT_TOKEN in Railway Variables tab")
    exit(1)

print(f"✅ Token loaded successfully (length: {len(TOKEN)})")

# ===== Helper Functions =====
def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def count_characters(text: str) -> int:
    """Count total characters including spaces"""
    return len(text)

def count_characters_no_spaces(text: str) -> int:
    """Count characters excluding spaces"""
    return len(text.replace(" ", ""))

def count_sentences(text: str) -> int:
    """Count sentences using ., !, ? as delimiters"""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def count_paragraphs(text: str) -> int:
    """Count paragraphs by splitting on double newlines"""
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])

def count_lines(text: str) -> int:
    """Count non-empty lines"""
    lines = text.split('\n')
    return len([l for l in lines if l.strip()])

def count_numbers(text: str) -> int:
    """Count numbers in text"""
    return len(re.findall(r'\d+', text))

def count_letters(text: str) -> dict:
    """Count frequency of each letter (a-z)"""
    letter_count = {}
    for char in text.lower():
        if char.isalpha():
            letter_count[char] = letter_count.get(char, 0) + 1
    return dict(sorted(letter_count.items(), key=lambda x: x[1], reverse=True))

def count_punctuation(text: str) -> int:
    """Count punctuation marks"""
    punctuation = r'[.,!?;:()"\'-]'
    return len(re.findall(punctuation, text))

def estimate_reading_time(word_count: int) -> str:
    """Estimate reading time (200 words per minute avg)"""
    if word_count == 0:
        return "0 seconds"
    minutes = word_count / 200
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    else:
        return f"{minutes:.1f} minute{'s' if minutes != 1 else ''}"

def estimate_speaking_time(word_count: int) -> str:
    """Estimate speaking time (150 words per minute avg)"""
    if word_count == 0:
        return "0 seconds"
    minutes = word_count / 150
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    else:
        return f"{minutes:.1f} minute{'s' if minutes != 1 else ''}"

# ===== Command Handlers =====
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_msg = (
        f"✍️ *Hello {user.first_name}!*\n\n"
        "Welcome to *WordBridgexBot* - your word counting companion!\n\n"
        "I can analyze any text you send me and provide detailed statistics.\n\n"
        "*What I can do:*\n"
        "📝 Count words\n"
        "🔤 Count characters (with and without spaces)\n"
        "📄 Count sentences\n"
        "📑 Count paragraphs\n"
        "📏 Count lines\n"
        "🔢 Count numbers\n"
        "📊 Show letter frequency\n"
        "⏱️ Estimate reading and speaking time\n\n"
        "*How to use:*\n"
        "Simply send me any text, and I'll analyze it!\n"
        "Send /help to see all commands."
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_msg = (
        "📖 *WordBridgexBot Help*\n\n"
        "*Commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/stats - Show bot statistics\n"
        "/about - About this bot\n"
        "/analyze - Detailed analysis of text\n"
        "/compare - Compare two texts\n\n"
        "*Text Analysis:*\n"
        "Simply send any text message and I'll provide:\n"
        "• Word count\n"
        "• Character count (with and without spaces)\n"
        "• Sentence count\n"
        "• Paragraph count\n"
        "• Line count\n"
        "• Number count\n"
        "• Punctuation count\n"
        "• Letter frequency (most common letters)\n"
        "• Estimated reading time\n"
        "• Estimated speaking time\n\n"
        "*Example:*\n"
        "Send: `Hello world! This is a test.`"
    )
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_msg = (
        "✍️ *About WordBridgexBot*\n\n"
        "This bot was created to help writers, students, and professionals "
        "quickly analyze text for word and character counts.\n\n"
        "*Why WordBridgexBot?*\n"
        "✓ Simple and fast\n"
        "✓ No registration needed\n"
        "✓ Privacy-focused (we don't store your text)\n"
        "✓ Free to use\n"
        "✓ Detailed letter frequency analysis\n"
        "✓ Reading and speaking time estimates\n\n"
        "Built with ❤️ using open-source tools."
    )
    await update.message.reply_text(about_msg, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    stats_msg = (
        "📊 *Bot Statistics*\n\n"
        "This bot is powered by:\n"
        "• Python 3.11\n"
        "• python-telegram-bot library\n"
        "• Deployed on Railway\n\n"
        "⚡ *Features:*\n"
        "• Real-time text analysis\n"
        "• Accurate counting algorithms\n"
        "• Fast response time\n"
        "• Privacy-focused (we don't store your text)\n\n"
        "📈 *Metrics tracked:*\n"
        "• Words\n"
        "• Characters\n"
        "• Sentences\n"
        "• Paragraphs\n"
        "• Lines\n"
        "• Numbers\n"
        "• Punctuation\n"
        "• Letter frequency"
    )
    await update.message.reply_text(stats_msg, parse_mode='Markdown')

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /analyze command - detailed analysis"""
    parts = update.message.text.split(' ', 1)
    if len(parts) < 2:
        await update.message.reply_text(
            "⚠️ Please provide text to analyze.\n"
            "Example: `/analyze Hello world! This is a test.`",
            parse_mode='Markdown'
        )
        return
    
    text = parts[1].strip()
    await analyze_text(update, text)

async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /compare command - compare two texts"""
    parts = update.message.text.split('||', 1)
    if len(parts) < 2:
        await update.message.reply_text(
            "⚠️ Please provide two texts separated by `||`.\n"
            "Example: `/compare Text 1 || Text 2`",
            parse_mode='Markdown'
        )
        return
    
    try:
        text1 = parts[0].replace('/compare', '').strip()
        text2 = parts[1].strip()
        
        if not text1 or not text2:
            await update.message.reply_text("⚠️ Both texts must not be empty.")
            return
        
        # Analyze both texts
        result1 = get_analysis(text1)
        result2 = get_analysis(text2)
        
        response = (
            f"📊 *Text Comparison*\n\n"
            f"*Text 1:*\n"
            f"• Words: {result1['words']}\n"
            f"• Characters: {result1['chars']}\n"
            f"• Sentences: {result1['sentences']}\n"
            f"• Paragraphs: {result1['paragraphs']}\n\n"
            f"*Text 2:*\n"
            f"• Words: {result2['words']}\n"
            f"• Characters: {result2['chars']}\n"
            f"• Sentences: {result2['sentences']}\n"
            f"• Paragraphs: {result2['paragraphs']}\n\n"
            f"*Difference:*\n"
            f"• Words: {result2['words'] - result1['words']}\n"
            f"• Characters: {result2['chars'] - result1['chars']}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error comparing texts: {str(e)}")

def get_analysis(text: str) -> dict:
    """Get analysis results for a text"""
    return {
        'words': count_words(text),
        'chars': count_characters(text),
        'chars_no_space': count_characters_no_spaces(text),
        'sentences': count_sentences(text),
        'paragraphs': count_paragraphs(text),
        'lines': count_lines(text),
        'numbers': count_numbers(text),
        'punctuation': count_punctuation(text),
    }

async def analyze_text(update: Update, text: str):
    """Analyze text and send results"""
    if len(text.strip()) == 0:
        await update.message.reply_text("⚠️ Please send some text to analyze!")
        return
    
    # Perform calculations
    word_count = count_words(text)
    char_count = count_characters(text)
    char_no_space = count_characters_no_spaces(text)
    sentence_count = count_sentences(text)
    paragraph_count = count_paragraphs(text)
    line_count = count_lines(text)
    number_count = count_numbers(text)
    punctuation_count = count_punctuation(text)
    reading_time = estimate_reading_time(word_count)
    speaking_time = estimate_speaking_time(word_count)
    
    # Get letter frequency (top 10)
    letter_freq = count_letters(text)
    top_letters = ""
    if letter_freq:
        top_items = list(letter_freq.items())[:10]
        top_letters = "\n".join([f"• `{letter}`: {count}" for letter, count in top_items])
        if len(letter_freq) > 10:
            top_letters += f"\n• *...and {len(letter_freq) - 10} more letters*"
    else:
        top_letters = "No letters found"
    
    # Build response
    response = (
        f"📊 *Text Analysis Results*\n"
        f"{'─' * 30}\n"
        f"📝 *Words:* {word_count:,}\n"
        f"🔤 *Characters:* {char_count:,}\n"
        f"⬜ *Characters (no spaces):* {char_no_space:,}\n"
        f"📄 *Sentences:* {sentence_count:,}\n"
        f"📑 *Paragraphs:* {paragraph_count:,}\n"
        f"📏 *Lines:* {line_count:,}\n"
        f"🔢 *Numbers:* {number_count:,}\n"
        f"🔸 *Punctuation:* {punctuation_count:,}\n"
        f"{'─' * 30}\n"
        f"⏱️ *Reading time:* {reading_time}\n"
        f"🗣️ *Speaking time:* {speaking_time}\n"
        f"{'─' * 30}\n"
        f"📊 *Top 10 Letters:*\n{top_letters}\n"
        f"{'─' * 30}\n"
        f"📎 *Text preview:*\n"
        f"`{text[:150]}{'...' if len(text) > 150 else ''}`"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

# ===== Message Handler =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages - analyze text"""
    text = update.message.text
    
    if text.startswith('/'):
        return
    
    await analyze_text(update, text)

# ===== Error Handler =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    print(f"❌ Error: {context.error}")
    try:
        if update and update.message:
            await update.message.reply_text(
                "⚠️ An error occurred. Please try again later."
            )
    except:
        pass

# ===== Main Function =====
def main():
    """Start the bot"""
    print("🚀 Starting WordBridgexBot...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Application built successfully")
        
        # Command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(CommandHandler("analyze", analyze_command))
        application.add_handler(CommandHandler("compare", compare_command))
        
        # Message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot is running! Waiting for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
