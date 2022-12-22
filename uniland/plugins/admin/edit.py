from pyrogram import Client, filters
from uniland.utils.triggers import Triggers
import uniland.db.user_methods as user_db
import uniland.db.doc_methods as doc_db
from uniland.db.submission_methods import get_submission
from uniland.db.tables import Document
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match
from uniland.plugins.start.start import start_stage
from uniland.utils.enums import DocType
from uniland.config import STORAGE_CHAT_ID

staged_editted_docs = {}


@Client.on_message(filters.text & user_step(UserSteps.ADMIN_PANEL.value))
async def start_editing_data2(
    client,
    message,
):
    #! edit this part
    user_step = UXTree.nodes[UserSteps.EDIT_SUBMISSION.value]
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(message.from_user.id, UserSteps.EDIT_SUBMISSION.value)


@Client.on_message(filters.text & user_step(UserSteps.EDIT_SUBMISSION.value))
async def get_editing_id(
    client,
    message,
):
    #! edit this part
    user_step = UXTree.nodes[UserSteps.EDIT_ID.value]
    try:
        submission = get_submission(int(message.text))
        if submission == None:
            await message.reply("Submission not found")
        if submission.submission_type == DocType.DOCUMENT.value:
            user_step = UXTree.nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value]
            await message.reply(
                user_step.description.value, reply_markup=user_step.keyboard.value
            )
            user_db.update_user_step(
                message.from_user.id, UserSteps.EDIT_DOCUMENT_SUBMISSION.value
            )
            global staged_editted_docs
            staged_editted_docs[message.from_user.id] = submission
        #! oncomment this part before applying the edit profile
        # else:
        #     user_step = UXTree.nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value]
        #     staged_editted_docs[message.from_user.id] = submission
        #     await message.reply(user_step.description.value, reply_markup=user_step.keyboard.value)
        #     user_db.update_user_step(
        #         message.from_user.id, UserSteps.EDIT_PROFILE_SUBMISSION.value
        #     )

    # print(get_submission(1))
    except Exception as e:
        print(e)

    # await message.reply(text=user_step.description, reply_markup=user_step.keyboard)


@Client.on_message(filters.text & user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION.value))
async def start_editing_data(
    client,
    message,
):
    #! edit this part
    user_step = UXTree.nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value]
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(
        message.from_user.id, UserSteps.EDIT_DOCUMENT_SUBMISSION_FILE.value
    )


async def go_back(client, message, step):
    # Going back to previous step
    user_step = UXTree.nodes[step]
    global staged_editted_docs
    staged_editted_docs.pop(message.from_user.id)
    await message.reply(
        text=user_step.parent.description, reply_markup=user_step.parent.keyboard
    )
    user_db.update_user_step(message.from_user.id, user_step.parent.step)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_COURSE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_course(
    client,
    message,
):
    # Editting course name
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.course = message.text.strip()
    await message.reply(".درس فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_COURSE.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_PROFESSOR.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_professor(
    client,
    message,
):
    # Editting professor name
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.professor = message.text.strip()
    await message.reply(".استاد فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_PROFESSOR.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_WRITER.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_writer(
    client,
    message,
):
    # Editting the writer of the document
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.writer = message.text.strip()
    await message.reply(".نویسنده فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_PROFESSOR.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_FACULTY.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_faculty(
    client,
    message,
):
    # Editting the faculty of the document
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.faculty = message.text.strip()
    await message.reply(".دانشکده فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_FACULTY.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_UNIVERSITY.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_university(
    client,
    message,
):
    # Editting the university of the document
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.university = message.text.strip()
    await message.reply(".دانشگاه فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_UNIVERSITY.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_owner_title(
    client,
    message,
):
    # Editting the owner title of the document
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.owner_title = message.text.strip()
    await message.reply(".عنوان صاحب فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_DESCRIPTION.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_description(
    client,
    message,
):
    # Editting the description of the document
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.description = message.text.strip()
    await message.reply(".توضیحات فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_DESCRIPTION.value)


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_year(
    client,
    message,
):
    # Editting the semester if its number, show error otherwise
    sem = 0
    try:
        sem = int(message.text.strip())
    except:
        await message.reply(".لطفا یک عدد وارد کنید")
        return
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    doc.semester_year = sem
    await message.reply(".سال تهیه فایل شما با موفقیت تغییر یافت")
    await message.reply_document(document=doc.file_id, caption=str(doc))
    await go_back(
        client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR.value
    )


@Client.on_message(
    user_step(UserSteps.EDIT_DOCUMENT_SUBMISSION_FILE_TYPE.value)
    & filters.text
    & ~exact_match(Triggers.BACK.value)
)
async def doc_file_type(
    client,
    message,
):
    # Editting the faculty of the document
    global staged_editted_docs
    doc = staged_editted_docs[message.from_user.id]
    for c in DocType:
        if c.value == message.text.strip():
            doc.file_type = c
            await message.reply(".نوع فایل شما با موفقیت تغییر یافت")
            await message.reply_document(document=doc.file_id, caption=str(doc))
            await go_back(
                client, message, UserSteps.EDIT_DOCUMENT_SUBMISSION_FILE_TYPE.value
            )
            return

    await message.reply(".لطفا یکی از گزینه‌های زیر را انتخاب کنید")
