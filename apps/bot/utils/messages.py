"""Message templates for bot in multiple languages."""
from typing import Dict


class Messages:
    """Message templates in multiple languages."""

    MESSAGES: Dict[str, Dict[str, str]] = {
        "fa": {
            "welcome": "سلام {name} عزیز! 👋\n\nبه ربات یونیلند خوش آمدید.\n\nاز منوی زیر گزینه مورد نظر خود را انتخاب کنید:",
            "help": "راهنمای ثبت و دریافت فایل، جستجو و استفاده از ربات یونیلند\n\n🔹 ایدی ربات: @UniLandbot\n\n🔹 کانال اطلاع رسانی: @UniLand_AUT\n\n🔹 پشتیبانی: @UniLandSupport",
            "help_search": "نکات مرتبط به بخش جستجو:\n\n🔹 ربات UniLand به شما عزیزان قابلیت دو مدل سرچ را می‌دهد.\n     - سرچ داخل ربات\n     - سرچ اینلاین (داخل چت های pv و گروه و کانال...)\n🔹 در جستجوی خود سعی کنید از کاراکتر \"نیم فاصله\" استفاده نکنید.\n🔹 برای دستیابی هرچه دقیق تر به اطلاعات مورد نظرتان، نگارش صحیح و دقیق کلمه را رعایت کنید.\n🔹 برای فیلتر نتایج جستجو، از کلمات کلیدی زیر استفاده نمایید:\n  - \"اطلاعات\": این کلیدواژه، اطلاعات و راه های ارتباطی با اساتید را نمایش می‌دهد.\n  - \"جزوه\": این کلیدواژه، جزوات و خلاصه نویسی ها و... دروس را نمایش می‌دهد.\n  - \"کتاب\": این کلیدواژه، کتاب‌ها، منابع، سورس‌ها و... دروس را نمایش می‌دهد.\n  - \"تمرینات\": این کلیدواژه، تمرینات، نمونه‌سوالات، امتحان‌ها و... دروس را نمایش می‌دهد.\n  - \"تمپلیت\": این کلیدواژه، تمپلیت‌ها، گزارش دروس آز، پلان‌ها، شیت‌ها و... دروس را نمایش می‌دهد.",
            "help_submit": "نکات مرتبط به بخش ارسال محتوا:\n\n🔹 در درج اطلاعات مرتبط با فایل ارسالی خود و نگارش کلمات دقت کافی داشته باشید.\n🔹 پس از درج و تکمیل اطلاعات، دکمه \"اتمام\" را بزنید.\n🔹 در ثبت اطلاعاتی مانند دانشگاه و نام استاد، از کلمات \"دانشگاه\" و \"استاد\" استفاده نکنید.\n🔹 فایل های قابل ثبت در ربات در حال حاضر به دو بخش فایل و اطلاعات تقسیم بندی می‌شوند.",
            "help_scores": "نکات مربوط به امتیازگیری:\n\n🔹 امتیاز های شما تعداد لایک (👍) هاییست که کاربران ربات روی فایل های ثبت شده توسط شما اعمال می‌کنند، به علاوه 5 امتیاز برای هر فایل ثبت و تایید شده از طرف شما.\n🔹 پس میشه گفت با ثبت محتوای بیشتر می‌تونی شانس امتیازگیری خودتو بالا ببری.",
            "help_about": "ساخته شده توسط جمعی از دانشجویان علوم کامپیوتر دانشگاه صنعتی امیرکبیر (پلی‌تکنیک تهران)\n\nایلیا، پوریا، دلارام، علی، فاطمه، محمدرضا، مریم، مهسا",
            "help_soon": "منتظر فیچر های جدیدمون باشید 😉\n\n🔹 دسترسی اسان به فرم های آموزشی دانشگاه\n🔹 راهنما و اطلاعات به روز انتخاب واحد هر ترم\n🔹 راهنمای اپلای\n🔹 تعامل و درس خوانی با دانشجو های دیگر\n🔹 ریمایندر\n🔹 دریافت و تبادل روزانه غذای سلف\n🔹 و ...",
            "profile": "👤 پروفایل شما\n\n🎰 امتیاز: {score}\n📦 تعداد ثبت‌ها: {submissions}\n🖇️ تعداد پسندها: {bookmarks}\n🎚️ سطح دسترسی: {access_level}",
            "no_results": "نتیجه‌ای یافت نشد.",
            "submission_received": "محتوای شما با موفقیت ثبت شد و در صف بررسی قرار گرفت.",
            "submission_confirmed": "محتوای شما تایید شد! ✅",
            "submission_rejected": "متأسفانه محتوای شما رد شد.\n\nدلیل: {reason}",
            "bookmark_added": "به پسندها اضافه شد.",
            "bookmark_removed": "از پسندها حذف شد.",
            "error": "خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        },
        "en": {
            "welcome": "Hello {name}! 👋\n\nWelcome to UniLand bot.\n\nPlease select an option from the menu below:",
            "help": "UniLand Bot Help\n\n🔹 Bot ID: @UniLandbot\n\n🔹 Channel: @UniLand_AUT\n\n🔹 Support: @UniLandSupport",
            "help_search": "Search Guide:\n\n🔹 UniLand bot provides two search modes.\n     - In-bot search\n     - Inline search (in PV, groups, and channels...)\n🔹 Try to avoid using half-space characters in your search.\n🔹 For more accurate results, use correct spelling.\n🔹 Use these keywords to filter results:\n  - \"اطلاعات\": Shows contact information for professors\n  - \"جزوه\": Shows notes and summaries\n  - \"کتاب\": Shows books and resources\n  - \"تمرینات\": Shows exercises and exams\n  - \"تمپلیت\": Shows templates and reports",
            "help_submit": "Submission Guide:\n\n🔹 Be careful when entering file information.\n🔹 After completing the information, press the \"Done\" button.\n🔹 When entering university and professor names, don't include the words \"university\" or \"professor\".\n🔹 Files are divided into two categories: files and information.",
            "help_scores": "Scoring Guide:\n\n🔹 Your score is the number of likes (👍) that users give to your submitted files, plus 5 points for each confirmed file.\n🔹 So by submitting more content, you can increase your chances of getting more points.",
            "help_about": "Created by a group of Computer Science students at Amirkabir University of Technology (Tehran Polytechnic)\n\nIlya, Pouria, Delaram, Ali, Fatemeh, MohammadReza, Maryam, Mahsa",
            "help_soon": "Stay tuned for new features 😉\n\n🔹 Easy access to university forms\n🔹 Course selection guide\n🔹 Application guide\n🔹 Study groups\n🔹 Reminders\n🔹 Cafeteria food exchange\n🔹 And more...",
            "profile": "👤 Your Profile\n\n🎰 Score: {score}\n📦 Submissions: {submissions}\n🖇️ Bookmarks: {bookmarks}\n🎚️ Access Level: {access_level}",
            "no_results": "No results found.",
            "submission_received": "Your submission has been received and is pending review.",
            "submission_confirmed": "Your submission has been confirmed! ✅",
            "submission_rejected": "Unfortunately, your submission was rejected.\n\nReason: {reason}",
            "bookmark_added": "Added to bookmarks.",
            "bookmark_removed": "Removed from bookmarks.",
            "error": "An error occurred. Please try again.",
        },
    }

    @classmethod
    def get(cls, key: str, lang: str = "fa", **kwargs) -> str:
        """Get message by key and language."""
        message = cls.MESSAGES.get(lang, cls.MESSAGES["fa"]).get(key, "")
        return message.format(**kwargs) if kwargs else message

    @classmethod
    def get_welcome_message(cls, name: str, lang: str = "fa") -> str:
        """Get welcome message."""
        return cls.get("welcome", lang, name=name)

    @classmethod
    def get_help_message(cls, lang: str = "fa") -> str:
        """Get help message."""
        return cls.get("help", lang)

    @classmethod
    def get_profile_message(cls, score: int, submissions: int, bookmarks: int, access_level: str, lang: str = "fa") -> str:
        """Get profile message."""
        return cls.get(
            "profile",
            lang,
            score=score,
            submissions=submissions,
            bookmarks=bookmarks,
            access_level=access_level,
        )
