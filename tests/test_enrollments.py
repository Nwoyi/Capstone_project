def _create_course(client, admin_token, code="PY101", capacity=30):
    response = client.post(
        "/courses",
        json={"title": "Python", "code": code, "capacity": capacity},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    return response.json()["id"]


def test_student_can_enroll(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    response = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 201
    assert response.json()["course_id"] == course_id


def test_admin_cannot_enroll(client, admin_token):
    course_id = _create_course(client, admin_token)
    response = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


def test_double_enrollment_blocked(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    headers = {"Authorization": f"Bearer {student_token}"}
    client.post("/enrollments", json={"course_id": course_id}, headers=headers)
    response = client.post(
        "/enrollments", json={"course_id": course_id}, headers=headers
    )
    assert response.status_code == 400


def test_enroll_in_inactive_course_blocked(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    client.patch(
        f"/courses/{course_id}/deactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 400


def test_capacity_enforced(client, admin_token, student_token):
    course_id = _create_course(client, admin_token, capacity=1)
    client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )

    client.post(
        "/auth/register",
        json={
            "name": "Student2",
            "email": "student2@test.com",
            "password": "password123",
            "role": "student",
        },
    )
    login = client.post(
        "/auth/login",
        data={"username": "student2@test.com", "password": "password123"},
    )
    token2 = login.json()["access_token"]

    response = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 400


def test_list_my_enrollments(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    headers = {"Authorization": f"Bearer {student_token}"}
    client.post("/enrollments", json={"course_id": course_id}, headers=headers)

    response = client.get("/enrollments/me", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_student_can_deregister_own(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    headers = {"Authorization": f"Bearer {student_token}"}
    create = client.post(
        "/enrollments", json={"course_id": course_id}, headers=headers
    )
    enrollment_id = create.json()["id"]

    response = client.delete(f"/enrollments/{enrollment_id}", headers=headers)
    assert response.status_code == 204


def test_admin_can_list_all_enrollments(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )

    response = client.get(
        "/enrollments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_admin_can_list_enrollments_by_course(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )

    response = client.get(
        f"/enrollments/by-course/{course_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["course_id"] == course_id


def test_admin_can_remove_any_enrollment(client, admin_token, student_token):
    course_id = _create_course(client, admin_token)
    create = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    enrollment_id = create.json()["id"]

    response = client.delete(
        f"/enrollments/admin/{enrollment_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204
