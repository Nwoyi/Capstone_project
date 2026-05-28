def test_list_courses_public(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == []


def test_create_course_requires_admin(client, student_token):
    response = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403


def test_create_course_as_admin(client, admin_token):
    response = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "PY101"
    assert data["is_active"] is True


def test_duplicate_course_code_fails(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"title": "Python", "code": "PY101", "capacity": 30}
    client.post("/courses", json=payload, headers=headers)
    response = client.post("/courses", json=payload, headers=headers)
    assert response.status_code == 400


def test_invalid_capacity_rejected(client, admin_token):
    response = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 0},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


def test_update_course_partial(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers=headers,
    )
    course_id = create.json()["id"]

    response = client.put(
        f"/courses/{course_id}",
        json={"title": "Advanced Python"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Advanced Python"
    assert data["code"] == "PY101"
    assert data["capacity"] == 30


def test_deactivate_hides_from_public_list(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers=headers,
    )
    course_id = create.json()["id"]
    client.patch(f"/courses/{course_id}/deactivate", headers=headers)

    response = client.get("/courses")
    assert response.json() == []


def test_get_course_by_id(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers=headers,
    )
    course_id = create.json()["id"]

    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["code"] == "PY101"


def test_get_course_by_id_not_found(client):
    response = client.get("/courses/9999")
    assert response.status_code == 404


def test_delete_course_as_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers=headers,
    )
    course_id = create.json()["id"]

    response = client.delete(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 204

    assert client.get(f"/courses/{course_id}").status_code == 404


def test_delete_course_requires_admin(client, admin_token, student_token):
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    course_id = create.json()["id"]

    response = client.delete(
        f"/courses/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403


def test_delete_course_with_enrollments_blocked(client, admin_token, student_token):
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    course_id = create.json()["id"]
    client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )

    response = client.delete(
        f"/courses/{course_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 400


def test_activate_makes_visible_again(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create = client.post(
        "/courses",
        json={"title": "Python", "code": "PY101", "capacity": 30},
        headers=headers,
    )
    course_id = create.json()["id"]
    client.patch(f"/courses/{course_id}/deactivate", headers=headers)
    client.patch(f"/courses/{course_id}/activate", headers=headers)

    response = client.get("/courses")
    assert len(response.json()) == 1
