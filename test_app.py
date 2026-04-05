import unittest
from contextlib import contextmanager

from flask import template_rendered

from app import app, load_data


@contextmanager
def captured_templates(flask_app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, flask_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, flask_app)


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_renders_home_template(self):
        with captured_templates(app) as templates:
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0][0].name, "index.html")

    def test_dashboard_get_uses_all_students_by_default(self):
        expected_total = len(load_data())

        with captured_templates(app) as templates:
            response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0][0].name, "dashboard.html")
        self.assertEqual(templates[0][1]["gender_filter"], "All")
        self.assertEqual(templates[0][1]["stats"]["total_students"], expected_total)

    def test_dashboard_post_filters_stats_by_gender(self):
        df = load_data()
        expected_total = len(df[df["gender"] == "female"])

        with captured_templates(app) as templates:
            response = self.client.post("/dashboard", data={"gender": "female"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0][1]["gender_filter"], "female")
        self.assertEqual(templates[0][1]["stats"]["total_students"], expected_total)


if __name__ == "__main__":
    unittest.main()
