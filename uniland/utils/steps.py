import enum


class UserSteps(enum.Enum):
    """
    Enum class representing the different steps in the user workflow.

    Each step is represented by a unique string value.

    Attributes:
        START: The starting stage of the workflow.
        SEARCH: The search branch of the workflow.
        SEARCH_SHOW_RESULTS: The search show results stage of the workflow.
        CHOOSE_SUBMISSION_TYPE: The choose submission type stage of the workflow.
        DOCUMENT_SUBMISSION_FILE: The document submission file stage of the workflow.
        DOCUMENT_SUBMISSION: The document submission process stage of the workflow.
        DOCUMENT_SUBMISSION_CANCEL: The document submission cancel stage of the workflow.
        DOCUMENT_SUBMISSION_FILE_TYPE: The document submission file type stage of the workflow.
        DOCUMENT_SUBMISSION_UNIVERSITY: The document submission university stage of the workflow.
        DOCUMENT_SUBMISSION_FACULTY: The document submission faculty stage of the workflow.
        DOCUMENT_SUBMISSION_OWNER_TITLE: The document submission owner title stage of the workflow.
        DOCUMENT_SUBMISSION_DESCRIPTION: The document submission description stage of the workflow.
        DOCUMENT_SUBMISSION_COURSE: The document submission course stage of the workflow.
        DOCUMENT_SUBMISSION_PROFESSOR: The document submission professor stage of the workflow.
        DOCUMENT_SUBMISSION_WRITER: The document submission writer stage of the workflow.
        DOCUMENT_SUBMISSION_SEMESTER_YEAR: The document submission semester year stage of the workflow.
        DOCUMENT_SUBMISSION_DONE: The document submission done stage of the workflow.
        PROFILE_SUBMISSION_INPUT_TITLE: The profile submission input title stage of the workflow.
        PROFILE_SUBMISSION: The profile submission process stage of the workflow.
        PROFILE_SUBMISSION_CANCEL: The profile submission cancel stage of the workflow.
        PROFILE_SUBMISSION_EDIT_TITLE: The profile submission edit title stage of the workflow.
        PROFILE_SUBMISSION_PHOTO: The profile submission photo stage of the workflow.
        PROFILE_SUBMISSION_UNIVERSITY: The profile submission university stage of the workflow.
        PROFILE_SUBMISSION_FACULTY: The profile submission faculty stage of the workflow.
        PROFILE_SUBMISSION_OWNER_TITLE: The profile submission owner title stage of the workflow.
        PROFILE_SUBMISSION_DESCRIPTION: The profile submission description stage of the workflow.
        PROFILE_SUBMISSION_EMAIL: The profile submission email stage of the workflow.
        PROFILE_SUBMISSION_PHONE: The profile submission phone stage of the workflow.
        PROFILE_SUBMISSION_DONE: The profile submission done stage of the workflow.
        MEDIA_SUBMISSION: The media submission process stage of the workflow.
        MEDIA_SUBMISSION_UNIVERSITY: The media submission university stage of the workflow.
        MEDIA_SUBMISSION_FACULTY: The media submission faculty stage of the workflow.
        MEDIA_SUBMISSION_OWNER_TITLE: The media submission owner title stage of the workflow.
        MEDIA_SUBMISSION_DESCRIPTION: The media submission description stage of the workflow.
        MEDIA_SUBMISSION_URL: The media submission URL stage of the workflow.
        MEDIA_SUBMISSION_MEDIA_TYPE: The media submission media type stage of the workflow.
        MEDIA_SUBMISSION_COURSE: The media submission course stage of the workflow.
        MEDIA_SUBMISSION_PROFESSOR: The media submission professor stage of the workflow.
        MEDIA_SUBMISSION_SEMESTER_YEAR: The media submission semester year stage of the workflow.
        ADMIN_PANEL: The admin panel stage of the workflow.
        SHOW_STATISTICS: The show statistics stage of the workflow.
        GET_SUBMISSION_TO_APPROVE: The get files to approve stage of the workflow.
        GET_REJECTION_REASON: The get rejection reason stage of the workflow.
        UPDATE_USER_ACCESS: The update user access stage of the workflow.
        CHOOSE_USER_TO_UPDATE: The choose user to update stage of the workflow.
        CHOOSE_USER_ACCESS_LEVEL: The choose user access level stage of the workflow.
        EDIT_SUBMISSION: The edit submission stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION: The edit document submission stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION: The edit document submission remove caution stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_FILE: The edit document submission file stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_FILE_TYPE: The edit document submission file type stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_UNIVERSITY: The edit document submission university stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_FACULTY: The edit document submission faculty stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE: The edit document submission owner title stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_DESCRIPTION: The edit document submission description stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_COURSE: The edit document submission course stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_PROFESSOR: The edit document submission professor stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_WRITER: The edit document submission writer stage of the workflow.
        EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR: The edit document submission semester year stage of the workflow.
        EDIT_PROFILE_SUBMISSION: The edit profile submission stage of the workflow.
        EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION: The edit profile submission remove caution stage of the workflow.
        EDIT_PROFILE_SUBMISSION_TITLE: The edit profile submission title stage of the workflow.
        EDIT_PROFILE_SUBMISSION_CANCEL: The edit profile submission cancel stage of the workflow.
        EDIT_PROFILE_SUBMISSION_EDIT_TITLE: The edit profile submission edit title stage of the workflow.
        EDIT_PROFILE_SUBMISSION_PHOTO: The edit profile submission photo stage of the workflow.
        EDIT_PROFILE_SUBMISSION_UNIVERSITY: The edit profile submission university stage of the workflow.
        EDIT_PROFILE_SUBMISSION_FACULTY: The edit profile submission faculty stage of the workflow.
        EDIT_PROFILE_SUBMISSION_OWNER_TITLE: The edit profile submission owner title stage of the workflow.
        EDIT_PROFILE_SUBMISSION_DESCRIPTION: The edit profile submission description stage of the workflow.
        EDIT_PROFILE_SUBMISSION_EMAIL: The edit profile submission email stage of the workflow.
        EDIT_PROFILE_SUBMISSION_PHONE: The edit profile submission phone stage of the workflow.
        EDIT_PROFILE_SUBMISSION_DONE: The edit profile submission done stage of the workflow.
    """

    # ----------------- Start -----------------
    START = "start_stage"

    # ----------------- Search Branch -----------------
    SEARCH = "bot_pv_search"
    SEARCH_SHOW_RESULTS = "bot_pv_search_show_results"

    # ----------------- Submit Branch -----------------
    CHOOSE_SUBMISSION_TYPE = "submission_type_stage"

    DOCUMENT_SUBMISSION_FILE = "document_submission_file_stage"
    DOCUMENT_SUBMISSION = "document_submission_process"
    DOCUMENT_SUBMISSION_CANCEL = "document_submission_cancel"
    DOCUMENT_SUBMISSION_FILE_TYPE = "document_submission_type_stage"
    DOCUMENT_SUBMISSION_UNIVERSITY = "document_submission_university"
    DOCUMENT_SUBMISSION_FACULTY = "document_submission_faculty"
    DOCUMENT_SUBMISSION_OWNER_TITLE = "document_submission_owner_title"
    DOCUMENT_SUBMISSION_DESCRIPTION = "document_submission_description"
    DOCUMENT_SUBMISSION_COURSE = "document_submission_course_stage"
    DOCUMENT_SUBMISSION_PROFESSOR = "document_submission_professor_stage"
    DOCUMENT_SUBMISSION_WRITER = "document_submission_writer_stage"
    DOCUMENT_SUBMISSION_SEMESTER_YEAR = "document_submission_semester_year_stage"
    DOCUMENT_SUBMISSION_DONE = "document_submission_done_stage"

    PROFILE_SUBMISSION_INPUT_TITLE = "profile_submission_title"
    PROFILE_SUBMISSION = "profile_submission_process"
    PROFILE_SUBMISSION_CANCEL = "profile_submission_cancel"
    PROFILE_SUBMISSION_EDIT_TITLE = "profile_submission_edit_title"
    PROFILE_SUBMISSION_PHOTO = "profile_submission_photo"
    PROFILE_SUBMISSION_UNIVERSITY = "profile_submission_university"
    PROFILE_SUBMISSION_FACULTY = "profile_submission_faculty"
    PROFILE_SUBMISSION_OWNER_TITLE = "profile_submission_owner_title"
    PROFILE_SUBMISSION_DESCRIPTION = "profile_submission_description"
    PROFILE_SUBMISSION_EMAIL = "profile_submission_email"
    PROFILE_SUBMISSION_PHONE = "profile_submission_phone"
    PROFILE_SUBMISSION_DONE = "profile_submission_done_stage"

    MEDIA_SUBMISSION = "media_submission_process"
    MEDIA_SUBMISSION_UNIVERSITY = "media_submission_university"
    MEDIA_SUBMISSION_FACULTY = "media_submission_faculty"
    MEDIA_SUBMISSION_OWNER_TITLE = "media_submission_owner_title"
    MEDIA_SUBMISSION_DESCRIPTION = "media_submission_description"
    MEDIA_SUBMISSION_URL = "media_submission_url"
    MEDIA_SUBMISSION_MEDIA_TYPE = "media_submission_media_type"
    MEDIA_SUBMISSION_COURSE = "media_submission_course_stage"
    MEDIA_SUBMISSION_PROFESSOR = "media_submission_professor_stage"
    MEDIA_SUBMISSION_SEMESTER_YEAR = "media_submission_semester_year_stage"

    # ----------------- User Profile Branch -----------------
    # We don't need nodes for this, because we can just send it and interact
    # using InlineKeyboardMarkup.

    # ----------------- Admin Branch -----------------
    ADMIN_PANEL = "admin_panel_stage"
    SHOW_STATISTICS = "show_statistics"
    GET_SUBMISSION_TO_APPROVE = "get_files_to_approve"
    GET_REJECTION_REASON = "get_rejection_reason"
    UPDATE_USER_ACCESS = "update_user_access"
    CHOOSE_USER_TO_UPDATE = "choose_user_to_update"
    CHOOSE_USER_ACCESS_LEVEL = "choose_user_access_level"

    # ------------------ Edit FIle --------------------
    EDIT_SUBMISSION = "edit_submission_stage"

    EDIT_DOCUMENT_SUBMISSION = "edit_document_submission_stage"
    EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION = "edit_document_submission_remove_caution"
    EDIT_DOCUMENT_SUBMISSION_FILE = "edit_document_submission_file_stage"
    EDIT_DOCUMENT_SUBMISSION_FILE_TYPE = "edit_document_submission_type_stage"
    EDIT_DOCUMENT_SUBMISSION_UNIVERSITY = "edit_document_submission_university_stage"
    EDIT_DOCUMENT_SUBMISSION_FACULTY = "edit_document_submission_faculty_stage"
    EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE = "edit_document_submission_owner_title_stage"
    EDIT_DOCUMENT_SUBMISSION_DESCRIPTION = "edit_document_submission_description_stage"
    EDIT_DOCUMENT_SUBMISSION_COURSE = "edit_document_submission_course_stage"
    EDIT_DOCUMENT_SUBMISSION_PROFESSOR = "edit_document_submission_professor_stage"
    EDIT_DOCUMENT_SUBMISSION_WRITER = "edit_document_submission_writer_stage"
    EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR = (
        "edit_document_submission_semester_year_stage"
    )

    EDIT_PROFILE_SUBMISSION = "edit_profile_submission_stage"
    EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION = "edit_profile_submission_remove_caution"
    EDIT_PROFILE_SUBMISSION_TITLE = "edit_profile_submission_title_stage"
    EDIT_PROFILE_SUBMISSION_CANCEL = "edit_profile_submission_cancel"
    EDIT_PROFILE_SUBMISSION_EDIT_TITLE = "edit_profile_submission_edit_title_stage"
    EDIT_PROFILE_SUBMISSION_PHOTO = "edit_profile_submission_photo_stage"
    EDIT_PROFILE_SUBMISSION_UNIVERSITY = "edit_profile_submission_university_stage"
    EDIT_PROFILE_SUBMISSION_FACULTY = "edit_profile_submission_faculty_stage"
    EDIT_PROFILE_SUBMISSION_OWNER_TITLE = "edit_profile_submission_owner_title_stage"
    EDIT_PROFILE_SUBMISSION_DESCRIPTION = "edit_profile_submission_description_stage"
    EDIT_PROFILE_SUBMISSION_EMAIL = "edit_profile_submission_email_stage"
    EDIT_PROFILE_SUBMISSION_PHONE = "edit_profile_submission_phone_stage"
    EDIT_PROFILE_SUBMISSION_DONE = "edit_profile_submission_done"
