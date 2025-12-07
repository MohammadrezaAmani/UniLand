"""Document submission handler - Complete implementation."""
import logging

from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

from apps.bot.di import get_injector
from apps.bot.services.submission_service import SubmissionService
from apps.bot.services.user_service import UserService
from apps.submissions.models import Document

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)
submission_service = injector.get(SubmissionService)

# Store staged documents
staged_documents = {}


@Client.on_message(filters.regex(r"^ارسال فایل$") & filters.private)
async def start_document_submission(client: Client, message: Message):
    """Start document submission flow."""
    await user_service.update_user_step(message.from_user.id, "document_submission_file_stage")
    
    keyboard = [["🔙 برگشت"]]
    text = "لطفا فایل مورد نظر خود را ارسال کنید:\n(می‌توانید فایل را فوروارد کنید، نگران کپشن آن هم نباشید😁)"
    
    await message.reply(text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


@Client.on_message(filters.document & filters.private)
async def receive_document(client: Client, message: Message):
    """Receive document file."""
    step = await user_service.get_user_step(message.from_user.id)
    
    if step != "document_submission_file_stage":
        return
    
    # Check if document already exists
    from asgiref.sync import sync_to_async
    
    @sync_to_async
    def check_exists():
        return Document.objects.filter(unique_id=message.document.file_unique_id).exists()
    
    if await check_exists():
        await message.reply("این فایل در پایگاه داده موجود است.\nلطفا فایل دیگری را ارسال نمایید.")
        return
    
    # Create staged document
    doc_data = {
        "file_id": message.document.file_id,
        "unique_id": message.document.file_unique_id,
        "file_type": "pamphlet",
        "course": "نامشخص",
        "professor": "نامشخص",
        "writer": "نامشخص",
        "semester_year": 0,
        "university": "نامشخص",
        "faculty": "نامشخص",
        "owner_title": message.from_user.first_name or "ناشناس",
        "description": "توضیحاتی برای این فایل ثبت نشده است.",
    }
    
    staged_documents[message.from_user.id] = doc_data
    
    await user_service.update_user_step(message.from_user.id, "document_submission_process")
    
    # Show document info
    info = f"نوع فایل: {doc_data['file_type']}\n"
    info += f"درس: {doc_data['course']}\n"
    info += f"استاد: {doc_data['professor']}\n"
    info += f"دانشکده: {doc_data['faculty']}\n"
    info += f"دانشگاه: {doc_data['university']}\n"
    info += f"نویسنده: {doc_data['writer']}\n"
    info += f"نام ثبت کننده: {doc_data['owner_title']}\n"
    info += f"سال: {doc_data['semester_year']}\n"
    info += f"توضیحات: {doc_data['description']}\n"
    
    await message.reply_document(document=message.document.file_id, caption=info)
    
    keyboard = [
        ["نوع فایل", "نام درس", "استاد درس"],
        ["دانشکده", "دانشگاه", "نویسنده"],
        ["نام ثبت کننده", "سال تهیه", "توضیحات"],
        ["✅ اتمام ✅", "❌ لغو ❌"],
    ]
    
    await message.reply(
        "مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )


@Client.on_message(filters.text & filters.private)
async def handle_document_fields(client: Client, message: Message):
    """Handle document field inputs."""
    step = await user_service.get_user_step(message.from_user.id)
    
    if step == "document_submission_process":
        if message.from_user.id not in staged_documents:
            await message.reply("خطای گم شدن فایل، لطفا مجددا تلاش کنید.")
            return
        
        text = message.text.strip()
        
        if text == "نوع فایل":
            await user_service.update_user_step(message.from_user.id, "document_submission_type_stage")
            keyboard = [
                ["کتاب", "جزوه"],
                ["تمرینات", "تمپلیت"],
                ["ترکیبی"],
                ["🔙 برگشت"],
            ]
            await message.reply("لطفا نوع فایل مورد نظر خود را انتخاب کنید.", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        
        elif text == "نام درس":
            await user_service.update_user_step(message.from_user.id, "document_submission_course_stage")
            await message.reply("لطفا نام درس مربوطه را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "استاد درس":
            await user_service.update_user_step(message.from_user.id, "document_submission_professor_stage")
            await message.reply("لطفا نام استاد درس را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "دانشکده":
            await user_service.update_user_step(message.from_user.id, "document_submission_faculty")
            await message.reply("لطفا نام دانشکده مربوطه را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "دانشگاه":
            await user_service.update_user_step(message.from_user.id, "document_submission_university")
            await message.reply("لطفا نام دانشگاه مربوطه را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "نویسنده":
            await user_service.update_user_step(message.from_user.id, "document_submission_writer_stage")
            await message.reply("لطفا نام تهیه‌کننده یا نویسنده فایل را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "نام ثبت کننده":
            await user_service.update_user_step(message.from_user.id, "document_submission_owner_title")
            await message.reply("می‌خواهید نام ثبت کننده فایل چه باشد؟ می‌توانید نام کامل یا مستعار خود را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "سال تهیه":
            await user_service.update_user_step(message.from_user.id, "document_submission_semester_year_stage")
            await message.reply("لطفا سال تهیه فایل را وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "توضیحات":
            await user_service.update_user_step(message.from_user.id, "document_submission_description")
            await message.reply("لطفا توضیحات مورد نظرتان را در مورد فایل خود وارد کنید.", reply_markup=ReplyKeyboardMarkup([["🔙 برگشت"]], resize_keyboard=True))
        
        elif text == "✅ اتمام ✅":
            # Submit document
            doc_data = staged_documents.pop(message.from_user.id)
            user = await user_service.get_user(message.from_user.id)
            
            doc = await submission_service.create_document(user, **doc_data)
            
            if doc:
                await message.reply("فایل شما با موفقیت ثبت شد و پس از تایید در دسترس کاربران قرار خواهد گرفت.\nبا سپاس از همراهی شما")
            else:
                await message.reply("متاسفانه مشکلی در ثبت فایل شما به وجود آمده است. لطفا مجددا تلاش کنید.")
            
            await user_service.update_user_step(message.from_user.id, "start_stage")
            keyboard = await get_main_keyboard(user.access_level)
            from pyrogram.types import ReplyKeyboardMarkup
            await message.reply("بازگشت به منوی اصلی", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        
        elif text == "❌ لغو ❌":
            staged_documents.pop(message.from_user.id, None)
            await message.reply("عملیات ارسال فایل لغو شد.")
            await user_service.update_user_step(message.from_user.id, "start_stage")
            user = await user_service.get_user(message.from_user.id)
            keyboard = await get_main_keyboard(user.access_level)
            from pyrogram.types import ReplyKeyboardMarkup
            await message.reply("بازگشت به منوی اصلی", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        
        else:
            await message.reply("لطفا یکی از گزینه های موجود را انتخاب کنید.")
    
    # Handle field value inputs
    elif step in ["document_submission_type_stage", "document_submission_course_stage", "document_submission_professor_stage",
                  "document_submission_faculty", "document_submission_university", "document_submission_writer_stage",
                  "document_submission_owner_title", "document_submission_semester_year_stage", "document_submission_description"]:
        
        if message.from_user.id not in staged_documents:
            return
        
        doc_data = staged_documents[message.from_user.id]
        text = message.text.strip()
        
        if text == "🔙 برگشت":
            await user_service.update_user_step(message.from_user.id, "document_submission_process")
            keyboard = [
                ["نوع فایل", "نام درس", "استاد درس"],
                ["دانشکده", "دانشگاه", "نویسنده"],
                ["نام ثبت کننده", "سال تهیه", "توضیحات"],
                ["✅ اتمام ✅", "❌ لغو ❌"],
            ]
            await message.reply("مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            return
        
        # Update field
        if step == "document_submission_type_stage":
            type_map = {"کتاب": "book", "جزوه": "pamphlet", "تمرینات": "exercises", "تمپلیت": "template", "ترکیبی": "compressed"}
            doc_data["file_type"] = type_map.get(text, "pamphlet")
            await message.reply("نوع فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_course_stage":
            doc_data["course"] = text
            await message.reply("درس فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_professor_stage":
            doc_data["professor"] = text
            await message.reply("استاد فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_faculty":
            doc_data["faculty"] = text
            await message.reply("دانشکده فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_university":
            doc_data["university"] = text
            await message.reply("دانشگاه فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_writer_stage":
            doc_data["writer"] = text
            await message.reply("نویسنده فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_owner_title":
            doc_data["owner_title"] = text
            await message.reply("عنوان صاحب فایل شما با موفقیت ثبت شد.")
        elif step == "document_submission_semester_year_stage":
            try:
                doc_data["semester_year"] = int(text)
                await message.reply("سال تهیه فایل شما با موفقیت ثبت شد.")
            except ValueError:
                await message.reply("لطفا یک عدد وارد کنید.")
                return
        elif step == "document_submission_description":
            doc_data["description"] = text
            await message.reply("توضیحات فایل شما با موفقیت ثبت شد.")
        
        # Show updated document
        info = f"نوع فایل: {doc_data['file_type']}\n"
        info += f"درس: {doc_data['course']}\n"
        info += f"استاد: {doc_data['professor']}\n"
        info += f"دانشکده: {doc_data['faculty']}\n"
        info += f"دانشگاه: {doc_data['university']}\n"
        info += f"نویسنده: {doc_data['writer']}\n"
        info += f"نام ثبت کننده: {doc_data['owner_title']}\n"
        info += f"سال: {doc_data['semester_year']}\n"
        info += f"توضیحات: {doc_data['description']}\n"
        
        await message.reply_document(document=doc_data["file_id"], caption=info)
        
        # Go back to main menu
        await user_service.update_user_step(message.from_user.id, "document_submission_process")
        keyboard = [
            ["نوع فایل", "نام درس", "استاد درس"],
            ["دانشکده", "دانشگاه", "نویسنده"],
            ["نام ثبت کننده", "سال تهیه", "توضیحات"],
            ["✅ اتمام ✅", "❌ لغو ❌"],
        ]
        await message.reply("مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def get_main_keyboard(access_level: int = 1):
    """Get main keyboard."""
    from apps.bot.utils.keyboards import get_main_keyboard as gmk
    return await gmk(access_level)
