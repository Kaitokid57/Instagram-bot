import telebot
import instaloader
from io import BytesIO
import requests

# توكن البوت
API_TOKEN = '7927251943:AAHS4ZcNpc51FLBT34kPY06GeRh-MOcgBuk'
bot = telebot.TeleBot(API_TOKEN)

# رسالة البداية
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, (
        "🤖 أهلاً بك في بوت تحميل الوسائط من Instagram!\n\n"
        "🔹 أرسل رابط الصورة أو الفيديو من Instagram، وسنقوم بتحميله لك.\n\n"
        "💡 تأكد من أن الرابط عام (غير محمي)."
    ))

# تحميل من Instagram
def download_instagram(url, chat_id):
    try:
        bot.send_message(chat_id, "🔄 جاري التحميل من Instagram...")
        loader = instaloader.Instaloader()
        shortcode = url.split("/")[-2]  # استخراج كود المنشور
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        if post.is_video:
            # تحميل الفيديو
            video_url = post.video_url
            response = requests.get(video_url)
            video_file = BytesIO(response.content)
            video_file.name = "instagram_video.mp4"
            bot.send_video(chat_id, video_file, caption="✅ تم تحميل الفيديو بنجاح!")
        else:
            # تحميل الصورة
            image_url = post.url
            response = requests.get(image_url)
            image_file = BytesIO(response.content)
            image_file.name = "instagram_image.jpg"
            bot.send_photo(chat_id, image_file, caption="✅ تم تحميل الصورة بنجاح!")
    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ أثناء تحميل الوسائط:\n{e}")

# رد على الرسائل بالرابط
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    chat_id = message.chat.id

    if "instagram.com" in url:
        download_instagram(url, chat_id)
    else:
        bot.send_message(chat_id, "❌ يرجى إرسال رابط صحيح من Instagram.")
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# استدعاء keep_alive لتشغيل الخادم
keep_alive()

# تشغيل البوت
bot.polling()