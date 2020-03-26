import unittest
from src.masonite.orm.grammar.mssql_grammar import MSSQLGrammar
from app.User import User
from src.masonite.orm.models import Model
import os

if os.getenv("RUN_MYSQL_DATABASE", False) == "True":

    class ProfileFillable(Model):
        __fillable__ = ["name"]
        __table__ = "profiles"

    class ProfileFillAsterisk(Model):
        __fillable__ = ["*"]
        __table__ = "profiles"

    class Profile(Model):
        pass

    class Company(Model):
        pass

    class ProductNames(Model):
        pass

    class TestModel(unittest.TestCase):
        def test_can_use_fillable(self):
            sql = ProfileFillable.create({"name": "Joe", "email": "user@example.com"})

            self.assertEqual(sql, "INSERT INTO `profiles` (`name`) VALUES ('Joe')")

        def test_can_use_fillable_asterisk(self):
            sql = ProfileFillAsterisk.create(
                {"name": "Joe", "email": "user@example.com"}
            )

            self.assertEqual(
                sql,
                "INSERT INTO `profiles` (`name`, `email`) VALUES ('Joe', 'user@example.com')",
            )

        def test_can_touch(self):
            profile = ProfileFillAsterisk.hydrate({"name": "Joe", "id": 1})

            sql = profile.touch("now", query=True)

            self.assertEqual(
                sql, "UPDATE `profiles` SET `updated_at` = 'now' WHERE `id` = '1'"
            )

        def test_table_name(self):
            table_name = Profile.get_table_name()
            self.assertEqual(table_name, "profiles")

            table_name = Company.get_table_name()
            self.assertEqual(table_name, "companies")

            table_name = ProductNames.get_table_name()
            self.assertEqual(table_name, "product_names")

        def test_serialize(self):
            profile = ProfileFillAsterisk.hydrate({"name": "Joe", "id": 1})

            self.assertEqual(profile.serialize(), {"name": "Joe", "id": 1})

        def test_serialize_with_dirty_attribute(self):
            profile = ProfileFillAsterisk.hydrate({"name": "Joe", "id": 1})

            profile.age = 18
            self.assertEqual(profile.serialize(), {"age": 18, "name": "Joe", "id": 1,})

        # def test_can_call(self):
        #     print(User.find(1))
        #     print(User.find(2))
        #     print(User.find(3))
        #     print(User.find(4))
        #     print(User.find(5))
        #     print(User.find(6))
        #     print(User.find(7))
