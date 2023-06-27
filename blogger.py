import os
import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import google.oauth2.service_account



# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Set up Telegram bot
telegram_token = '6041556424:AAEjRM7RsQ73GumD1vqcRL0nlxgk5B6gwbU'
bot = telegram.Bot(token=telegram_token)

# Set up Blogger API
blogger_credentials_file = 'blogger1.json'
SCOPES = ['https://www.googleapis.com/auth/blogger.readonly']
creds = Credentials.from_authorized_user_file(blogger_credentials_file, SCOPES)
blogger_service = build('blogger', 'v3', credentials=creds)

def get_all_posts():
    all_posts = []
    page_token = None

    while True:
        posts = blogger_service.posts().list(blogId='495358728331336316', pageToken=page_token).execute()
        all_posts.extend(posts['items'])
        
        # Check if there are more posts
        if 'nextPageToken' in posts:
            page_token = posts['nextPageToken']
        else:
            break

    return all_posts

def start(update, context):
    user_id = update.effective_chat.id
    posts = get_all_posts()

    # Reverse the order of posts
    posts.reverse()

    # Send welcome message
    #context.bot.send_message(chat_id=user_id, text='Welcome to the Blogger Bot!')
    context.bot.send_photo(chat_id=user_id, photo='https://imgur.com/a/J9YM29b', caption=f"""
                           🙃😎 Hi...! I'm Learn Python Bot... 🙃
    
👨🏻‍💻 Learn Python Using Our Blog...
                           
👨🏻‍💻 User Friendly Teaching Method...
                           
👨🏻‍💻 Get All the Available Lessons through Me...
                           
💬 Inform Author About Q & A s...
                           
☢️ Coded by @drkvidun""")

    
    # Send each post with image, name, and link
    for post in posts:
        post_name = post['title']
        post_url = post['url']

        # Get the post image
        image_url = get_post_image(post)

        if image_url:
            # Send image
            context.bot.send_photo(chat_id=user_id, photo=image_url)

        # Send post name
        context.bot.send_message(chat_id=user_id, text=post_name)

        # Create inline keyboard with button
        button = InlineKeyboardButton(text='Read More', url=post_url)
        keyboard = InlineKeyboardMarkup([[button]])

        # Send link
        context.bot.send_message(chat_id=user_id, text=post_url, reply_markup=keyboard)


def get_post_image(post):
    # Check if 'images' attribute exists and is not empty
    if 'images' in post and len(post['images']) > 0:
        # Retrieve the first image URL
        return post['images'][0]['url']
    else:
        return None








# Error handler
def error(update, context):
    logging.error(f'Update "{update}" caused error "{context.error}"')

def main():
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handler for /start command
    dispatcher.add_handler(CommandHandler('start', start))

    # Add error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
