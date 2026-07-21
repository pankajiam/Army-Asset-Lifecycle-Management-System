from app.db.database import SessionLocal
from app.models.role import Role
from app.models.rank import Rank
from app.models.unit import Unit

db = SessionLocal()

try:
    # -------------------- Roles --------------------
    if db.query(Role).count() == 0:
        roles = [
            Role(role_name="Administrator", description="System Administrator"),
            Role(role_name="Commanding Officer", description="Unit Commander"),
            Role(role_name="Quarter Master", description="Inventory Manager"),
            Role(role_name="Store Keeper", description="Store Incharge"),
            Role(role_name="Unit Officer", description="Unit Officer"),
        ]

        db.add_all(roles)
        print("Roles inserted.")

    # -------------------- Ranks --------------------
    if db.query(Rank).count() == 0:
        ranks = [
            Rank(rank_name="Colonel", level=1, can_approve=True),
            Rank(rank_name="Lieutenant Colonel", level=2, can_approve=True),
            Rank(rank_name="Major", level=3, can_approve=True),
            Rank(rank_name="Captain", level=4, can_approve=False),
            Rank(rank_name="Lieutenant", level=5, can_approve=False),
        ]

        db.add_all(ranks)
        print("Ranks inserted.")

    # -------------------- Units --------------------
    if db.query(Unit).count() == 0:
        units = [
            Unit(unit_name="Army Headquarters", location="New Delhi"),
            Unit(unit_name="Northern Command", location="Udhampur"),
            Unit(unit_name="Western Command", location="Chandimandir"),
            Unit(unit_name="Eastern Command", location="Kolkata"),
            Unit(unit_name="Southern Command", location="Pune"),
        ]

        db.add_all(units)
        print("Units inserted.")

    db.commit()
    print("\nDatabase seeded successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()