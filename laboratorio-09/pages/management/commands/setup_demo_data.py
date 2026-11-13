from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from pages.models import Category, Resource


class Command(BaseCommand):
    help = "Initializes demo data, groups (Catalog reviewers and Catalog editors), and test users for Laboratorio 9."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Setting up demo data for Laboratorio 9..."))

        content_type = ContentType.objects.get_for_model(Resource)

        # 1. Setup Groups & Permissions
        # Catalog reviewers
        view_perm = Permission.objects.get(
            content_type=content_type,
            codename="view_resource",
        )
        reviewers_group, _ = Group.objects.get_or_create(name="Catalog reviewers")
        reviewers_group.permissions.set([view_perm])

        # Catalog editors (CRUD permissions)
        crud_perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "view_resource",
                "add_resource",
                "change_resource",
                "delete_resource",
            ],
        )
        editors_group, _ = Group.objects.get_or_create(name="Catalog editors")
        editors_group.permissions.set(crud_perms)

        self.stdout.write(self.style.SUCCESS("[OK] Groups configured:"))
        self.stdout.write("  - 'Catalog reviewers' (view_resource)")
        self.stdout.write("  - 'Catalog editors' (view, add, change, delete)")

        # 2. Setup Users
        User = get_user_model()

        # Admin user
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@classroomhub.local", "is_staff": True, "is_superuser": True},
        )
        admin_user.set_password("AdminPassword123!")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        # Editor demo user
        editor_user, _ = User.objects.get_or_create(
            username="editor_demo",
            defaults={"email": "editor@classroomhub.local"},
        )
        editor_user.set_password("EditorPassword123!")
        editor_user.is_staff = False
        editor_user.is_superuser = False
        editor_user.groups.set([editors_group])
        editor_user.save()

        # Reviewer demo user
        reviewer_user, _ = User.objects.get_or_create(
            username="reviewer_demo",
            defaults={"email": "reviewer@classroomhub.local"},
        )
        reviewer_user.set_password("ReviewerPassword123!")
        reviewer_user.is_staff = False
        reviewer_user.is_superuser = False
        reviewer_user.groups.set([reviewers_group])
        reviewer_user.save()

        # Reader demo user
        reader_user, _ = User.objects.get_or_create(
            username="reader_demo",
            defaults={"email": "reader@classroomhub.local"},
        )
        reader_user.set_password("ReaderPassword123!")
        reader_user.is_staff = False
        reader_user.is_superuser = False
        reader_user.groups.clear()
        reader_user.save()

        self.stdout.write(self.style.SUCCESS("[OK] Demo users created / updated:"))
        self.stdout.write("  - admin / AdminPassword123! (Superuser)")
        self.stdout.write("  - editor_demo / EditorPassword123! (Member of 'Catalog editors' - Full CRUD)")
        self.stdout.write("  - reviewer_demo / ReviewerPassword123! (Member of 'Catalog reviewers')")
        self.stdout.write("  - reader_demo / ReaderPassword123! (Standard user)")

        # 3. Setup Categories
        cat_prog, _ = Category.objects.get_or_create(
            name="Programming",
            defaults={"description": "Core programming topics and algorithms"},
        )
        cat_db, _ = Category.objects.get_or_create(
            name="Databases",
            defaults={"description": "Relational and NoSQL database management"},
        )
        cat_web, _ = Category.objects.get_or_create(
            name="Web Development",
            defaults={"description": "Full-stack web frameworks and frontend tools"},
        )

        # 4. Setup Resources
        resources_data = [
            {
                "title": "Python basics",
                "description": "Variables, functions, data structures and standard library essentials.",
                "category": cat_prog,
                "available": True,
                "resource_type": "Tutorial",
            },
            {
                "title": "Django models",
                "description": "Database fundamentals, migrations, and ORM query optimization.",
                "category": cat_web,
                "available": True,
                "resource_type": "Documentation",
            },
            {
                "title": "Relational Database Design with MariaDB",
                "description": "Entity-relationship modeling, normal forms, and SQL constraints.",
                "category": cat_db,
                "available": False,
                "resource_type": "Guide",
            },
            {
                "title": "Django Generic Class-Based Views & ModelForms",
                "description": "Building protected CRUD workflows with CreateView, UpdateView and DeleteView.",
                "category": cat_web,
                "available": True,
                "resource_type": "Workshop",
            },
        ]

        for item in resources_data:
            res, _ = Resource.objects.update_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "category": item["category"],
                    "available": item["available"],
                    "resource_type": item["resource_type"],
                },
            )

        self.stdout.write(self.style.SUCCESS("[OK] Sample categories and resources created successfully."))
        self.stdout.write(self.style.SUCCESS("Demo setup complete! You can now test CRUD operations."))
