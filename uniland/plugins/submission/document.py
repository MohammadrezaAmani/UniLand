# Implementing finctionality of users' document submission

from pyrogram import Client, filters

import uniland.db.doc_methods as doc_db
import uniland.db.user_methods as user_db
from uniland.config import STORAGE_CHAT_ID
from uniland.db.tables import Document
from uniland.plugins.start.start import start_stage
from uniland.utils.enums import DocType
from uniland.utils.filters import exact_match, user_step
from uniland.utils.steps import UserSteps
from uniland.utils.triggers import Triggers
from uniland.utils.uxhandler import UXTree

staged_docs = {}


@Client.on_message(
    filters.text
    & exact_match(Triggers.DOCUMENT_SUBMISSION_FILE.value)
    & user_step(UserSteps.CHOOSE_SUBMISSION_TYPE.value)
)
async def get_file(client, message):
    """
    This function is triggered when a user sends a text message that matches the DOCUMENT_SUBMISSION_FILE trigger,
    and the user is in the CHOOSE_SUBMISSION_TYPE step. It handles the process of getting a file from the user.

    Args:
        client: The Telegram client.
        message: The message object.

    Returns:
        None
    """
    # Getting file from user
    user_step = UXTree.nodes[UserSteps.DOCUMENT_SUBMISSION_FILE.value]
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(
        message.from_user.id, UserSteps.DOCUMENT_SUBMISSION_FILE.value
    )


@Client.on_message(
    filters.document & user_step(UserSteps.DOCUMENT_SUBMISSION_FILE.value)
)
async def start_getting_data(
    client,
    message,
):
    """
    This function is triggered when a document is received from the user for submission.
    It checks if the document already exists in the database and handles the submission process.

    Args:
        client: The Telegram client.
        message: The message containing the document.

    Returns:
        None
    """
    # User has sent the file, now it can change the file data
    if doc_db.unique_id_exists(message.document.file_unique_id):
        await message.reply(
            text="این در پایگاه داده موجود است.\n لطفا فایل دیگری را ارسال نمایید."
        )
        return
    doc = Document(None, message.document.file_id, message.document.file_unique_id)
    doc.owner_title = message.from_user.first_name
    global staged_docs
    staged_docs[message.from_user.id] = doc
    user_step = UXTree.nodes[UserSteps.DOCUMENT_SUBMISSION.value]
    await message.reply_document(document=message.document.file_id, caption=str(doc))
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(message.from_user.id, UserSteps.DOCUMENT_SUBMISSION.value)


@Client.on_message(user_step(UserSteps.DOCUMENT_SUBMISSION.value) & filters.text)
async def choose_doc_field(client, message):
    """
    This function handles the user's selection of document fields during the document submission process.

    Parameters:
    - client: The Telegram client.
    - message: The message object containing the user's input.

    Returns:
    None
    """
    # Routing the user to input file data fields
    user_step = UXTree.nodes[UserSteps.DOCUMENT_SUBMISSION.value]
    global staged_docs
    if message.from_user.id not in staged_docs:
        await message.reply(text="خطای گم شدن فایل، لطفا مجددا تلاش کنید.")
        await start_stage(client, message)
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
        doc = staged_docs.pop(message.from_user.id)
        final_doc = user_db.add_user_submission(message.from_user.id, doc)
        sent_message = None
        if final_doc:
            sent_message = await client.send_document(
                chat_id=STORAGE_CHAT_ID,
                document=final_doc.file_id,
                caption=final_doc.user_display(),
            )
        if sent_message:
            await message.reply(
                text="فایل شما با موفقیت ثبت شد و پس از تایید در دسترس کاربران قرار خواهد گرفت. \nبا سپاس از همراهی شما"
            )
        else:
            await message.reply(
                "متاسفانه مشکلی در ثبت فایل شما به وجود آمده است. لطفا مجددا تلاش کنید."
            )
        await start_stage(client, message)

    # Cancel Button
    elif message.text.strip() == Triggers.DOCUMENT_SUBMISSION_CANCEL.value:
        # User has canceled the submission process
        await message.reply("عملیات ارسال فایل لغو شد.")
        if message.from_user.id in staged_docs:
            staged_docs.pop(message.from_user.id)
        await start_stage(client, message)

    else:
        await message.reply("لطفا یکی از گزینه های موجود را انتخاب کنید.")


# ---------------------- Inputting data fields ----------------------


async def go_back(client, message, step):
    # Going back to previous step
    user_step = UXTree.nodes[step]
    await message.reply(
        text=user_step.parent.description, reply_markup=user_step.parent.keyboard
    )
    user_db.update_user_step(message.from_user.id, user_step.parent.step)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_COURSE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_course(
    client,
    message,
):
    """
    Handles the submission of a document for a specific course.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting course name
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.course = message.text.strip()
    await message.reply("درس فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_COURSE.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_professor(
    client,
    message,
):
    """
    Handles the submission of a document by a professor.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting professor name
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.professor = message.text.strip()
    await message.reply("استاد فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_WRITER.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_writer(
    client,
    message,
):
    """
    Function to handle document submission by the writer.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting the writer of the document
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.writer = message.text.strip()
    await message.reply("نویسنده فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_FACULTY.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_faculty(
    client,
    message,
):
    """
    Function to handle the submission of the faculty for a document.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting the faculty of the document
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.faculty = message.text.strip()
    await message.reply("دانشکده فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_FACULTY.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_university(
    client,
    message,
):
    """
    Handles the submission of a document's university.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting the university of the document
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.university = message.text.strip()
    await message.reply("دانشگاه فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_owner_title(
    client,
    message,
):
    """
    Sets the owner title of the document.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.owner_title = message.text.strip()
    await message.reply("عنوان صاحب فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_description(
    client,
    message,
):
    """
    Handles the input of the description for a document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting the description of the document
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.description = message.text.strip()
    await message.reply("توضیحات فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_year(
    client,
    message,
):
    """
    Sets the semester year for the document submission.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    # Inputting the semester if its number, show error otherwise
    sem = 0
    try:
        sem = int(message.text.strip())
    except:
        await message.reply("لطفا یک عدد وارد کنید.")
        return
    global staged_docs
    doc = staged_docs[message.from_user.id]
    doc.semester_year = sem
    await message.reply("سال تهیه فایل شما با موفقیت ثبت شد.")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value)


@Client.on_message(
    user_step(UserSteps.DOCUMENT_SUBMISSION_FILE_TYPE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_file_type(
    client,
    message,
):
    """
    Handles the document file type selection step in the document submission process.

    Args:
        client: The client instance.
        message: The message object.

    Returns:
        None
    """
    # Inputting the faculty of the document
    global staged_docs
    doc = staged_docs[message.from_user.id]
    for c in DocType:
        if c.value == message.text.strip():
            doc.file_type = c
            await message.reply("نوع فایل شما با موفقیت ثبت شد.")
            await message.reply_document(document=doc.file_id, caption=str(doc))
            await go_back(
                client, message, UserSteps.DOCUMENT_SUBMISSION_FILE_TYPE.value
            )
            return

    await message.reply("لطفا یکی از گزینه های زیر را انتخاب کنید.")
