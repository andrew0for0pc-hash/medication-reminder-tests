import unittest
from datetime import datetime, timezone
from reminder import create_reminder


class ReminderTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 29, 10, tzinfo=timezone.utc)
        self.future = '2026-10-29T11:00:00+00:00'

    def test_valid(self):
        result = create_reminder('Medicine A', self.future, self.now)
        self.assertEqual(result['medicine'], 'Medicine A')
        self.assertEqual(result['status'], 'planned')
        self.assertEqual(result['scheduled_at'], self.future)

    def test_trim(self):
        self.assertEqual(create_reminder(' A ', self.future, self.now)['medicine'], 'A')

    def test_blank_name(self):
        with self.assertRaises(ValueError):
            create_reminder(' ', self.future, self.now)

    def test_wrong_name_type(self):
        with self.assertRaises(ValueError):
            create_reminder(None, self.future, self.now)

    def test_past(self):
        with self.assertRaises(ValueError):
            create_reminder('A', '2026-10-29T09:59:00+00:00', self.now)

    def test_equal_now(self):
        with self.assertRaises(ValueError):
            create_reminder('A', self.now.isoformat(), self.now)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            create_reminder('A', '2026-02-30T11:00:00+00:00', self.now)

    def test_missing_timezone(self):
        with self.assertRaises(ValueError):
            create_reminder('A', '2026-10-29T11:00:00', self.now)

    def test_same_instant_with_offset(self):
        with self.assertRaises(ValueError):
            create_reminder('A', '2026-10-29T12:00:00+02:00', self.now)

    def test_wrong_date_type(self):
        with self.assertRaises(ValueError):
            create_reminder('A', None, self.now)

    def test_naive_now(self):
        with self.assertRaises(ValueError):
            create_reminder('A', self.future, datetime(2026, 10, 29, 10))


if __name__ == '__main__':
    unittest.main()
