"""Контракт API, на который опирается фронтенд: каждый ресурс — список, чтение, создание,
изменение (включая очистку поля через null) и удаление."""
import pytest

# (имя, URL коллекции человека, URL записи, тело создания, поле для изменения)
# Аккаунты, недвижимость, транспорт и устройства удаляются мягко (is_active = False): запись пропадает
# из списка, но остаётся в базе и читается по id — это задуманное поведение (история).
SOFT_DELETED = {"digital-accounts", "real-estate", "vehicles", "devices"}
PERSON_RESOURCES = [
    ("digital-accounts", "/api/persons/{pid}/digital-accounts", "/api/digital-accounts",
     {"platform_type": "game", "platform_name": "Genshin"}, "notes"),
    ("real-estate", "/api/persons/{pid}/real-estate", "/api/real-estate",
     {"property_type": "apartment", "address": "ул. Тестовая, 1"}, "notes"),
    ("vehicles", "/api/persons/{pid}/vehicles", "/api/vehicles",
     {"vehicle_type": "car", "brand": "Lada", "model": "Vesta"}, "notes"),
    ("cases", "/api/persons/{pid}/cases", "/api/cases",
     {"case_type": "task", "title": "Позвонить"}, "description"),
    ("medical", "/api/persons/{pid}/medical", "/api/medical",
     {"record_type": "visit", "title": "Осмотр"}, "description"),
    ("devices", "/api/persons/{pid}/devices", "/api/devices",
     {"device_type": "phone", "brand": "Apple", "model": "iPhone"}, "notes"),
]


@pytest.mark.parametrize("name,collection,item,body,field", PERSON_RESOURCES, ids=[r[0] for r in PERSON_RESOURCES])
def test_person_resource_full_crud(client, person, name, collection, item, body, field):
    pid = person["id"]
    payload = {**body, "person_id": pid}

    created = client.post(collection.format(pid=pid), json=payload)
    assert created.status_code == 201, created.text
    rid = created.json()["id"]

    listed = client.get(collection.format(pid=pid))
    assert listed.status_code == 200
    assert [r["id"] for r in listed.json()] == [rid]

    assert client.get(f"{item}/{rid}").json()["id"] == rid

    updated = client.put(f"{item}/{rid}", json={field: "обновлено"})
    assert updated.status_code == 200, updated.text
    assert updated.json()[field] == "обновлено"

    cleared = client.put(f"{item}/{rid}", json={field: None})
    assert cleared.json()[field] is None, "очистка поля через null должна сохраняться"

    assert client.delete(f"{item}/{rid}").status_code in (200, 204)
    assert client.get(collection.format(pid=pid)).json() == []
    if name not in SOFT_DELETED:
        assert client.get(f"{item}/{rid}").status_code == 404


@pytest.mark.parametrize("name,collection,item,body,field", PERSON_RESOURCES, ids=[r[0] for r in PERSON_RESOURCES])
def test_person_resource_404s(client, name, collection, item, body, field):
    assert client.get(collection.format(pid=999999)).status_code == 404
    assert client.get(f"{item}/999999").status_code == 404
    assert client.put(f"{item}/999999", json={field: "x"}).status_code == 404
    assert client.delete(f"{item}/999999").status_code == 404


class TestPersons:
    def test_crud(self, client, person):
        pid = person["id"]
        assert client.get(f"/api/persons/{pid}").json()["full_name"] == "Иван Тестов"

        updated = client.put(f"/api/persons/{pid}", json={"phone": "+7 900 000-00-00"})
        assert updated.json()["phone"] == "+7 900 000-00-00"
        assert client.put(f"/api/persons/{pid}", json={"phone": None}).json()["phone"] is None

        assert client.delete(f"/api/persons/{pid}").status_code == 200
        assert client.get(f"/api/persons/{pid}").status_code == 404

    def test_duplicate_short_name_is_rejected(self, client, person):
        r = client.post("/api/persons", json={"full_name": "Другой", "short_name": "ivan"})
        assert r.status_code == 400

    def test_list_has_no_secrets_or_nested_collections(self, client, person):
        client.post(f"/api/persons/{person['id']}/digital-accounts",
                    json={"platform_type": "game", "platform_name": "X", "password": "секрет"})

        item = client.get("/api/persons").json()[0]

        assert "секрет" not in str(item)
        assert "digital_accounts" not in item

    def test_list_is_not_capped_at_100(self, client):
        for i in range(105):
            client.post("/api/persons", json={"full_name": f"Человек {i}", "short_name": f"p{i}"})

        assert len(client.get("/api/persons").json()) == 105


