from pyrogram import Client, filters

import uniland.db.submission_methods as sub_db
import uniland.db.user_methods as user_db
from uniland import usercache
from uniland.config import STORAGE_CHAT_ID
from uniland.db.submission_methods import get_submission
from uniland.plugins.start.start import start_stage
from uniland.utils.enums import DocType
from uniland.utils.filters import access_level, exact_match, user_step
from uniland.utils.steps import UserSteps
from uniland.utils.triggers import Triggers
from uniland.utils.uxhandler import UXTree

staged_editted_subs = {}


async def send_submission(client, message, submission):
    """
    Sends a submission to a client.

    Args:
        client (Client): The client to send the submission to.
        message (Message): The message object to reply to.
        submission (Submission): The submission to send.

    Returns:
        None
    """
    if submission:
        if submission.submission_type == "document":
            await message.reply_document(
                document=submission.file_id, caption=str(submission)
            )
        elif submission.submission_type == "profile":
            if submission.image_id == "":
                await message.reply_text(str(submission))
            else:
                await message.reply_document(
                    document=submission.image_id, caption=str(submission)
                )


async def check_sub(client, message):
    """
    Check if the user's ID is in the list of staged edited subs.

    Parameters:
    - client: The client object.
    - message: The message object.

    Returns:
    - True if the user's ID is in the list of staged edited subs, False otherwise.
    """
    global staged_editted_subs
    if message.from_user.id not in staged_editted_subs:
        await message.reply(text="خطای گم شدن اطلاعات، لطفا دوباره تلاش کنید.")
        await start_stage(client, message)
        return False
    return True


async def go_back(client, message):
    """
    Go back to the previous step.

    Args:
        client (TelegramClient): The Telegram client.
        message (Message): The message object.

    Returns:
        None
    """
    # Going back to previous step
    step = usercache.get_last_step(message.from_user.id)
    user_step = UXTree.nodes[step]
    await message.reply(
        text=user_step.parent.description, reply_markup=user_step.parent.keyboard
    )
    user_db.update_user_step(message.from_user.id, user_step.parent.step)


