from uniland.utils.steps import UserSteps
from uniland.utils.pages import Pages
from uniland.utils.messages import Messages

class UXNode:
    def __init__(
        self,
        step: str,
        parent: "UXNode" = None,
        trigger: str = None,
        keyboard: list = None,
        description: str = "",
        required_permission: int = 1,
    ):
        self.step = step
        self.trigger = trigger
        self.keyboard = keyboard
        self.required_permission = required_permission
        self.description = description
        self.parent = None
        if parent:
            self.set_parent(parent)
        self.children = set()

    def set_parent(self, parent: "UXNode"):
        self.parent = parent
        parent.children.add(self)

    def __repr__(self):
        return str(
            {
                "step": self.step,
                "trigger": self.trigger,
                "required_permission": self.required_permission,
            }
        )


class UXTree:
    nodes = {}

    # initializing ux nodes
    # ----------------- START -----------------
    nodes[UserSteps.START.value] = UXNode(
        UserSteps.START.value,
        keyboard=Pages.HOME,
        description='This is uniland bot for testing purposes',
        trigger='/start',
    )

    # ----------------- PV Search -----------------
    nodes[UserSteps.SEARCH.value] = UXNode(
        step=UserSteps.SEARCH.value,
        parent=nodes[UserSteps.START.value],
        trigger=Messages.SEARCH.value,
    )

    # ----------------- Starting Submission -----------------
    nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value] = UXNode(
        step=UserSteps.CHOOSE_SUBMISSION_TYPE.value,
        parent=nodes[UserSteps.START.value],
        description='لطفا نوع محتوای ارسالی خود را مشخص کنید:',
        keyboard=Pages.CHOOSE_SUBMISSION_TYPE,
        trigger=Messages.CHOOSE_SUBMISSION_TYPE.value,
    )

    # ----------------- Document Submission -----------------
    nodes[UserSteps.DOCUMENT_SUBMISSION_FILE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_FILE.value,
        keyboard=Pages.BACK,
        description='لطفا فایل مورد نظر خود را ارسال کنید:',
        parent=nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
        trigger=Messages.DOCUMENT_SUBMISSION_FILE.value
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION.value,
        keyboard=Pages.DOCUMENT_SUBMISSION,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION_FILE.value],
        description='مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید',
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_FILE_TYPE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_FILE_TYPE.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا نوع فایل مورد نظر خود را انتخاب کنید',
        keyboard=Pages.DOCUMENT_SUBMISSION_FILE_TYPE,
        trigger=Messages.DOCUMENT_SUBMISSION_FILE_TYPE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا نام دانشگاه مربوطه را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_UNIVERSITY.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا دانشکده مربوطه را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_FACULTY.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='می خواهید نام ثبت کننده فایل چه باشد؟'\
            'می توانید نام کامل یا مستعار خود را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا توضیحات مورد نظرتان را در مورد فایل خود وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_DESCRIPTION.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_COURSE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_COURSE.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا نام درس مربوطه را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_COURSE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا نام استاد درس را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_PROFESSOR.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_WRITER.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_WRITER.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا نام تهیه کننده یا نویسنده فایل را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_WRITER.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description='لطفا سال تهیه فایل را وارد کنید',
        trigger=Messages.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
    )

    # ----------------- Media Submission -----------------
    nodes[UserSteps.PROFILE_SUBMISSION.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION.value,
        parent=nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
        keyboard=Pages.MEDIA_SUBMISSION,
        trigger="ارسال اطلاعات",
    )
    nodes[UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger="دانشگاه",
    )
    nodes[UserSteps.PROFILE_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger=nodes[UserSteps.PROFILE_SUBMISSION.value],
    )
    nodes[UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger="نام ثبت کننده",
    )
    nodes[UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger="توضیحات",
    )
    nodes[UserSteps.PROFILE_SUBMISSION_TITLE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_TITLE.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger="عنوان",
    )
    nodes[UserSteps.PROFILE_SUBMISSION_EMAIL.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_EMAIL.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger="ایمیل",
    )
    nodes[UserSteps.PROFILE_SUBMISSION_PHONE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_PHONE.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        trigger="تلفن",
    )

    # ----------------- Profile Submission -----------------
    nodes[UserSteps.MEDIA_SUBMISSION.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION.value,
        parent=nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
        keyboard=Pages.PROFILE_SUBMISSION,
        trigger="ارسال رسانه",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="دانشگاه",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="دانشکده",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="نام ثبت کننده",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="توضیحات",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_URL.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_URL.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="لینک محتوا",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_MEDIA_TYPE.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_MEDIA_TYPE.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="نوع رسانه",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_COURSE.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_COURSE.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="درس",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_PROFESSOR.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_PROFESSOR.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="استاد",
    )
    nodes[UserSteps.MEDIA_SUBMISSION_SEMESTER_YEAR.value] = UXNode(
        step=UserSteps.MEDIA_SUBMISSION_SEMESTER_YEAR.value,
        parent=nodes[UserSteps.MEDIA_SUBMISSION.value],
        trigger="سال ترم",
    )

    # ----------------- Admin Controls -----------------
    nodes[UserSteps.ADMIN_PANEL.value] = UXNode(
        step=UserSteps.ADMIN_PANEL.value,
        parent=nodes[UserSteps.START.value],
        trigger="/admin",
    )
    nodes[UserSteps.SHOW_STATISTICS.value] = UXNode(
        step=UserSteps.SHOW_STATISTICS.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        trigger="/stats",
    )
    nodes[UserSteps.GET_SUBMISSION_TO_APPROVE.value] = UXNode(
        step=UserSteps.GET_SUBMISSION_TO_APPROVE.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        trigger="/submissions",
    )
    nodes[UserSteps.UPDATE_USER_ACCESS.value] = UXNode(
        step=UserSteps.UPDATE_USER_ACCESS.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        trigger="/update_access",
    )
    nodes[UserSteps.CHOOSE_USER_TO_UPDATE.value] = UXNode(
        step=UserSteps.CHOOSE_USER_TO_UPDATE.value,
        parent=nodes[UserSteps.UPDATE_USER_ACCESS.value],
        trigger="انتخاب کاربر",
    )
    nodes[UserSteps.CHOOSE_USER_ACCESS_LEVEL.value] = UXNode(
        step=UserSteps.CHOOSE_USER_ACCESS_LEVEL.value,
        parent=nodes[UserSteps.UPDATE_USER_ACCESS.value],
        trigger="انتخاب سطح دسترسی",
    )
