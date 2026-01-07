# crud operations for mongodb using pymongo

import os
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


def get_collection() -> Collection:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGO_DB", "cat_db")
    collection_name = os.getenv("MONGO_COLLECTION", "cats")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)

    # quick connectivity check
    client.admin.command("ping")

    db = client[db_name]
    col = db[collection_name]

    # ensure unique names to avoid duplicates
    col.create_index("name", unique=True)

    return col


def print_cat(doc: Dict[str, Any]) -> None:
    _id = str(doc.get("_id", ""))
    name = doc.get("name", "")
    age = doc.get("age", "")
    features = doc.get("features", [])
    if features is None:
        features = []

    print(f"_id: {_id}")
    print(f"name: {name}")
    print(f"age: {age}")
    print(f"features: {features}")
    print("-" * 30)


def create_cat(col: Collection, name: str, age: int, features: List[str]) -> None:
    doc = {"name": name, "age": age, "features": features}
    try:
        res = col.insert_one(doc)
        print(f"created: {res.inserted_id}")
    except PyMongoError as e:
        print(f"db error: {e}")


def list_all(col: Collection) -> None:
    try:
        docs = list(col.find({}))
        if not docs:
            print("no records")
            return
        for doc in docs:
            print_cat(doc)
    except PyMongoError as e:
        print(f"db error: {e}")


def find_by_name(col: Collection, name: str) -> Optional[Dict[str, Any]]:
    try:
        doc = col.find_one({"name": name})
        if not doc:
            print("not found")
            return None
        print_cat(doc)
        return doc
    except PyMongoError as e:
        print(f"db error: {e}")
        return None


def update_age_by_name(col: Collection, name: str, new_age: int) -> None:
    try:
        res = col.update_one({"name": name}, {"$set": {"age": new_age}})
        if res.matched_count == 0:
            print("not found")
            return
        print("age updated")
    except PyMongoError as e:
        print(f"db error: {e}")


def add_feature_by_name(col: Collection, name: str, feature: str) -> None:
    try:
        # addToSet prevents duplicates inside features
        res = col.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if res.matched_count == 0:
            print("not found")
            return
        print("feature added")
    except PyMongoError as e:
        print(f"db error: {e}")


def delete_by_name(col: Collection, name: str) -> None:
    try:
        res = col.delete_one({"name": name})
        if res.deleted_count == 0:
            print("not found")
            return
        print("deleted")
    except PyMongoError as e:
        print(f"db error: {e}")


def delete_all(col: Collection) -> None:
    try:
        res = col.delete_many({})
        print(f"deleted records: {res.deleted_count}")
    except PyMongoError as e:
        print(f"db error: {e}")


def read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("enter integer")


def read_features(prompt: str) -> List[str]:
    raw = input(prompt).strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",")]
    return [p for p in parts if p]


def menu() -> None:
    print("1) list all cats")
    print("2) find cat by name")
    print("3) create cat")
    print("4) update age by name")
    print("5) add feature by name")
    print("6) delete cat by name")
    print("7) delete all cats")
    print("0) exit")


def main() -> None:
    try:
        col = get_collection()
    except ServerSelectionTimeoutError:
        print("cannot connect to mongodb")
        print("check that mongodb is running and MONGO_URI is correct")
        return
    except PyMongoError as e:
        print(f"db error: {e}")
        return

    while True:
        menu()
        choice = input("choose: ").strip()

        if choice == "1":
            list_all(col)

        elif choice == "2":
            name = input("name: ").strip()
            if name:
                find_by_name(col, name)

        elif choice == "3":
            name = input("name: ").strip()
            age = read_int("age: ")
            features = read_features("features (comma separated): ")
            if name:
                create_cat(col, name, age, features)

        elif choice == "4":
            name = input("name: ").strip()
            new_age = read_int("new age: ")
            if name:
                update_age_by_name(col, name, new_age)

        elif choice == "5":
            name = input("name: ").strip()
            feature = input("feature: ").strip()
            if name and feature:
                add_feature_by_name(col, name, feature)

        elif choice == "6":
            name = input("name: ").strip()
            if name:
                delete_by_name(col, name)

        elif choice == "7":
            confirm = in