@Client.on_message(
    filters.text
    & exact_match(Triggers.EDIT_SUBMISSION.value)
    & user_step(UserSteps.ADMIN_PANEL.value)
    & access_level(min=3)
)
async def start_editing_subs(
    client,
    message,
):
    """
    Starts the process of editing submissions for the admin panel.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    #! edit this part
    user_step = UXTree.nodes[UserSteps.EDIT_SUBMISSION.value]
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(message.from_user.id, UserSteps.EDIT_SUBMISSION.value)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_SUBMISSION.value)
    & ~exact_match(Triggers.BACK.value)
)
async def get_submission_id(
    client,
    message,
):
    """
    Retrieves the submission ID from the user's message and performs necessary checks.
    If the submission ID is valid, it retrieves the submission and stores it in the global variable.
    Then, it sends the submission to the user and updates the user's next step based on the submission type.
    """
    submission = None
    sub_id = -1
    try:
        sub_id = int(message.text)
    except Exception as _:
        await message.reply(text="شماره فایل یا اطلاعات وارد شده نامعتبر است!")
        return

    try:
        submission = get_submission(sub_id)
    except Exception as _:
        await message.reply("محتوایی با شماره موردنظر یافت نشد!")
        return

    if submission is None:
        await message.reply("محتوایی با شماره موردنظر یافت نشد!")
        return

    global staged_editted_subs
    staged_editted_subs[message.from_user.id] = submission
    await send_submission(client, message, submission)

    if submission.submission_type == "document":
        next_step = UXTree.nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value]
        await message.reply(next_step.description, reply_markup=next_step.keyboard)

        user_db.update_user_step(message.from_user.id, next_step.step)
    # ! oncomment this part before applying the edit profile
    elif submission.submission_type == "profile":
        next_step = UXTree.nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value]
        await message.reply(next_step.description, reply_markup=next_step.keyboard)

        user_db.update_user_step(message.from_user.id, next_step.step)


@Client.on_message(filters.text & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION.value))
async def choose_document_field(
    client,
    message,
):
    """
    This function is triggered when a user selects a document field to edit during the document submission process.
    It handles the routing of the user to input file data fields based on their selection.
    If the user selects the "Done" button, it saves the edited document and sends it to the storage chat.
    If the user selects the "Cancel" button, it cancels the document submission process.
    """
    user_step = UXTree.nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value]
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    # Data Fields
    for child in user_step.children:
        if message.text.strip() == child.trigger:
            await message.reply(text=child.description, reply_markup=child.keyboard)
            user_db.update_user_step(message.from_user.id, child.step)
            return

    # Done Button
    if message.text.strip() == Triggers.DOCUMENT_SUBMISSION_DONE.value:
        # User has finished the submission process
        doc = staged_editted_subs.pop(message.from_user.id)
        result = user_db.edit_admin_submission(message.from_user.id, doc)
        sent_message = None
        if result:
            sent_message = await client.send_document(
                chat_id=STORAGE_CHAT_ID,
                document=doc.file_id,
                caption=doc.user_display()
                + "\n\n فایل ویرایش شده توسط "
                + message.from_user.first_name,
            )
        if sent_message:
            await message.reply(
                text="فایل شما با موفقیت ویرایش شد. \nبا سپاس از همراهی شما"
            )
        else:
            await message.reply(
                "متاسفانه مشکلی در ویرایش فایل شما به وجود آمده است. لطفا مجددا تلاش کنید."
            )
        await start_stage(client, message)

    # Cancel Button
    elif message.text.strip() == Triggers.DOCUMENT_SUBMISSION_CANCEL.value:
        # User has canceled the submission process
        await message.reply("عملیات ویرایش اطلاعات لغو شد.")
        if message.from_user.id in staged_editted_subs:
            staged_editted_subs.pop(message.from_user.id)
        await start_stage(client, message)

    else:
        await message.reply("لطفا یکی از گزینه های موجود را انتخاب کنید.")


@Client.on_message(filters.text & user_step(UserSteps.EDIT_PROFILE_SUBMISSION.value))
async def choose_profile_field(client, message):
    """
    This function is triggered when a user sends a text message and is in the process of editing their profile submission.
    It routes the user to input file data fields based on their selection.

    Parameters:
        client (TelegramClient): The Telegram client instance.
        message (Message): The message object containing the user's text message.
    """
    user_step = UXTree.nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value]
    global staged_editted_subs
    if not await check_sub(client, message):
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
        profile = staged_editted_subs.pop(message.from_user.id)
        result = user_db.edit_admin_submission(message.from_user.id, profile)
        if result:
            await message.reply(
                text="فایل شما با موفقیت ویرایش شد. \nبا سپاس از همراهی شما"
            )
        else:
            await message.reply(
                "متاسفانه مشکلی در ویرایش فایل شما به وجود آمده است. لطفا دوباره تلاش کنید."
            )
        await start_stage(client, message)

    # Cancel Button
    elif message.text.strip() == Triggers.PROFILE_SUBMISSION_CANCEL.value:
        # User has canceled the submission process
        await message.reply("عملیات ویرایش فایل لغو شد.")
        staged_editted_subs.pop(message.from_user.id)
        await start_stage(client, message)

    else:
        await message.reply("لطفا یکی از گزینه‌های موجود را انتخاب کنید.")


@Client.on_message(
    filters.text
    & (
        user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value)
        | user_step(UserSteps.EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION.value)
    )
    & ~exact_match(Triggers.BACK.value)
)
async def delete_submission(
    client,
    message,
):
    """
    Deletes a submission from the database if the user confirms.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Deleting the submission if the user confirms
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    if message.text.strip() == Triggers.EDIT_DOCUMENT_SUBMISSION_REMOVE.value:
        sub = staged_editted_subs.pop(message.from_user.id)
        result = sub_db.delete_submission(sub.id)
        if result:
            await message.reply(
                "محتوای مورد نظر شما با متن جستجوی: \n\n"
                + str(sub.search_text)
                + "\n\nاز پایگاه داده حذف شد."
            )
            await start_stage(client, message)
        else:
            await message.reply(
                "متاسفانه مشکلی در حذف محتوا به وجود آمده است. لطفا دوباره تلاش کنید."
            )
        return


