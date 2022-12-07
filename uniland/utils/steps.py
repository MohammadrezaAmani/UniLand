import enum


class UserSteps(enum.Enum):

    # ----------------- Start -----------------
    START = 'start_stage'

    # ----------------- Search Branch -----------------
    SEARCH = 'bot_pv_search'
    SEARCH_SHOW_RESULTS = 'bot_pv_search_show_results'

    # ----------------- Submit Branch -----------------
    CHOOSE_SUBMISSION_TYPE = 'submission_type_stage'

    DOCUMENT_SUBMISSION_FILE = 'document_submission_file_stage'
    DOCUMENT_SUBMISSION = 'document_submission_process'
    DOCUMENT_SUBMISSION_CANCEL = 'document_submission_cancel'
    DOCUMENT_SUBMISSION_FILE_TYPE = 'document_submission_type_stage'
    DOCUMENT_SUBMISSION_UNIVERSITY = 'document_submission_university'
    DOCUMENT_SUBMISSION_FACULTY = 'document_submission_faculty'
    DOCUMENT_SUBMISSION_OWNER_TITLE = 'document_submission_owner_title'
    DOCUMENT_SUBMISSION_DESCRIPTION = 'document_submission_description'
    DOCUMENT_SUBMISSION_COURSE = 'document_submission_course_stage'
    DOCUMENT_SUBMISSION_PROFESSOR = 'document_submission_professor_stage'
    DOCUMENT_SUBMISSION_WRITER = 'document_submission_writer_stage'
    DOCUMENT_SUBMISSION_SEMESTER_YEAR = 'document_submission_semester_year_stage'
    DOCUMENT_SUBMISSION_DONE = 'document_submission_done_stage'

    PROFILE_SUBMISSION_INPUT_TITLE = 'profile_submission_title'
    PROFILE_SUBMISSION = 'profile_submission_process'
    PROFILE_SUBMISSION_CANCEL = 'profile_submission_cancel'
    PROFILE_SUBMISSION_EDIT_TITLE = 'profile_submission_edit_title'
    PROFILE_SUBMISSION_PHOTO = 'profile_submission_photo'
    PROFILE_SUBMISSION_UNIVERSITY = 'profile_submission_university'
    PROFILE_SUBMISSION_FACULTY = 'profile_submission_faculty'
    PROFILE_SUBMISSION_OWNER_TITLE = 'profile_submission_owner_title'
    PROFILE_SUBMISSION_DESCRIPTION = 'profile_submission_description'
    PROFILE_SUBMISSION_EMAIL = 'profile_submission_email'
    PROFILE_SUBMISSION_PHONE = 'profile_submission_phone'
    PROFILE_SUBMISSION_DONE = 'profile_submission_done_stage'

    MEDIA_SUBMISSION = 'media_submission_process'
    MEDIA_SUBMISSION_UNIVERSITY = 'media_submission_university'
    MEDIA_SUBMISSION_FACULTY = 'media_submission_faculty'
    MEDIA_SUBMISSION_OWNER_TITLE = 'media_submission_owner_title'
    MEDIA_SUBMISSION_DESCRIPTION = 'media_submission_description'
    MEDIA_SUBMISSION_URL = 'media_submission_url'
    MEDIA_SUBMISSION_MEDIA_TYPE = 'media_submission_media_type'
    MEDIA_SUBMISSION_COURSE = 'media_submission_course_stage'
    MEDIA_SUBMISSION_PROFESSOR = 'media_submission_professor_stage'
    MEDIA_SUBMISSION_SEMESTER_YEAR = 'media_submission_semester_year_stage'

    # ----------------- User Profile Branch -----------------
    # We don't need nodes for this, because we can just send it and interact
    # using InlineKeyboardMarkup.

    # ----------------- Admin Branch -----------------
    ADMIN_PANEL = 'admin_panel_stage'
    SHOW_STATISTICS = 'show_statistics'
    GET_SUBMISSION_TO_APPROVE = 'get_files_to_approve'
    UPDATE_USER_ACCESS = 'update_user_access'
    CHOOSE_USER_TO_UPDATE = 'choose_user_to_update'
    CHOOSE_USER_ACCESS_LEVEL = 'choose_user_access_level'
