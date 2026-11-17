from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app
from models import Friendship, ShotSession, User
from routers import leaderboard as leaderboard_router
from services.security import create_access_token

if not any(getattr(r, "path", "").startswith("/leaderboard") for r in app.routes):
    app.include_router(leaderboard_router.router, prefix="/leaderboard", tags=["leaderboard"])

def make_user(db, name: str, username: str) -> User:
    u = User(
        email=f"{username}@example.com",
        username=username,
        password_hash="fake_hash",
        name=name,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def make_friendship(db, u1: User, u2: User, status: str = "accepted") -> Friendship:
    f = Friendship(requester_id=u1.id, addressee_id=u2.id, status=status)
    db.add(f)
    db.commit()
    return f

def add_shots(
    db,
    user: User,
    made_count: int,
    missed_count: int,
    created_at: datetime | None = None,
    score: float | None = 85.0,
):
    ts = created_at or datetime.utcnow()
    for _ in range(made_count):
        db.add(
            ShotSession(
                user_id=user.id,
                video_url="https://example.com",
                made=True,
                overall_score=score,
                created_at=ts,
                status="done",
            )
        )
    for _ in range(missed_count):
        db.add(
            ShotSession(
                user_id=user.id,
                video_url="https://example.com",
                made=False,
                overall_score=score,
                created_at=ts,
                status="done",
            )
        )
    db.commit()

def auth_headers(user: User) -> dict:
    return {"Authorization": f"Bearer {create_access_token(str(user.id))}"}

def test_ranking_order(client: TestClient, db_session):
    me = make_user(db_session, "Me", "me_user")
    friend = make_user(db_session, "Friend High", "friend_high")
    make_friendship(db_session, me, friend, "accepted")

    # Me: 3/5 = 60%, Friend: 4/5 = 80%
    add_shots(db_session, me, made_count=3, missed_count=2)
    add_shots(db_session, friend, made_count=4, missed_count=1)

    res = client.get("/leaderboard", headers=auth_headers(me))
    assert res.status_code == 200
    data = res.json()

    assert [row["name"] for row in data] == ["Friend High", "Me"]
    assert data[0]["rank"] == 1
    assert data[0]["make_pct"] == 80
    assert data[0]["is_me"] is False
    assert data[1]["rank"] == 2
    assert data[1]["make_pct"] == 60
    assert data[1]["is_me"] is True

def test_five_shot_minimum(client: TestClient, db_session):
    me = make_user(db_session, "Me Ranked", "me_ranked")
    rookie = make_user(db_session, "Rookie Friend", "rookie_friend")
    make_friendship(db_session, me, rookie, "accepted")

    # Me: 3/5 = 60% (ranked), Rookie: 4/4 = 100% (unranked because < 5 shots)
    add_shots(db_session, me, made_count=3, missed_count=2)
    add_shots(db_session, rookie, made_count=4, missed_count=0)

    res = client.get("/leaderboard", headers=auth_headers(me))
    assert res.status_code == 200
    data = res.json()

    assert data[0]["name"] == "Me Ranked"
    assert data[0]["rank"] == 1
    assert data[1]["name"] == "Rookie Friend"
    assert data[1]["rank"] is None
    assert data[1]["make_pct"] == 100

def test_tie_breaker_more_shots_wins(client: TestClient, db_session):
    me = make_user(db_session, "Volume Shooter", "vol_shooter")
    friend = make_user(db_session, "Low Volume", "low_vol")
    make_friendship(db_session, me, friend, "accepted")

    # Same make_pct, but Me has more shots than Friend (10 vs 5)
    add_shots(db_session, me, made_count=8, missed_count=2)
    add_shots(db_session, friend, made_count=4, missed_count=1)

    res = client.get("/leaderboard", headers=auth_headers(me))
    assert res.status_code == 200
    data = res.json()

    assert [row["name"] for row in data] == ["Volume Shooter", "Low Volume"]
    assert data[0]["rank"] == 1
    assert data[0]["attempts"] == 10
    assert data[1]["rank"] == 2
    assert data[1]["attempts"] == 5

def test_week_vs_all_period(client: TestClient, db_session):
    me = make_user(db_session, "Me Period", "me_period")
    old_date = datetime.utcnow() - timedelta(days=10)

    # 5 old shots (80%) + 5 recent shots (40%)
    add_shots(db_session, me, made_count=4, missed_count=1, created_at=old_date)
    add_shots(db_session, me, made_count=2, missed_count=3)

    res_week = client.get("/leaderboard?period=week", headers=auth_headers(me))
    assert res_week.status_code == 200
    week_row = res_week.json()[0]
    assert week_row["attempts"] == 5
    assert week_row["make_pct"] == 40

    res_all = client.get("/leaderboard?period=all", headers=auth_headers(me))
    assert res_all.status_code == 200
    all_row = res_all.json()[0]
    assert all_row["attempts"] == 10
    assert all_row["make_pct"] == 60

def test_non_friend_and_pending_never_appear(client: TestClient, db_session):
    me = make_user(db_session, "Me Privacy", "me_priv")
    accepted_friend = make_user(db_session, "Accepted Pal", "acc_pal")
    pending_friend = make_user(db_session, "Pending Pal", "pend_pal")
    stranger = make_user(db_session, "Total Stranger", "stranger_x")

    make_friendship(db_session, me, accepted_friend, "accepted")
    make_friendship(db_session, me, pending_friend, "pending")

    for u in (me, accepted_friend, pending_friend, stranger):
        add_shots(db_session, u, made_count=5, missed_count=0)

    res = client.get("/leaderboard", headers=auth_headers(me))
    assert res.status_code == 200
    data = res.json()

    returned_names = {row["name"] for row in data}
    assert returned_names == {"Me Privacy", "Accepted Pal"}
    assert "Pending Pal" not in returned_names
    assert "Total Stranger" not in returned_names
    for row in data:
        assert "email" not in row