@Client.on_message(
    filters.text
    & (
        user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_FACULTY.value)
        | user_step(UserSteps.EDIT_PROFILE_SUBMISSION_FACULTY.value)
    )
    & ~exact_match(Triggers.BACK.value)
)
async def submission_faculty(
    client,
    message,
):
    """
    Handles the submission of faculty information for editing a document or profile.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Editting the faculty of the document
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.faculty = message.text.strip()
    await message.reply("نام دانشکده با موفقیت تغییر یافت.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & (
        user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_UNIVERSITY.value)
        | user_step(UserSteps.EDIT_PROFILE_SUBMISSION_UNIVERSITY.value)
    )
    & ~exact_match(Triggers.BACK.value)
)
async def submission_university(
    client,
    message,
):
    """
    Edits the university of the document submission or profile submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.university = message.text.strip()
    await message.reply("دانشگاه فایل شما با موفقیت تغییر یافت.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & (
        user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE.value)
        | user_step(UserSteps.EDIT_PROFILE_SUBMISSION_OWNER_TITLE.value)
    )
    & ~exact_match(Triggers.BACK.value)
)
async def submission_owner_title(
    client,
    message,
):
    """
    Edits the owner title of the document.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.owner_title = message.text.strip()
    await message.reply("عنوان صاحب فایل شما با موفقیت تغییر یافت.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & (
        user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_DESCRIPTION.value)
        | user_step(UserSteps.EDIT_PROFILE_SUBMISSION_DESCRIPTION.value)
    )
    & ~exact_match(Triggers.BACK.value)
)
async def submission_description(
    client,
    message,
):
    """
    Edits the description of a document submission or profile submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.description = message.text.strip()
    await message.reply("توضیحات فایل شما با موفقیت تغییر یافت.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_COURSE.value)
    & ~exact_match(Triggers.BACK.value)
)
async def document_course(
    client,
    message,
):
    """
    Edits the course name of a document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Editting course name
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.course = message.text.strip()
    await message.reply(".درس فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=sub.file_id, caption=str(sub))
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_PROFESSOR.value)
    & ~exact_match(Triggers.BACK.value)
)
async def document_professor(
    client,
    message,
):
    """
    Edit the professor name for a document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.professor = message.text.strip()
    await message.reply("استاد فایل شما با موفقیت تغییر یافت.")
    await message.reply_document(document=sub.file_id, caption=str(sub))
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_WRITER.value)
    & ~exact_match(Triggers.BACK.value)
)
async def document_writer(
    client,
    message,
):
    """
    Edits the writer of a document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.writer = message.text.strip()
    await message.reply("نویسنده فایل شما با موفقیت تغییر یافت.")
    await message.reply_document(document=sub.file_id, caption=str(sub))
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR.value)
    & ~exact_match(Triggers.BACK.value)
)
async def document_year(
    client,
    message,
):
    """
    Edits the semester year of a document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Editting the semester if its number, show error otherwise
    if not await check_sub(client, message):
        return
    sem = 0
    try:
        sem = int(message.text.strip())
    except Exception as _:
        await message.reply("لطفا یک عدد وارد کنید.")
        return
    global staged_editted_subs
    sub = staged_editted_subs[message.from_user.id]
    sub.semester_year = sem
    await message.reply("سال تهیه فایل شما با موفقیت تغییر یافت.")
    await message.reply_document(document=sub.file_id, caption=str(sub))
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_FILE_TYPE.value)
    & ~exact_match(Triggers.BACK.value)
)
async def document_file_type(
    client,
    message,
):
    """
    This function handles the editing of the file type of a document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Editting the faculty of the document
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    for c in DocType:
        if c.value == message.text.strip():
            sub.file_type = c
            await message.reply("نوع فایل شما با موفقیت تغییر یافت.")
            await message.reply_document(document=sub.file_id, caption=str(sub))
            await go_back(client, message)
            return

    await message.reply("لطفا یکی از گزینه‌های زیر را انتخاب کنید.")


@Client.on_message(
    user_step(UserSteps.EDIT_PROFILE_SUBMISSION_TITLE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def profile_title(
    client,
    message,
):
    """
    Updates the profile title for a user's submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting new profile title
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.title = message.text.strip()
    await message.reply("عنوان اطلاعات با موفقیت تغییر کرد.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_PROFILE_SUBMISSION_PHONE.value)
    & ~exact_match(Triggers.BACK.value)
)
async def profile_phone(
    client,
    message,
):
    """
    Handles the user's input for updating the profile phone number.

    Args:
        client: The Telegram client.
        message: The message object.

    Returns:
        None
    """
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.phone_number = message.text.strip()
    await message.reply("شماره تماس با موفقیت تغییر کرد.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_PROFILE_SUBMISSION_EMAIL.value)
    & ~exact_match(Triggers.BACK.value)
)
async def profile_email(
    client,
    message,
):
    """
    Handles the user's input for changing the profile email.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting profile email
    global staged_editted_subs
    if not await check_sub(client, message):
        return
    sub = staged_editted_subs[message.from_user.id]
    sub.email = message.text.strip()
    await message.reply("ایمیل با موفقیت تغییر کرد.")
    await send_submission(client, message, sub)
    await go_back(client, message)


@Client.on_message(
    filters.text
    & user_step(UserSteps.EDIT_PROFILE_SUBMISSION_PHOTO.value)
    & ~exact_match(Triggers.BACK.value)
)
async def profile_photo_by_text(client, message):
    """
    Handles the profile photo submission by text.

    Args:
        client: The Telegram client.
        message: The message object.

    Returns:
        None
    """
    if not await check_sub(client, message):
        return
    global staged_editted_subs
    if message.text == Triggers.PROFILE_SUBMISSION_DELETE_PHOTO.value:
        # Deleting profile photo
        profile = staged_editted_subs[message.from_user.id]
        profile.image_id = ""
        await message.reply("عکس پروفایل با موفقیت حذف شد.")
        await send_submission(client, message, profile)
        await go_back(client, message)
        return

    # Inputting profile photo
    # Upload photo to telegram
    # Set profile photo to uploaded photo
    profile = staged_editted_subs[message.from_user.id]
    sent_message = await client.send_document(
        chat_id=STORAGE_CHAT_ID, document=message.text.strip()
    )
    if sent_message:
        profile.image_id = sent_message.document.file_id
        await message.reply("عکس پروفایل با موفقیت تغییر کرد.")
        await send_submission(client, message, profile)
        await go_back(client, message)
        return

    await message.reply("لینک عکس پروفایل نامعتبر است.")


@Client.on_message(
    filters.photo
    & user_step(UserSteps.EDIT_PROFILE_SUBMISSION_PHOTO.value)
    & ~exact_match(Triggers.BACK.value)
)
async def profile_photo(client, message):
    """
    Handles the profile photo update process.

    Args:
        client: The Telegram client.
        message: The message object.

    Returns:
        None
    """
    if not await check_sub(client, message):
        return
    # Downloading photo and uploading as document on telegram
    # To get file_id as document
    await message.reply("در حال تبدیل به فایل...")
    photo = await message.download(in_memory=True)
    sent_message = await client.send_document(chat_id=STORAGE_CHAT_ID, document=photo)
    if sent_message is None:
        await message.reply(
            "دریافت فایل تصویری ناموفق بود، ممکن است به دلیل حجم زیاد تصویر باشد\n .لطفا مجددا تلاش کنید."
        )
        return
    # image_id is file_id of document
    global staged_editted_subs
    profile = staged_editted_subs[message.from_user.id]
    profile.image_id = sent_message.document.file_id
    await message.reply("عکس پروفایل با موفقیت تغییر کرد.")
    await send_submission(client, message, profile)
    await go_back(client, message)


@Client.on_message(
    filters.document
    & user_step(UserSteps.EDIT_PROFILE_SUBMISSION_PHOTO.value)
    & ~exact_match(Triggers.BACK.value)
)
async def profile_photo_document(client, message):
    """
    Handles the profile photo document message.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    if not await check_sub(client, message):
        return
    if "image" in message.document.mime_type or usercache.has_permission(
        message.from_user.id, min_permission=3
    ):
        global staged_editted_subs
        profile = staged_editted_subs[message.from_user.id]
        profile.image_id = message.document.file_id
        await message.reply("عکس پروفایل با موفقیت تغییر کرد.")
        await send_submission(client, message, profile)
        await go_back(client, message)
    else:
        await message.reply("لطفا فایلی با فرمت تصویر ارسال کنید.")
