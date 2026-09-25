import pytest
from django.urls import reverse

from apps.articles.models import Article, Revision

pytestmark = pytest.mark.django_db


def test_list_articles_is_public(api_client, article):
    response = api_client.get(reverse("article-list"))
    assert response.status_code == 200
    assert response.data["count"] == 1


def test_create_article_requires_auth(api_client):
    response = api_client.post(reverse("article-list"), {"title": "X", "content": "y"})
    assert response.status_code == 401


def test_create_article_records_revision(auth_client, category):
    payload = {
        "title": "Brand New",
        "summary": "A summary",
        "content": "# Body",
        "category": category.slug,
        "comment": "first draft",
    }
    response = auth_client.post(reverse("article-list"), payload)
    assert response.status_code == 201
    article = Article.objects.get(slug=response.data["slug"])
    assert article.author is not None
    assert article.revisions.count() == 1
    assert article.revisions.first().comment == "first draft"


def test_retrieve_increments_view_count(api_client, article):
    url = reverse("article-detail", kwargs={"slug": article.slug})
    api_client.get(url)
    article.refresh_from_db()
    assert article.view_count == 1


def test_edit_creates_new_revision(auth_client, article):
    url = reverse("article-detail", kwargs={"slug": article.slug})
    response = auth_client.patch(url, {"content": "# Updated", "comment": "fix typo"})
    assert response.status_code == 200
    assert Revision.objects.filter(article=article).count() == 1
    article.refresh_from_db()
    assert "Updated" in article.content


def test_non_author_cannot_delete(api_client, article, other_user):
    api_client.force_authenticate(user=other_user)
    url = reverse("article-detail", kwargs={"slug": article.slug})
    assert api_client.delete(url).status_code == 403


def test_author_can_delete(auth_client, article):
    url = reverse("article-detail", kwargs={"slug": article.slug})
    assert auth_client.delete(url).status_code == 204


def test_search_finds_article(api_client, article):
    response = api_client.get(reverse("article-list"), {"search": "django"})
    assert response.status_code == 200
    assert response.data["count"] >= 1


def test_filter_by_category(api_client, article, category):
    response = api_client.get(reverse("article-list"), {"category": category.slug})
    assert response.data["count"] == 1


def test_revisions_endpoint(auth_client, article):
    auth_client.patch(
        reverse("article-detail", kwargs={"slug": article.slug}),
        {"content": "# v2", "comment": "edit"},
    )
    url = reverse("article-revisions", kwargs={"slug": article.slug})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data["count"] == 1


def test_stats_endpoint(api_client, article):
    response = api_client.get(reverse("article-stats"))
    assert response.status_code == 200
    assert response.data["articles"] == 1


def test_categories_endpoint(api_client, category):
    response = api_client.get(reverse("category-list"))
    assert response.status_code == 200
    assert any(c["slug"] == "programming" for c in response.data)


def test_health_endpoint(api_client):
    response = api_client.get(reverse("health"))
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
