from fastapi import FastAPI
from database import Base, engine, SessionLocal
from models import PeopleCount
from datetime import datetime

# tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Railway Monitoring Backend")


# ======================
# API: LƯU DỮ LIỆU
# ======================
@app.post("/data")
def save_data(payload: dict):
    db = SessionLocal()

    record = PeopleCount(
        timestamp=datetime.now(),   # thời gian server
        density=payload["density"]
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    return {
        "status": "saved",
        "time": record.timestamp.strftime("%H:%M:%S"),
        "density": record.density
    }


# ======================
# API: XEM LỊCH SỬ
# ======================
@app.get("/stats")
def get_stats(limit: int = 100):
    """
    limit: số bản ghi trả về (mặc định 100)
    """
    db = SessionLocal()

    data = (
        db.query(PeopleCount)
        .order_by(PeopleCount.timestamp.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return [
        {
            "time": d.timestamp.strftime("%H:%M:%S"),
            "density": d.density
        }
        for d in reversed(data)
    ]






