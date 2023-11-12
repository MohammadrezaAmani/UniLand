from uniland.utils.steps import UserSteps
from uniland.utils.pages import Pages
from uniland.utils.triggers import Triggers
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
        description="به ربات یونیلند خوش آمدید.",
        trigger="/start",
    )

    # ----------------- PV Search -----------------
    nodes[UserSteps.SEARCH.value] = UXNode(
        step=UserSteps.SEARCH.value,
        parent=nodes[UserSteps.START.value],
        description="لطفا متن جستجو را وارد کنید: ",
        keyboard=Pages.BACK,
        trigger=Triggers.SEARCH.value,
    )

    # ----------------- Starting Submission -----------------
    nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value] = UXNode(
        step=UserSteps.CHOOSE_SUBMISSION_TYPE.value,
        parent=nodes[UserSteps.START.value],
        description="لطفا نوع محتوای ارسالی خود را مشخص کنید:\n(توضیح مختصر این بخش را در راهنمای ربات مطالعه نمایید.)",
        keyboard=Pages.CHOOSE_SUBMISSION_TYPE,
        trigger=Triggers.CHOOSE_SUBMISSION_TYPE.value,
    )

    # ----------------- Document Submission -----------------
    nodes[UserSteps.DOCUMENT_SUBMISSION_FILE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_FILE.value,
        keyboard=Pages.BACK,
        description="لطفا فایل مورد نظر خود را ارسال کنید:\n(می‌توانید فایل را فوروارد کنید، نگران کپشن آن هم نباشید😁)",
        parent=nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
        trigger=Triggers.DOCUMENT_SUBMISSION_FILE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION.value,
        keyboard=Pages.DOCUMENT_SUBMISSION,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION_FILE.value],
        description="مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.",
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_FILE_TYPE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_FILE_TYPE.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا نوع فایل مورد نظر خود را انتخاب کنید.",
        keyboard=Pages.DOCUMENT_SUBMISSION_FILE_TYPE,
        trigger=Triggers.DOCUMENT_SUBMISSION_FILE_TYPE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا نام دانشگاه مربوطه را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_UNIVERSITY.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا نام دانشکده مربوطه را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_FACULTY.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="می‌خواهید نام ثبت کننده فایل چه باشد؟"
        " می‌توانید نام کامل یا مستعار خود را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا توضیحات مورد نظرتان را در مورد فایل خود وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_DESCRIPTION.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_COURSE.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_COURSE.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا نام درس مربوطه را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_COURSE.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا نام استاد درس را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_PROFESSOR.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_WRITER.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_WRITER.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا نام تهیه‌کننده یا نویسنده فایل را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_WRITER.value,
    )
    nodes[UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value] = UXNode(
        step=UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
        parent=nodes[UserSteps.DOCUMENT_SUBMISSION.value],
        description="لطفا سال تهیه فایل را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
    )

    # ----------------- Profile Submission -----------------
    nodes[UserSteps.PROFILE_SUBMISSION_INPUT_TITLE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_INPUT_TITLE.value,
        parent=nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
        description="لطفا عنوان اطلاعات را وارد کنید:",
        keyboard=Pages.BACK,
        trigger=Triggers.PROFILE_SUBMISSION_INPUT_TITLE.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION_INPUT_TITLE.value],
        keyboard=Pages.PROFILE_SUBMISSION,
        description="مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.",
        trigger=Triggers.PROFILE_SUBMISSION.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_EDIT_TITLE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_EDIT_TITLE.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا عنوان جدید را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_EDIT_TITLE.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_PHOTO.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_PHOTO.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.EDIT_PROFILE_SUBMISSION_PHOTO,
        # description='.لطفا عکس جدید یا لینک آن را ارسال کنید',
        description="لطفا عکس جدید را ارسال کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_PHOTO.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا نام دانشگاه مربوطه را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_UNIVERSITY.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا نام دانشکده مربوطه را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_FACULTY.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="می خواهید نام ثبت کننده فایل چه باشد؟"
        " می توانید نام کامل یا مستعار خود را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_OWNER_TITLE.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا توضیحات مورد نظر خود وارد کنید ",
        trigger=Triggers.PROFILE_SUBMISSION_DESCRIPTION.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_EMAIL.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_EMAIL.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا اطلاعات ایمیل را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_EMAIL.value,
    )
    nodes[UserSteps.PROFILE_SUBMISSION_PHONE.value] = UXNode(
        step=UserSteps.PROFILE_SUBMISSION_PHONE.value,
        parent=nodes[UserSteps.PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description=".لطفا اطلاعات شماره تلفن را وارد کنید",
        trigger=Triggers.PROFILE_SUBMISSION_PHONE.value,
    )

    # ----------------- Media Submission -----------------
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
        trigger=Triggers.ADMIN_PANEL.value,
        keyboard=Pages.ADMIN_PANEL,
        description="پنل ادمین",
    )

    nodes[UserSteps.SHOW_STATISTICS.value] = UXNode(
        step=UserSteps.SHOW_STATISTICS.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        trigger="/stats",
    )
    # nodes[UserSteps.GET_SUBMISSION_TO_APPROVE.value] = UXNode(
    #   step=UserSteps.GET_SUBMISSION_TO_APPROVE.value,
    #   parent=nodes[UserSteps.ADMIN_PANEL.value],
    #   # keyboard=Pages.ADMIN_PANEL.value,
    #   trigger=Triggers.GET_SUBMISSION_TO_APPROVE.value,
    # )

    nodes[UserSteps.GET_REJECTION_REASON.value] = UXNode(
        step=UserSteps.GET_REJECTION_REASON.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        keyboard=Pages.BACK,
    )

    nodes[UserSteps.UPDATE_USER_ACCESS.value] = UXNode(
        step=UserSteps.UPDATE_USER_ACCESS.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        description=Messages.ACCESS_LEVEL_BY_USERID.value,
        keyboard=Pages.BACK,
        trigger="تغییر سطح دسترسی کاربران",
    )
    # nodes[UserSteps.CHOOSE_USER_TO_UPDATE.value] = UXNode(
    #   step=UserSteps.CHOOSE_USER_TO_UPDATE.value,
    #   parent=nodes[UserSteps.UPDATE_USER_ACCESS.value],
    #   trigger="انتخاب کاربر",
    # )
    nodes[UserSteps.CHOOSE_USER_ACCESS_LEVEL.value] = UXNode(
        step=UserSteps.CHOOSE_USER_ACCESS_LEVEL.value,
        parent=nodes[UserSteps.UPDATE_USER_ACCESS.value],
        trigger="انتخاب سطح دسترسی",
        keyboard=Pages.ADMIN_PANEL_CHOOSE_NEW_ACCESS_LEVEL,
    )

    # ----------------- Edit Submission -----------------

    nodes[UserSteps.EDIT_SUBMISSION.value] = UXNode(
        step=UserSteps.EDIT_SUBMISSION.value,
        parent=nodes[UserSteps.ADMIN_PANEL.value],
        trigger=Triggers.EDIT_SUBMISSION,
        description="لطفا شماره فایل یا اطلاعات مورد نظرتان را وارد کنید.",
        keyboard=Pages.BACK,
    )
    # #--------------- EDIT DOCUMENT SUBMISSION -------------

    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION.value,
        keyboard=Pages.EDIT_DOCUMENT_SUBMISSION,
        parent=nodes[UserSteps.EDIT_SUBMISSION.value],
        description="مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.",
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_FILE_TYPE.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_FILE_TYPE.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا نوع فایل مورد نظر خود را انتخاب کنید.",
        keyboard=Pages.DOCUMENT_SUBMISSION_FILE_TYPE,
        trigger=Triggers.DOCUMENT_SUBMISSION_FILE_TYPE.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا نام دانشگاه مربوطه را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_UNIVERSITY.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا نام دانشکده مربوطه را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_FACULTY.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="می خواهید نام ثبت کننده فایل چه باشد؟"
        " می توانید نام کامل یا مستعار خود را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا توضیحات مورد نظرتان را در مورد فایل خود وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_DESCRIPTION.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_COURSE.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_COURSE.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا نام درس مربوطه را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_COURSE.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_PROFESSOR.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_PROFESSOR.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا نام استاد درس را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_PROFESSOR.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_WRITER.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_WRITER.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا نام تهیه‌کننده یا نویسنده فایل را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_WRITER.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="لطفا سال تهیه فایل را وارد کنید.",
        keyboard=Pages.BACK,
        trigger=Triggers.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
    )
    nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value] = UXNode(
        step=UserSteps.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value,
        parent=nodes[UserSteps.EDIT_DOCUMENT_SUBMISSION.value],
        description="آیا از حذف این فایل اطمینان دارید؟\nاین عمل قابل بازگشت نخواهد بود...",
        keyboard=Pages.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION,
        trigger=Triggers.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value,
    )

    # ---------------- EDIT PROFILE SUBMISSION ----------------
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION.value,
        keyboard=Pages.EDIT_PROFILE_SUBMISSION,
        parent=nodes[UserSteps.EDIT_SUBMISSION.value],
        description="مشخصاتی که می‌خواهید تغییر دهید را انتخاب کنید.",
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_TITLE.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_TITLE.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        description="لطفا عنوان جدید اطلاعات را وارد کنید:",
        keyboard=Pages.BACK,
        trigger=Triggers.PROFILE_SUBMISSION_EDIT_TITLE.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_PHOTO.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_PHOTO.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.EDIT_PROFILE_SUBMISSION_PHOTO,
        # description='.لطفا عکس جدید یا لینک آن را ارسال کنید',
        description="لطفا عکس جدید را ارسال کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_PHOTO.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_UNIVERSITY.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_UNIVERSITY.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا نام دانشگاه مربوطه را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_UNIVERSITY.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_FACULTY.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_FACULTY.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا نام دانشکده مربوطه را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_FACULTY.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_OWNER_TITLE.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_OWNER_TITLE.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="می خواهید نام ثبت کننده فایل چه باشد؟"
        " می توانید نام کامل یا مستعار خود را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_OWNER_TITLE.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_DESCRIPTION.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_DESCRIPTION.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا توضیحات مورد نظر خود وارد کنید ",
        trigger=Triggers.PROFILE_SUBMISSION_DESCRIPTION.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_EMAIL.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_EMAIL.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description="لطفا اطلاعات ایمیل را وارد کنید.",
        trigger=Triggers.PROFILE_SUBMISSION_EMAIL.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_PHONE.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_PHONE.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        keyboard=Pages.BACK,
        description=".لطفا اطلاعات شماره تلفن را وارد کنید",
        trigger=Triggers.PROFILE_SUBMISSION_PHONE.value,
    )
    nodes[UserSteps.EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION.value] = UXNode(
        step=UserSteps.EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION.value,
        parent=nodes[UserSteps.EDIT_PROFILE_SUBMISSION.value],
        description="آیا از حذف این فایل اطمینان دارید؟\nاین عمل قابل بازگشت نخواهد بود...",
        keyboard=Pages.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION,
        trigger=Triggers.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value,
    )
