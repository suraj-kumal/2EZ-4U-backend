import os
import uuid
from django.http import Http404
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, redirect, render
from content.models import Chapter, SeoContent, Subject, Topic, Material
from django.core.files.storage import default_storage
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Max
from tutorialsite import settings
from decouple import config

ADMIN_USERNAME = config("ADMIN_USERNAME")
ADMIN_PASSWORD = config("ADMIN_PASSWORD")


def check_session(request):
    if request.session.get("username") != ADMIN_USERNAME:
        return redirect("admin_login")
    return None


def admin_login(request):
    if request.session.get("username") == ADMIN_USERNAME:
        return redirect("dashboard")
    return render(request, "admin_login.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session["username"] = username
            return redirect("dashboard")

        else:
            messages.error(request, "invalid credientials")
            return redirect("admin_login")


def logout(request):
    request.session.flush()
    return redirect("admin_login")


def dashboard(request):
    check = check_session(request)
    if check:
        return check

    subjects = Subject.objects.filter(is_active=True).order_by("-created_at")

    for subject in subjects:
        if subject.logo and not default_storage.exists(subject.logo.name):
            subject.logo = None
    context = {
        "subjects": subjects,
    }

    return render(request, "dashboard.html", context)


def clean_html_styles(html_content):
    """Remove inline styles and unnecessary nested spans"""
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, "html.parser")

    for element in soup.find_all():
        if element.has_attr("style"):
            del element["style"]
    for span in soup.find_all("span"):
        if not span.attrs:
            span.unwrap()

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text == "" or text == "\u00a0":
            p.decompose()

    return str(soup)


def individual_subject_dashboard(request, slug):
    check = check_session(request)
    if check:
        return check
    try:
        subject = Subject.objects.get(slug=slug)
    except Subject.DoesNotExist:
        raise Http404("Subject not found")

    cleaned_description = clean_html_styles(subject.description)
    chapters = Chapter.objects.filter(subject=subject).order_by("order_priority")
    logo_path = (
        os.path.join(settings.MEDIA_ROOT, subject.logo.name) if subject.logo else None
    )
    logo_exists = os.path.isfile(logo_path) if logo_path else False

    try:
        seo = SeoContent.objects.get(subject_id=subject.uid)
    except SeoContent.DoesNotExist:
        seo = SeoContent.objects.create(
            title=subject.title,
            meta_description="",
            subject_id=subject.uid,
            keywords="",
        )

    context = {
        "subject": subject,
        "seo": seo,
        "logo_exists": logo_exists,
        "cleaned_description": cleaned_description,
        "chapters": chapters,
    }

    return render(request, "subject.html", context)


def material_dashboard(request, subject, chapter, topic):
    check = check_session(request)
    if check:
        return check

    chap = get_object_or_404(Chapter, slug=chapter)
    top = get_object_or_404(Topic, slug=topic)
    material = get_object_or_404(Material, topic_id=top.uid)

    cleaned_material = clean_html_styles(material.content)

    context = {
        "subjectslug": subject,
        "chapter": chap,
        "topic": top,
        "material": material,
        "cleaned_material": cleaned_material,
    }

    return render(request, "material.html", context)


