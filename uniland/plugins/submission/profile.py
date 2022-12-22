# Implementing finctionality of users' profile submission

from pyrogram import Client, filters
from uniland.utils.triggers import Triggers
import uniland.db.user_methods as user_db
import uniland.db.profile_methods as profile_db
from uniland.db.tables import Profile
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match
from uniland.plugins.start.start import start_stage
from uniland.utils.enums import DocType
from uniland.config import STORAGE_CHAT_ID

staged_profs = {}


async def check_profile(client, message):
    global staged_profs
    if message.from_user.id not in staged_profs:
        await message.reply(text="خطای گم شدن اطلاعات، لطفا دوباره تلاش کنید.")
        await start_stage(client, message)
        return False
    return True


async def display_profile(client, message, profile):
    # Displaying the profile
    global staged_profs
    profile = staged_profs[message.from_user.id]
    if profile.image_id == None or profile.image_id == "":
        await message.reply(text=str(profile))
    else:
        await message.reply_document(document=profile.image_id, caption=str(profile))


@Client.on_message(
    filters.text
    & ~filters.me
    & exact_match(Triggers.PROFILE_SUBMISSION_INPUT_TITLE.value)
    & user_step(UserSteps.CHOOSE_SUBMISSION_TYPE.value)
)
async def get_title(client, message):
    # Getting profile title from user
    user_step = UXTree.nodes[UserSteps.PROFILE_SUBMISSION_INPUT_TITLE.value]
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(
        message.from_user.id, UserSteps.PROFILE_SUBMISSION_INPUT_TITLE.value
    )


@Client.on_message(
    filters.text
    & ~filters.me
    & ~exact_match(Triggers.BACK.value)
    & user_step(UserSteps.PROFILE_SUBMISSION_INPUT_TITLE.value)
)
async def start_getting_data(client, message):
    # User has sent the file, now it can change the file data
    profile = Profile(None, title=message.text)
    global staged_profs
    staged_profs[message.from_user.id] = profile
    user_step = UXTree.nodes[UserSteps.PROFILE_SUBMISSION.value]
    await display_profile(client, message, profile)
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(message.from_user.id, UserSteps.PROFILE_SUBMISSION.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION.value) & ~filters.me & filters.text
)
async def choose_doc_field(client, message):
    # Routing the user to input file data fields
    user_step = UXTree.nodes[UserSteps.PROFILE_SUBMISSION.value]
    global staged_profs
    if not await check_profile(client, message):
        return
    # Data Fields
    for child in user_step.children:
        if message.text.strip() == child.trigger:
            await message.reply(text=child.description, reply_markup=child.keyboard)
            user_db.update_user_step(message.from_user.id, child.step)
            return

    # Done Button
    if message.text.strip() == Triggers.PROFILE_SUBMISSION_DONE.value:
        # User has finished the submission process
        profile = staged_profs.pop(message.from_user.id)
        result = user_db.add_user_submission(message.from_user.id, profile)
        if result:
            await message.reply(
                text="فایل شما با موفقیت ثبت شد و پس از تایید در دسترس کاربران قرار خواهد گرفت \nبا تشکر از شما بابت ارسال محتوای خود."
            )
        else:
            await message.reply(
                "متاسفانه مشکلی در ثبت فایل شما به وجود آمده است. لطفا دوباره تلاش کنید."
            )
        await start_stage(client, message)

    # Cancel Button
    elif message.text.strip() == Triggers.PROFILE_SUBMISSION_CANCEL.value:
        # User has canceled the submission process
        await message.reply("عملیات ارسال فایل لغو شد.")
        staged_profs.pop(message.from_user.id)
        await start_stage(client, message)

    else:
        await message.reply("لطفا یکی از گزینه‌های موجود را انتخاب کنید.")


# ---------------------- Inputting data fields ----------------------


