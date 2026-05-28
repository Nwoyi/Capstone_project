"""End-to-end smoke test against a running deployment.

Usage:
    python scripts/smoke_test.py https://capstone-project-do33.onrender.com \\
        --admin-email you@example.com --admin-password your-password

Exits 0 on success, non-zero on the first failed assertion.
"""

from __future__ import annotations

import argparse
import sys
import time
import uuid

import httpx


def check(label: str, condition: bool, detail: str = "") -> None:
    mark = "PASS" if condition else "FAIL"
    print(f"  [{mark}] {label}{(' — ' + detail) if detail else ''}")
    if not condition:
        sys.exit(1)


def run(base_url: str, admin_email: str, admin_password: str) -> None:
    base_url = base_url.rstrip("/")
    client = httpx.Client(base_url=base_url, timeout=60.0)
    suffix = uuid.uuid4().hex[:6]
    student_email = f"smoke+{suffix}@test.com"
    student_password = "smoke-password-123"
    course_code = f"SMOKE-{suffix.upper()}"

    print(f"Smoke test against {base_url}")

    print("\n[1] Health: /docs reachable")
    r = client.get("/docs")
    check("GET /docs returns 200", r.status_code == 200, str(r.status_code))

    print("\n[2] Admin login")
    r = client.post(
        "/auth/login",
        data={"username": admin_email, "password": admin_password},
    )
    check("admin login 200", r.status_code == 200, r.text[:120])
    admin_token = r.json()["access_token"]
    admin_h = {"Authorization": f"Bearer {admin_token}"}

    print("\n[3] Register a fresh student")
    r = client.post(
        "/auth/register",
        json={"name": "Smoke Student", "email": student_email, "password": student_password},
    )
    check("register student 201", r.status_code == 201, r.text[:120])
    check("role is student (admin role not grantable)", r.json()["role"] == "student")

    print("\n[4] Student login")
    r = client.post(
        "/auth/login",
        data={"username": student_email, "password": student_password},
    )
    check("student login 200", r.status_code == 200)
    student_token = r.json()["access_token"]
    student_h = {"Authorization": f"Bearer {student_token}"}

    print("\n[5] Admin creates a course")
    r = client.post(
        "/courses",
        json={"title": "Smoke Course", "code": course_code, "capacity": 2},
        headers=admin_h,
    )
    check("create course 201", r.status_code == 201, r.text[:120])
    course_id = r.json()["id"]

    print("\n[6] Public list shows the course")
    r = client.get("/courses")
    check("list courses 200", r.status_code == 200)
    check(
        "new course appears in listing",
        any(c["id"] == course_id for c in r.json()),
    )

    print("\n[7] Student enrolls")
    r = client.post("/enrollments", json={"course_id": course_id}, headers=student_h)
    check("enroll 201", r.status_code == 201, r.text[:120])
    enrollment_id = r.json()["id"]

    print("\n[8] Double-enroll blocked")
    r = client.post("/enrollments", json={"course_id": course_id}, headers=student_h)
    check("double-enroll rejected (400)", r.status_code == 400)

    print("\n[9] Admin cannot enroll")
    r = client.post("/enrollments", json={"course_id": course_id}, headers=admin_h)
    check("admin enroll rejected (403)", r.status_code == 403)

    print("\n[10] Student lists own enrollments")
    r = client.get("/enrollments/me", headers=student_h)
    check("list mine 200", r.status_code == 200)
    check("contains the new enrollment", any(e["id"] == enrollment_id for e in r.json()))

    print("\n[11] Delete-with-enrollments is blocked")
    r = client.delete(f"/courses/{course_id}", headers=admin_h)
    check("delete blocked while enrolled (400)", r.status_code == 400)

    print("\n[12] Student deregisters")
    r = client.delete(f"/enrollments/{enrollment_id}", headers=student_h)
    check("deregister 204", r.status_code == 204)

    print("\n[13] Admin deletes the now-empty course")
    r = client.delete(f"/courses/{course_id}", headers=admin_h)
    check("delete course 204", r.status_code == 204)

    print("\nAll checks passed.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="e.g. https://capstone-project-do33.onrender.com")
    parser.add_argument("--admin-email", required=True)
    parser.add_argument("--admin-password", required=True)
    args = parser.parse_args()

    start = time.time()
    run(args.base_url, args.admin_email, args.admin_password)
    print(f"\nElapsed: {time.time() - start:.1f}s")


if __name__ == "__main__":
    main()
