import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(level=logging.INFO)

# Bot data storage
users_data = {}
admin_id = 6565686047
channel_links = [
    "https://t.me/+Tx0ogyhkN9NjZjc1",
    "https://t.me/channel2",
    "https://t.me/channel3"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in users_data:
        users_data[user_id] = {'balance': 0, 'referrals': 0, 'daily_bonus': False}
    
    # Check if user has joined channels
    if not await check_channel_join(update, context, user_id):
        return

    keyboard = [
        [InlineKeyboardButton("💰 Check Balance", callback_data='balance')],
        [InlineKeyboardButton("🔗 Get Referral Link", callback_data='referral')],
        [InlineKeyboardButton("🎁 Claim Daily Bonus", callback_data='daily_bonus')],
        [InlineKeyboardButton("📘 How to Earn", callback_data='earnings')],
    ]

    if user_id == admin_id:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Panel", callback_data='admin')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def check_channel_join(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    for link in channel_links:
        await update.message.reply_text(f"Please join this channel: {link}")
    await update.message.reply_text("After joining all channels, click /start again.")
    return False

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'balance':
        balance = users_data[user_id]['balance']
        await query.message.reply_text(f"Your balance: ₹{balance}")
    elif query.data == 'referral':
        referral_link = f"https://t.me/YourBotUsername?start={user_id}"
        await query.message.reply_text(f"Your referral link: {referral_link}")
    elif query.data == 'daily_bonus':
        if not users_data[user_id]['daily_bonus']:
            users_data[user_id]['balance'] += 5
            users_data[user_id]['daily_bonus'] = True
            await query.message.reply_text("Daily bonus of ₹5 claimed!")
        else:
            await query.message.reply_text("You've already claimed your daily bonus today.")
    elif query.data == 'earnings':
        await query.message.reply_text("You earn ₹5 for each successful referral.")
    elif query.data == 'admin' and user_id == admin_id:
        await query.message.reply_text("Welcome to the admin panel. More functions coming soon!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

def main():
    application = Application.builder().token("7257817332:AAED9hZhniWkfK4OVrerzmVJERujyxBHQao").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error_handler)

    logging.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()