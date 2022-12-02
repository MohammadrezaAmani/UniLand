from uniland.utils.steps import UserSteps

class UXNode():
    
    def __init__(self,
                 step: str,
                 parent: 'UXNode' = None,
                 trigger: str = None,
                 keyboard: list = None,
                 required_permission: int = 1):
        self.step = step
        self.trigger = trigger
        self.keyboard = keyboard
        self.required_permission = required_permission
        self.parents = set()
        if parent:
            self.parents.add(parent)
        self.children = set()
        
    def add_parent(self, parent: 'UXNode'):
        self.parents.add(parent)
        parent.children.add(self)
        
    def __repr__(self):
        return str({'step': self.step,
                    'trigger': self.trigger,
                    'required_permission': self.required_permission})
        
class UXTree():
    
    def __init__(self):
        self.nodes = {}
        
        # initializing ux nodes
        # ----------------- START -----------------
        self.nodes[UserSteps.START.value] = UXNode(UserSteps.START.value)
        
        # ----------------- PV Search -----------------
        self.nodes[UserSteps.SEARCH.value] = \
            UXNode(step = UserSteps.SEARCH.value,
                   parent = self.nodes[UserSteps.START.value],
                   trigger='جستجو')
        
        # ----------------- Starting Submission -----------------
        self.nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value] = \
            UXNode(step = UserSteps.CHOOSE_SUBMISSION_TYPE.value,
                   parent = self.nodes[UserSteps.START.value],
                   trigger='ارسال محتوا')
        
        # ----------------- Document Submission -----------------
        self.nodes[UserSteps.DOCUMENT_SUBMISSION.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION.value,
                   parent = self.nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
                   trigger='ارسال فایل')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_UNIVERSITY.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'دانشگاه')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_FACULTY.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_FACULTY.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'دانشکده')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'نام ثبت کننده')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_DESCRIPTION.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'توضیحات')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_COURSE.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_COURSE.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'درس')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_PROFESSOR.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'استاد')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_WRITER.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_WRITER.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'نویسنده')
        self.nodes[UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value] = \
            UXNode(step = UserSteps.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
                   parent = self.nodes[UserSteps.DOCUMENT_SUBMISSION.value],
                   trigger = 'سال ترم')
        
        # ----------------- Media Submission -----------------
        self.nodes[UserSteps.PROFILE_SUBMISSION.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION.value,
                   parent = self.nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
                   trigger = 'ارسال اطلاعات')
        self.nodes[UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_UNIVERSITY.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = 'دانشگاه')
        self.nodes[UserSteps.PROFILE_SUBMISSION_FACULTY.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_FACULTY.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = self.nodes[UserSteps.PROFILE_SUBMISSION.value])
        self.nodes[UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_OWNER_TITLE.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = 'نام ثبت کننده')
        self.nodes[UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_DESCRIPTION.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = 'توضیحات')
        self.nodes[UserSteps.PROFILE_SUBMISSION_TITLE.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_TITLE.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = 'عنوان')
        self.nodes[UserSteps.PROFILE_SUBMISSION_EMAIL.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_EMAIL.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = 'ایمیل')
        self.nodes[UserSteps.PROFILE_SUBMISSION_PHONE.value] = \
            UXNode(step = UserSteps.PROFILE_SUBMISSION_PHONE.value,
                   parent = self.nodes[UserSteps.PROFILE_SUBMISSION.value],
                   trigger = 'تلفن')
        
        # ----------------- Profile Submission -----------------
        self.nodes[UserSteps.MEDIA_SUBMISSION.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION.value,
                   parent = self.nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value],
                   trigger = 'ارسال رسانه')
        self.nodes[UserSteps.MEDIA_SUBMISSION_UNIVERSITY.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_UNIVERSITY.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'دانشگاه')
        self.nodes[UserSteps.MEDIA_SUBMISSION_FACULTY.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_FACULTY.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'دانشکده')
        self.nodes[UserSteps.MEDIA_SUBMISSION_OWNER_TITLE.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_OWNER_TITLE.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'نام ثبت کننده')
        self.nodes[UserSteps.MEDIA_SUBMISSION_DESCRIPTION.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_DESCRIPTION.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'توضیحات')
        self.nodes[UserSteps.MEDIA_SUBMISSION_URL.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_URL.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'لینک محتوا')
        self.nodes[UserSteps.MEDIA_SUBMISSION_MEDIA_TYPE.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_MEDIA_TYPE.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'نوع رسانه')
        self.nodes[UserSteps.MEDIA_SUBMISSION_COURSE.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_COURSE.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'درس')
        self.nodes[UserSteps.MEDIA_SUBMISSION_PROFESSOR.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_PROFESSOR.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'استاد')
        self.nodes[UserSteps.MEDIA_SUBMISSION_SEMESTER_YEAR.value] = \
            UXNode(step = UserSteps.MEDIA_SUBMISSION_SEMESTER_YEAR.value,
                   parent = self.nodes[UserSteps.MEDIA_SUBMISSION.value],
                   trigger = 'سال ترم')
        
        # ----------------- Admin Controls -----------------
        self.nodes[UserSteps.ADMIN_PANEL.value] = \
            UXNode(step = UserSteps.ADMIN_PANEL.value,
                   parent = self.nodes[UserSteps.START.value],
                   trigger = '/admin')
        self.nodes[UserSteps.SHOW_STATISTICS.value] = \
            UXNode(step = UserSteps.SHOW_STATISTICS.value,
                   parent = self.nodes[UserSteps.ADMIN_PANEL.value],
                   trigger = '/stats')
        self.nodes[UserSteps.GET_SUBMISSION_TO_APPROVE.value] = \
            UXNode(step = UserSteps.GET_SUBMISSION_TO_APPROVE.value,
                   parent = self.nodes[UserSteps.ADMIN_PANEL.value],
                   trigger = '/submissions')
        self.nodes[UserSteps.UPDATE_USER_ACCESS.value] = \
            UXNode(step = UserSteps.UPDATE_USER_ACCESS.value,
                   parent = self.nodes[UserSteps.ADMIN_PANEL.value],
                   trigger = '/update_access')
        self.nodes[UserSteps.CHOOSE_USER_TO_UPDATE.value] = \
            UXNode(step = UserSteps.CHOOSE_USER_TO_UPDATE.value,
                   parent = self.nodes[UserSteps.UPDATE_USER_ACCESS.value],
                   trigger = 'انتخاب کاربر')
        self.nodes[UserSteps.CHOOSE_USER_ACCESS_LEVEL.value] = \
            UXNode(step = UserSteps.CHOOSE_USER_ACCESS_LEVEL.value,
                   parent = self.nodes[UserSteps.UPDATE_USER_ACCESS.value],
                   trigger = 'انتخاب سطح دسترسی')
            
        