async def go_back(client, message, step):
    # Going back to previous step
    user_step = UXTree.nodes[step]
    await message.reply(
        text=user_step.parent.description, reply_markup=user_step.parent.keyboard
    )
    user_db.update_user_step(message.from_user.id, user_step.parent.step)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_EDIT_TITLE.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def update_profile_title(
    client,
    message,
):
    # Inputting new profile title
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.title = message.text.strip()
    await message.reply("عنوان اطلاعات با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_EDIT_TITLE.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_PHONE.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_phone(
    client,
    message,
):
    # Inputting profile phone number
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.phone_number = message.text.strip()
    await message.reply("شماره تماس با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_PHONE.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_EMAIL.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_email(
    client,
    message,
):
    # Inputting profile email
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.email = message.text.strip()
    await message.reply("ایمیل با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_EMAIL.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_university(
    client,
    message,
):
    # Inputting university name
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.university = message.text.strip()
    await message.reply("نام دانشگاه با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_FACULTY.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_faculty(
    client,
    message,
):
    # Inputting faculty name
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.faculty = message.text.strip()
    await message.reply("عنوان اطلاعات با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_FACULTY.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_owner_title(
    client,
    message,
):
    # Inputting owner title
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.owner_title = message.text.strip()
    await message.reply("نام ثبت‌کننده‌ی اطلاعات با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_description(
    client,
    message,
):
    # Inputting description
    global staged_profs
    if not await check_profile(client, message):
        return
    profile = staged_profs[message.from_user.id]
    profile.description = message.text.strip()
    await message.reply("توضیحات با موفقیت تغییر کرد.")
    await display_profile(client, message, profile)
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_PHOTO.value)
    & ~filters.me
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def delete_profile_photo(client, message):
    if not await check_profile(client, message):
        return
    global staged_profs
    if message.text == Triggers.PROFILE_SUBMISSION_DELETE_PHOTO.value:
        # Deleting profile photo
        profile = staged_profs[message.from_user.id]
        profile.image_id = ""
        await message.reply("عکس پروفایل با موفقیت حذف شد.")
        await display_profile(client, message, profile)
        await go_back(client, message, UserSteps.PROFILE_SUBMISSION_PHOTO.value)
        return

    # return # TODO! delete this line when implemented

    # TODO! delete this line when implemented
    # await message.reply('لطفا تصویر جدید را ارسال کنید یا یکی از دکمه‌های زیر را بزنید.')1

    # TODO! Complete this part
    # Inputting profile photo
    # Check if message is link using regex
    # Download photo if input is a link
    # Upload photo to telegram
    # Set profile photo to uploaded photo
    profile = staged_profs[message.from_user.id]
    sent_message = await client.send_document(
        chat_id=STORAGE_CHAT_ID, document=message.text.strip()
    )
    if sent_message:
        profile.image_id = sent_message.document.file_id
        await message.reply("عکس پروفایل با موفقیت تغییر کرد.")
        await display_profile(client, message, profile)
        await go_back(client, message, UserSteps.PROFILE_SUBMISSION_PHOTO.value)

    await message.reply("لینک عکس پروفایل نامعتبر است.")


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_PHOTO.value)
    & ~filters.me
    & filters.photo
    & ~exact_match(Triggers.BACK.value)
)
async def profile_photo(client, message):
    if not await check_profile(client, message):
        return
    # Downloading photo and uploading as document on telegram
    # To get file_id as document
    await message.reply("در حال تبدیل به فایل...")
    photo = await message.download(in_memory=True)
    sent_message = await client.send_document(chat_id=STORAGE_CHAT_ID, document=photo)
    if sent_message == None:
        await message.reply(
            "دریافت فایل تصویری ناموفق بود، ممکن است به دلیل حجم زیاد تصویر باشد\n .لطفا مجددا تلاش کنید."
        )
        return
    # image_id is file_id of document
    image_id = sent_message.document.file_id
    global staged_profs
    staged_profs[message.from_user.id].image_id = image_id
    await message.reply("عکس پروفایل با موفقیت تغییر کرد.")
    await display_profile(client, message, staged_profs[message.from_user.id])
    await go_back(client, message, UserSteps.PROFILE_SUBMISSION_PHOTO.value)


@Client.on_message(
    user_step(UserSteps.PROFILE_SUBMISSION_PHOTO.value)
    & ~filters.me
    & filters.document
    & ~exact_match(Triggers.BACK.value)
)
async def profile_photo_document(client, message):
    if not await check_profile(client, message):
        return
    if "image" in message.document.mime_type:
        image_id = message.document.file_id
        global staged_profs
        staged_profs[message.from_user.id].image_id = image_id
        await message.reply("عکس پروفایل با موفقیت تغییر کرد.")
        await display_profile(client, message, staged_profs[message.from_user.id])
        await go_back(client, message, UserSteps.PROFILE_SUBMISSION_PHOTO.value)
    else:
        await message.reply("لطفا فایلی با فرمت تصویر ارسال کنید.")