def update_subject(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        uid = request.POST.get("uid")

        # if not uid:
        #     messages.error(request, "Subject ID is required")
        #     return redirect("subject_dashboard", slug=slug)

        try:
            subject = get_object_or_404(Subject, uid=uid)
            slug = subject.slug

            if request.POST.get("title"):
                title = request.POST.get("title")
                subject.title = title
                subject.save()
                messages.success(request, "Title updated successfully")
                return redirect("subject_dashboard", slug=slug)

            elif request.POST.get("description"):
                description = request.POST.get("description")
                subject.description = description
                subject.save()
                messages.success(request, "Description updated successfully")
                return redirect("subject_dashboard", slug=slug)

            else:
                messages.error(request, "No data provided for update")
                return redirect("subject_dashboard", slug=slug)

        except Exception as e:
            messages.error(request, f"Update failed: {str(e)}")
            if "slug" in locals():
                return redirect("subject_dashboard", slug=slug)
            else:
                return redirect("subject_dashboard", slug=slug)

    else:
        return redirect("dashboard")


def update_chapter_title(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        uid = request.POST.get("uid")
        Subjectslug = request.POST.get("slug")

    try:
        chapter = get_object_or_404(Chapter, uid=uid)
        title = request.POST.get("title")
        chapter.title = title
        chapter.save()

        messages.success(request, "Chapter title updated successfully")
        return redirect("subject_dashboard", slug=Subjectslug)

    except Exception as e:
        messages.error(request, f"Update failed: {str(e)}")
        if "slug" in locals():
            return redirect("subject_dashboard", slug=Subjectslug)
        else:
            return redirect("subject_dashboard", slug=Subjectslug)

    else:
        return redirect("dashboard")


def add_chapter(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        try:
            subject_uid = request.POST.get("uid")
            subject_slug = request.POST.get("slug")
            title = request.POST.get("chaptername")

            try:
                subject = Subject.objects.get(uid=subject_uid)
            except Subject.DoesNotExist:
                messages.error(request, "Invalid subject selected.")
                return redirect("subject_dashboard", slug=subject_slug)

            max_priority = Chapter.objects.filter(subject_id=subject.uid).aggregate(
                Max("order_priority")
            )["order_priority__max"]

            new_priority = (max_priority or 0) + 1
            chapter = Chapter.objects.create(
                uid=str(uuid.uuid4()).replace("-", ""),
                title=title,
                slug=slugify(title),
                is_active=True,
                order_priority=new_priority,
                subject_id=subject.uid,
            )

            messages.success(request, f"Chapter '{title}' added successfully!")
            return redirect("subject_dashboard", slug=subject_slug)

        except Exception as e:
            messages.error(request, f"Error adding chapter: {str(e)}")
            return redirect("subject_dashboard", slug=subject_slug)

    else:
        return redirect("dashboard")


def add_topic(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        try:
            chapter_uid = request.POST.get("uid")
            subject_slug = request.POST.get("slug")
            title = request.POST.get("topictitle")

            if not chapter_uid or not title:
                messages.error(request, "Chapter and Topic title are required.")
                return redirect("subject_dashboard", slug=subject_slug)

            try:
                chapter = Chapter.objects.get(uid=chapter_uid)
            except Chapter.DoesNotExist:
                messages.error(request, "Invalid Chapter selected.")
                return redirect("subject_dashboard", slug=subject_slug)

            topic_uid = str(uuid.uuid4()).replace("-", "")
            topic = Topic.objects.create(
                uid=topic_uid,
                title=title,
                slug=slugify(title),
                is_active=True,
                chapter_id=chapter.uid,
            )

            try:
                material_uid = str(uuid.uuid4()).replace("-", "")
                material = Material.objects.create(
                    uid=material_uid,
                    content="",
                    slug=slugify(material_uid),
                    status="Draft",
                    is_active=True,
                    topic_id=topic_uid,
                    pdf_file=None,
                )
                messages.success(request, f"Topic '{title}' added successfully!")
            except Exception as material_error:
                topic.delete()
                messages.error(
                    request, f"Error creating material: {str(material_error)}"
                )
                return redirect("subject_dashboard", slug=subject_slug)

            return redirect("subject_dashboard", slug=subject_slug)

        except Exception as e:
            messages.error(request, f"Error adding topic: {str(e)}")
            return redirect("subject_dashboard", slug=subject_slug)

    else:
        return redirect("dashboard")


def Sub_form(request):
    return render(request, "add_sub.html")


def add_course(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        try:
            name = request.POST.get("coursename")
            description = request.POST.get("description")
            logo = request.FILES.get("logo")

            if not name:
                messages.error(request, "Course name is required.")
                return redirect("dashboard")

            subject = Subject.objects.create(
                title=name,
                course_type_id="3079d562ecb24edabae5a6ac8c13b307",
                description=description,
                logo=logo,
                slug=slugify(name),
                is_active=True,
            )

            messages.success(request, f"Course '{name}' has been created successfully!")
            return redirect("dashboard")

        except Exception as e:
            messages.error(request, f"Error creating course: {str(e)}")
            return redirect("dashboard")

    else:
        return redirect("dashboard")


def update_logo(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        try:
            uid = request.POST.get("uid")
            logo = request.FILES.get("logo")

            subject = get_object_or_404(Subject, uid=uid)
            subject.logo = logo
            subject.save()

            messages.success(request, "Logo updated successfully.")
            return redirect("subject_dashboard", slug=subject.slug)
        except Exception as e:
            messages.error(request, f"Logo update failed: {str(e)}")
            return redirect("subject_dashboard", slug=subject.slug)
    else:
        return redirect("dashboard")


def update_seo(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        id = request.POST.get("id")
        slug = request.POST.get("slug")

        if not (slug and id):
            messages.warning("necessary credentials not provided")
            return redirect("dashboard")

        if request.POST.get("title"):
            try:
                title = request.POST.get("title")
                seo = get_object_or_404(SeoContent, id=id)
                seo.title = title
                seo.save()
                messages.success(request, "seo title updated successfully")
                return redirect("subject_dashboard", slug=slug)
            except Exception as e:
                messages.error(request, f"seo title update failed: {str(e)}")
                return redirect("subject_dashboard", slug=slug)

        elif request.POST.get("description"):

            try:
                description = request.POST.get("description")
                seo = get_object_or_404(SeoContent, id=id)
                seo.meta_description = description
                seo.save()
                messages.success(request, "seo description updated successfully")
                return redirect("subject_dashboard", slug=slug)
            except Exception as e:
                messages.error(request, f"meta description update failed: {str(e)}")
                return redirect("subject_dashboard", slug=slug)

        elif request.POST.get("keywords"):
            try:
                keywords = request.POST.get("keywords")
                seo = get_object_or_404(SeoContent, id=id)
                seo.keywords = keywords
                seo.save()
                messages.success(request, "seo keywords updated successfully")
                return redirect("subject_dashboard", slug=slug)
            except Exception as e:
                messages.error(request, f"keywords update failed: {str(e)}")
                return redirect("subject_dashboard", slug=slug)
    else:
        return redirect("dashboard")


def update_content(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        try:
            uid = request.POST.get("uid")
            subject = request.POST.get("subject")
            chapter = request.POST.get("chapter")
            topic = request.POST.get("topic")
            content = request.POST.get("content")
            material = get_object_or_404(Material, uid=uid)
            material.content = content
            material.save()
            messages.success(request, "content updated successfully")
            return redirect(
                "material_dashboard", subject=subject, chapter=chapter, topic=topic
            )
        except Exception as e:
            messages.error(request, "content update failed")
            return redirect(
                "material_dashboard", subject=subject, chapter=chapter, topic=topic
            )
    else:
        return redirect("dashboard")


def update_topic_title(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check

        try:
            uid = request.POST.get("uid")
            subject = request.POST.get("subject")
            chapter = request.POST.get("chapter")
            topictitle = request.POST.get("topictitle")
            topic = get_object_or_404(Topic, uid=uid)
            topic.title = topictitle
            topic.save()
            messages.success(request, "title updated successfully")
            return redirect(
                "material_dashboard", subject=subject, chapter=chapter, topic=topic.slug
            )
        except Exception as e:
            messages.error(request, "title update failed")
            return redirect(
                "material_dashboard", subject=subject, chapter=chapter, topic=topic.slug
            )
    else:
        return redirect("dashboard")


def delete(request):
    if request.method == "POST":
        check = check_session(request)
        if check:
            return check
        slug = request.POST.get("slug")

        if request.POST.get("course"):
            try:
                uid = request.POST.get("course")
                course = get_object_or_404(Subject, uid=uid)
                title = course.title
                course.delete()
                messages.success(request, f"{title} deleted sucessfully")
                return redirect("dashboard")
            except Exception as e:
                messages.error(request, f"{title} delete failed")
                return redirect("subject_dashboard", slug=slug)

        elif request.POST.get("chapter"):
            try:
                uid = request.POST.get("chapter")
                chapter = get_object_or_404(Chapter, uid=uid)
                title = chapter.title
                chapter.delete()
                messages.success(request, f"{title} delete succesfully")
                return redirect("subject_dashboard", slug=slug)
            except Exception as e:
                messages.error(request, f"{title} delete failed")
                return redirect("subject_dashboard", slug=slug)

        elif request.POST.get("topic"):
            try:
                uid = request.POST.get("topic")
                topic = get_object_or_404(Topic, uid=uid)
                title = topic.title
                topic.delete()
                messages.success(request, f"{title} deleted successfully")
                return redirect("subject_dashboard", slug=slug)
            except Exception as e:
                messages.error(request, f"{title} delete failed")
                return redirect("subject_dashboard", slug=slug)

    else:
        return redirect("dashboard")
