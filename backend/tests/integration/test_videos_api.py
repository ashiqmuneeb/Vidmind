import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_videos_lifecycle(async_client: AsyncClient):
    # 1. Create a video
    payload = {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "title": "Rick Astley Test Video",
        "enable_vision": False
    }
    create_res = await async_client.post("/api/videos", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    video_id = created["id"]
    assert created["title"] == "Rick Astley Test Video"
    assert created["source_type"] == "youtube"

    # 2. Check processing status was automatically created
    proc_res = await async_client.get(f"/api/videos/{video_id}/processing")
    assert proc_res.status_code == 200
    proc_data = proc_res.json()
    assert proc_data["video_id"] == video_id
    assert proc_data["status"] == "pending"
    assert proc_data["current_stage"] == "VALIDATE"

    # 3. Retrieve video details
    get_res = await async_client.get(f"/api/videos/{video_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == video_id

    # 4. List videos
    list_res = await async_client.get("/api/videos")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # 5. Delete video
    del_res = await async_client.delete(f"/api/videos/{video_id}")
    assert del_res.status_code == 204

    # 6. Verify deletion
    verify_res = await async_client.get(f"/api/videos/{video_id}")
    assert verify_res.status_code == 404
