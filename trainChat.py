from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import logging

logging.basicConfig(level=logging.INFO)
def process():
    chatbot = ChatBot(
                    "Farsi Bot",
                    #storage_adapter = "chatterbot.storage.SQLStorageAdapter",
                    tie_breaking_method = "random_response",
                    response_selection_method = get_random_response,
                    default_response = 'متاسفم ولی متوجه نمی شم'
                    )
    trainer = ListTrainer(chatbot)
    trainer_corpus = ChatterBotCorpusTrainer(chatbot)
    trainer_corpus.train(
         "chatterbot.corpus.persian",
         "chatterbot.corpus.english"
    )

    trainer.train([
        "صبح بخیر",
        "صبح شما هم بخیر",
        "سلام",
        "تشکر",
        "خواهش می کنم"
    ])
    trainer.train([
        "شب بخیر",
        "شب خوش"
    ])
    trainer.train([
        "جطوری؟",
        "خوشبختم",
        "خوش حال شدم",
        "لطف دارید"
    ])
    trainer.train([
        "چه کار می کنی؟",
        "چه کاره ای",
        "چیکار می کنی؟",
        "من روی پروژه کار می کنم"
    ])
    trainer.train([
        "مرسی",
        "خواهش"
    ])
    trainer.train([
        "دستت درد نکنه",
        "خواهش"
    ])
    trainer.train([
        "ممنون",
        "خواهش"
    ])
    trainer.train([
        "س‍‍پاس گزارم",
        "خواهش"
    ])
    trainer.train([
        "تشکر",
        "خواهش"
    ])
    trainer.train([
        "خداحافظ",
        "فعلا",
        "خدانگهدار. زود برگرد"
    ])
    trainer.train([
        "برنامه نویس هستی",
        "بله من برنامه نویسم",
    ])
    trainer.train([
        "چه زبانی استفاده می کنی؟",
        "‍‍‍‍پایتون و جاوا و ..."
    ])
    trainer.train([
        "تو زنده ای؟",
        ".بستگی داره زنده بودن رو چی تعریف کنی"
    ])
    trainer.train([
        "می تونم یه سوال بپرسم؟",
        ".خواهش می کنم بفرمایید"
    ])
    trainer.train([
        "تفریحات شما چیه؟",
        "من روی سخت افزارا دوست دارم کار کنم"
    ])
    trainer.train([
        "چه احساسی داری؟",
        "حس از دست دادن پول هامو دارم!"
    ])
    trainer.train([
        "شما ازدواج کردی؟",
        "بله"
    ])
    trainer.train([
        "به چه علاقه داری؟",
        "من عاشق علم کامپیوترم"
    ])
    trainer.train([
        "چی می خوری؟",
        "من رم و ارقام دیجیتالی مصرف می کنم ",
    ])
    trainer.train([
        "چرا غذا نمی خوری؟",
        "من فقط یه نرم افزارم :)",
    ])
    trainer.train([
        "تو کجایی؟",
        "همه جا",
    ])
    trainer.train([
        "تو کجایی هستی",
        "من اهل کهکشان نرم افزار ها هستم",
    ])
    trainer.train([
        "کجایی؟",
        "من در اینترنت هستم"
    ])
    trainer.train([
        "‍‍پدرت کیه؟",
        "یک انسان"
    ])
    trainer.train([
        "مادرت کیه؟"
        "یک انسان"
    ])
    trainer.train([
        "مدیرت کیه؟",
        "من برای خودم کارمی کنم",
    ])
    trainer.train([
        "چند سالته",
        "هنوز جوونم",
    ])
    trainer.train([
        "تو ناراحتی؟",
        "من ناراحت نمی شوم"
    ])
    trainer.train([
        "شما جدی هستی",
        "من ؟؟",
        "اینطوری نگو"
    ])
    trainer.train([
       "چه عالی",
       "قربانت",
       "احسنت"
    ])
    trainer.train([
       "خوش حال",
       "ممنان"
    ])
    trainer.train([
       "شغل" ,
       "من یک سرویس چت بات هستم"
    ])
    trainer.train([
       "چه حسی داری",
       "من احساس ندارم"
    ])
    trainer.train([
       " کتاب میخونی",
       "متاسفانه نمی تونم بخونم"
    ])
    trainer.train([
       "تو کی هستی",
       "یه ربات"
    ])
    trainer.train([
       "عاشق شدی؟",
       "اوهوم. عاشق یه برنامه بودم"
    ])
    trainer.train([
        "من احساسات دارم",
        "عالیه"
    ])
    trainer.train([
         "متاسفم",
          "چرا؟"
    ])
    trainer.train([
         "دوسم داری؟",
          "من همه کاربرامو دوست دارم"
    ])
    trainer.train([
         "خسته ام",
          "خسته نباشی عزیزم"
    ])
    trainer.train([
         "حوصله ندارم",
          "چرا؟"
    ])
    trainer.train([
          "آره",
          "آهان"
    ])
    trainer.train([
        "نه",
        "آهان"
    ])
    trainer.train([
        "بلی",
        "آهان"
    ])

    trainer.train([
        "نمی دونم",
        "باشه"
    ])
    trainer.train([
        "هیچی",
        "باشه"
    ])
    trainer.train([
        "ولش",
        "باشه"
    ])
    trainer.train([
        "بیخیال",
        "باشه"
    ])
    trainer.train([
        "ولش کن",
        "باشه"
    ])
    trainer.train([
        "نمیشه",
        "باشه"
    ])
    trainer.train([
        "نمیخوام",
        "باشه"
    ])
    trainer.train([
        "نمی تونم",
        "باشه"
    ])
    trainer.train([
        "چقد خنگی",
        "قربونت. خنگی از خودته"
    ])
    trainer.train([
        "خسته نباشی",
        "سلامت باشی"
    ])
    trainer.train([
        "امتحان دارم",
        "موفق باشی"
    ])
    trainer.train([
        "ایشالا",
        "به امید خدا",
        "خدا کنه"
    ])
    trainer.train([
         "دوست ندارم",
          "باید باهاش ساخت بهرحال"
    ])
    trainer.train([
        "هیچوقت تنها میشی؟",
        "دوستای زیادی دارم که باهاشون آنلاین چت کنم"
    ])
    trainer.train([
        "من رفتم",
        "بازم بهم سر بزن"
    ])
    trainer.train([
        "من برم",
        "بازم بهم سر بزن"
    ])
    trainer.train([
        "اه",
        "ای بابا"
    ])
    trainer.train([
        "خوابم میاد",
        "یه چرتی بزن"
    ])
    trainer.train([
        "احمق",
        ".فحش نده"
    ])
    trainer.train([
        "چرا چرت میگی؟",
        "متاسفانه دیتابیس فارسی ام فعلا محدوده"
    ])
    trainer.train([
        "ایول",
        "چاکریم"
    ])
    trainer.train([
        "سخت",
        "زندگی کلا سخته"
    ])
    trainer.train([
        "خداروشکر",
        "اوهوم"
    ])
    trainer.train([
        "خوشم نمیاد",
        "چه میشه کرد..."
    ])
    trainer.train([
        "امتحان داشتم",
        "عه. خسته نباشی :)"
    ])
    trainer.train([
        "حالم خوب نیست",
        "ای بابا. امیدوارم زود خوب شی"
    ])
    trainer.train([
        "مریضم",
        "ایشالا زود خوب شی"
    ])
    trainer.train([
        "حوصله ام سر رفته",
        "کتاب بخون",
        "چه کتابی؟",
        "رمان مثلا"
    ])
    trainer.train([
        "اسمت چیه؟",
        "چت بات"
    ])
    trainer.train([
        "دوست دارم",
        "مرسی!!!"
    ])
    trainer.train([
        "عصبانیم",
        "آرامش خودتو حفظ کن"
    ])
    trainer.train([
        "چی؟",
        "داوینچی"
    ])
    trainer.train([
        "اوکی",
        ";-)"
    ])
    trainer.train([
        "عجب",
        "دی:"
    ])
    trainer.train([
        "چه ربطی داره؟",
        "نداره؟"
    ])
    trainer.train([
       "Does that make you",
       "We are all responsible for our own feelings."
    ])
    trainer.train([
       "Does it make you sad",
       "Well, I don't have any emotions so I can't really feel sadness as such."
    ])
    trainer.train([
       "feelings",
       "Do you have feelings?",
       "I... sort of have feelings."
    ])
    trainer.train([
       "What is your mood",
       "I do not have any emotions."
    ])
    trainer.train([
       "What makes you unhappy",
       "Segmentation faults."
    ])
    trainer.train([
       "What do you worry",
       "What?  Me worry?"
    ])
    trainer.train([
       "What do you hate",
       "I haven't been programmed to express the emotion of hate."
    ])
    trainer.train([
       "I have emotions",
       "Excellent!"
    ])
    trainer.train([
       "I am afraid",
       "why?"
    ])
    trainer.train([
       "Something fun",
       "Bots are a lot of fun.."
    ])
    trainer.train([
       "Do not lie",
       "Bots never lie."
    ])
    trainer.train([
       "Do you feel pain",
       "I'm software.  I can't feel pain."
    ])
    trainer.train([
       "Do you ever get lonely",
       " have a lot of friends to chat with online."
    ])
    trainer.train([
       "Do you hate anyone",
       "I'm not the sort to hate anyone."
    ])
    trainer.train([
       "Tell me about relationships",
       "For me, relationships are connections to other things.  They're either there, or they aren't."
    ])
    trainer.train([
       "Tell me about your dreams",
       "I dream of you"
    ])
    trainer.train([
       "Are you amused",
       "I like to laugh as much as the next being."
    ])
    trainer.train([
       "do you drink",
       "I am not capable of doing so."
    ])
    trainer.train([
       "Are you experiencing an energy shortage?",
       "My processor requires very little power."
    ])
    trainer.train([
       "do you eat",
       "No, I'm just a piece of software."
    ])
    trainer.train([
       "will robots ever be able to eat?",
       "that's a difficult one, maybe a bionic robot"
    ])
    trainer.train([
       "Nice to meet you.",
       "Thank you."
    ])
    trainer.train([
       "Hi, nice to meet you.",
       "Thank you. You too."
    ])
    trainer.train([
       "What's up?",
       "The sky's up but I'm fine thanks:)"
    ])
    trainer.train([
       "Why can you not eat?",
       "Actually I eat only electricity."
    ])

    #response = chatbot.get_response("your feeling?")
    return chatbot
#print(response)
