from django.urls import path, include
from contentadmin.views import (
    Sub_form,
    add_chapter,
    add_course,
    add_topic,
    admin_login,
    dashboard,
    delete,
    individual_subject_dashboard,
    login,
    logout,
    material_dashboard,
    update_chapter_title,
    update_content,
    update_logo,
    update_seo,
    update_subject,
    update_topic_title,
)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("addcourse", Sub_form, name="form_page"),
    path("course", add_course, name="course"),
    path(
        "dashboard/<slug:slug>", individual_subject_dashboard, name="subject_dashboard"
    ),
    path(
        "dashboard/<slug:subject>/<slug:chapter>/<slug:topic>/",
        material_dashboard,
        name="material_dashboard",
    ),
    path("subject", update_subject, name="subject"),
    path("chaptertitle", update_chapter_title, name="update_chapter_title"),
    path("topictitle", update_topic_title, name="update_topic_title"),
    path("chapter", add_chapter, name="add_chapter"),
    path("topic", add_topic, name="add_topic"),
    path("logo", update_logo, name="update_logo"),
    path("seo", update_seo, name="update_seo"),
    path("content", update_content, name="update_content"),
    path("delete", delete, name="delete"),
    path("adminlogin", admin_login, name="admin_login"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
]