class TestRelations:
    def test_create_list_delete(self, client, person, other_person):
        r = client.post("/api/relations", json={
            "parent_id": person["id"], "child_id": other_person["id"], "relation_type": "friend"})
        assert r.status_code == 201, r.text
        rid = r.json()["id"]

        assert [x["id"] for x in client.get("/api/relations").json()] == [rid]
        assert client.get(f"/api/persons/{person['id']}/relations").json()[0]["person_id"] == other_person["id"]

        assert client.delete(f"/api/relations/{rid}").status_code == 200
        assert client.get("/api/relations").json() == []

    def test_relation_with_self_is_rejected(self, client, person):
        r = client.post("/api/relations", json={
            "parent_id": person["id"], "child_id": person["id"], "relation_type": "self"})
        assert r.status_code == 400


class TestSocial:
    def test_list_create_delete(self, client, person):
        pid = person["id"]
        created = client.post(f"/api/persons/{pid}/social", json={"platform": "telegram", "link": "t.me/ivan"})
        assert created.status_code == 201, created.text
        sid = created.json()["id"]

        listed = client.get(f"/api/persons/{pid}/social")
        assert listed.status_code == 200, "фронтенд загружает соцсети этим запросом"
        assert [s["id"] for s in listed.json()] == [sid]

        assert client.delete(f"/api/social/{sid}").status_code == 200
        assert client.get(f"/api/persons/{pid}/social").json() == []

    def test_social_for_missing_person_is_404(self, client):
        assert client.post("/api/persons/999999/social", json={"platform": "x", "link": "y"}).status_code == 404


class TestPartners:
    def test_crud(self, client, person, other_person):
        pid = person["id"]
        created = client.post(f"/api/persons/{pid}/partners",
                              json={"person_id": pid, "partner_id": other_person["id"]})
        assert created.status_code == 201, created.text
        rid = created.json()["id"]

        assert [p["id"] for p in client.get(f"/api/persons/{pid}/partners").json()] == [rid]
        assert client.put(f"/api/partners/{rid}", json={"relationship_notes": "заметка"}).json()["relationship_notes"] == "заметка"
        assert client.delete(f"/api/partners/{rid}").status_code == 200
        assert client.get(f"/api/partners/{rid}").status_code == 404


class TestCategoriesAndCrossRecords:
    def test_category_crud_and_tree(self, client):
        created = client.post("/api/categories", json={"name": "Подарки", "slug": "gifts"})
        assert created.status_code == 201, created.text
        cid = created.json()["id"]

        assert client.get(f"/api/categories/{cid}").json()["slug"] == "gifts"
        tree = client.get("/api/categories/tree")
        assert tree.status_code == 200, "маршрут /tree не должен перехватываться /{category_id}"
        assert [c["id"] for c in tree.json()] == [cid]

        assert client.put(f"/api/categories/{cid}", json={"name": "Подарки 2"}).json()["name"] == "Подарки 2"
        assert client.delete(f"/api/categories/{cid}").status_code in (200, 204)
        assert client.get(f"/api/categories/{cid}").status_code == 404

    def test_duplicate_slug_is_a_conflict(self, client):
        client.post("/api/categories", json={"name": "A", "slug": "same"})
        assert client.post("/api/categories", json={"name": "B", "slug": "same"}).status_code == 409

    def test_cross_record_crud(self, client, person):
        cid = client.post("/api/categories", json={"name": "Даты", "slug": "dates"}).json()["id"]
        created = client.post("/api/cross-records", json={
            "title": "День рождения", "record_type": "date", "primary_category_id": cid, "person_id": person["id"]})
        assert created.status_code == 201, created.text
        rid = created.json()["id"]

        assert [r["id"] for r in client.get(f"/api/persons/{person['id']}/cross-records").json()] == [rid]
        assert client.put(f"/api/cross-records/{rid}", json={"title": "ДР"}).json()["title"] == "ДР"
        assert client.delete(f"/api/cross-records/{rid}").status_code == 200
        assert client.get(f"/api/cross-records/{rid}").status_code == 404

    def test_category_in_use_cannot_be_deleted(self, client, person):
        cid = client.post("/api/categories", json={"name": "Работа", "slug": "work"}).json()["id"]
        client.post("/api/cross-records", json={
            "title": "Офис", "record_type": "work", "primary_category_id": cid, "person_id": person["id"]})

        assert client.delete(f"/api/categories/{cid}").status_code == 400


def test_each_route_is_registered_once():
    import main
    seen = {}
    for route in main.app.routes:
        for method in getattr(route, "methods", None) or []:
            key = (method, route.path)
            seen[key] = seen.get(key, 0) + 1
    duplicates = {k: v for k, v in seen.items() if v > 1}
    assert duplicates == {}
