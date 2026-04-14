---
title: "WebHook으로 구현하는 Agentic AI: 주차장 자동화 완전 구축 가이드"
description: "NOX NVR WebHook을 활용해 번호판 인식(LPR)부터 차단기 자동 제어까지 — 주차장 Agentic AI 자동화 시스템을 단계별로 구현하는 실전 개발 가이드입니다."
date: 2026-04-21
tags: [WebHook, NVR, 주차장 자동화, LPR, REST API, Agentic AI, 개발가이드]
slug: "webhook-agentic-ai-parking-automation-guide"
keywords: [WebHook NVR, 주차장 자동화, LPR 연동, REST API NVR, NOX NVR WebHook, 차단기 자동화, 번호판 인식 연동, Agentic AI 주차]
---

번호판이 카메라에 잡히는 순간, 차단기가 열린다. 사람의 개입은 없다.

이것이 Agentic AI 주차장 자동화의 결과다. 그리고 이 결과를 만드는 건 복잡한 AI 인프라가 아니다. NVR의 WebHook 하나면 충분하다.

이 가이드는 NOX NVR WebHook을 활용해 LPR(번호판 인식) 이벤트를 받아서 차단기를 자동으로 제어하고, 주차 데이터를 기록하는 시스템을 처음부터 구현하는 실전 가이드다.

## 아키텍처 개요

주차장 자동화 시스템의 전체 흐름은 다음과 같다:

```
[카메라] → [NOX NVR: LPR 감지]
              ↓ HTTP POST WebHook
[WebHook 서버: 이벤트 수신]
              ↓
[화이트리스트 DB 조회] → 등록 차량?
              ↓ YES
[차단기 API 호출] → 차단기 개방
              ↓
[주차 DB 기록] → 입/출차 시각, 번호판, 카메라 ID
              ↓
[알림 발송] → Slack / 메신저
```

전체 처리 시간: 번호판 인식 후 **1~2초 이내**. NOX NVR은 이벤트 감지 즉시 WebHook을 발송하고, 그 이후 로직은 개발자가 자유롭게 구성할 수 있다.

## NOX NVR WebHook 설정

### 1. WebHook URL 등록

NOX NVR 관리 콘솔 → **이벤트 설정** → **WebHook 구성**에서 외부 서버 URL을 등록한다.

```
POST http://your-server.com/webhook/nvr/events
Content-Type: application/json
```

### 2. WebHook 페이로드 구조

LPR 이벤트 발생 시 NOX NVR이 전송하는 페이로드:

```json
{
  "event_type": "lpr_detected",
  "timestamp": "2026-04-21T09:15:32.418Z",
  "camera_id": "CAM_ENTRANCE_01",
  "camera_name": "입구 카메라",
  "channel": 1,
  "data": {
    "license_plate": "12가3456",
    "confidence": 0.97,
    "direction": "in",
    "image_url": "http://nvr-host/snapshots/lpr/20260421_091532_CAM01.jpg",
    "crop_image_url": "http://nvr-host/snapshots/lpr/crop/20260421_091532_CAM01.jpg"
  },
  "device_id": "NOX-NVR-SN-20240001",
  "site_id": "SITE_PARKLOT_MAIN"
}
```

주요 필드:
- `event_type`: 이벤트 종류 (`lpr_detected`, `motion_detected`, `line_crossing` 등)
- `data.license_plate`: 인식된 번호판
- `data.confidence`: 인식 정확도 (0~1, 0.85 이상 권장)
- `data.direction`: 입차(`in`) / 출차(`out`)
- `data.image_url`: 전체 스냅샷 이미지 URL

## 구현: WebHook 서버

### Python (FastAPI) 기반 구현 예시

```python
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import httpx
import sqlite3
import asyncio

app = FastAPI()

# 화이트리스트 DB (실제로는 별도 데이터베이스 사용)
WHITELIST_DB = "parking.db"
GATE_API_URL = "http://gate-controller.local/api/v1"
SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

@app.post("/webhook/nvr/events")
async def handle_nvr_event(request: Request):
    payload = await request.json()
    
    # LPR 이벤트만 처리
    if payload.get("event_type") != "lpr_detected":
        return {"status": "ignored"}
    
    plate = payload["data"]["license_plate"]
    confidence = payload["data"]["confidence"]
    direction = payload["data"]["direction"]
    camera_id = payload["camera_id"]
    
    # 신뢰도 필터링 (85% 미만은 무시)
    if confidence < 0.85:
        return {"status": "low_confidence", "plate": plate}
    
    # 화이트리스트 조회
    is_registered = check_whitelist(plate)
    
    if is_registered:
        # 병렬로 차단기 제어 + DB 기록 + 알림 처리
        await asyncio.gather(
            open_gate(direction, camera_id),
            record_parking_event(plate, direction, camera_id, payload["timestamp"]),
            send_slack_notification(plate, direction, camera_id)
        )
        return {"status": "access_granted", "plate": plate}
    else:
        # 미등록 차량 기록 및 알림
        await record_unknown_vehicle(plate, camera_id, payload["timestamp"])
        return {"status": "access_denied", "plate": plate}


def check_whitelist(plate: str) -> bool:
    conn = sqlite3.connect(WHITELIST_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM whitelist WHERE license_plate = ? AND is_active = 1",
        (plate,)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


async def open_gate(direction: str, camera_id: str):
    """차단기 API 호출 — 실제 하드웨어 제어"""
    gate_id = get_gate_id_from_camera(camera_id)
    async with httpx.AsyncClient(timeout=3.0) as client:
        await client.post(
            f"{GATE_API_URL}/gates/{gate_id}/open",
            json={"duration_seconds": 10, "reason": "lpr_access"}
        )


async def record_parking_event(plate: str, direction: str, camera_id: str, timestamp: str):
    """주차 이벤트 DB 기록"""
    conn = sqlite3.connect(WHITELIST_DB)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO parking_log 
           (license_plate, direction, camera_id, event_time, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (plate, direction, camera_id, timestamp, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


async def send_slack_notification(plate: str, direction: str, camera_id: str):
    """Slack 알림 발송"""
    direction_label = "입차" if direction == "in" else "출차"
    message = f"🚗 [{direction_label}] {plate} — {camera_id} ({datetime.now().strftime('%H:%M:%S')})"
    async with httpx.AsyncClient() as client:
        await client.post(SLACK_WEBHOOK, json={"text": message})


def get_gate_id_from_camera(camera_id: str) -> str:
    """카메라 ID → 차단기 ID 매핑"""
    mapping = {
        "CAM_ENTRANCE_01": "GATE_01",
        "CAM_ENTRANCE_02": "GATE_02",
        "CAM_EXIT_01": "GATE_03",
    }
    return mapping.get(camera_id, "GATE_DEFAULT")
```

### Node.js (Express) 기반 구현 예시

```javascript
const express = require('express');
const axios = require('axios');
const Database = require('better-sqlite3');

const app = express();
app.use(express.json());

const db = new Database('parking.db');
const GATE_API_URL = 'http://gate-controller.local/api/v1';

app.post('/webhook/nvr/events', async (req, res) => {
  const { event_type, data, camera_id, timestamp } = req.body;

  if (event_type !== 'lpr_detected') {
    return res.json({ status: 'ignored' });
  }

  const { license_plate: plate, confidence, direction } = data;

  if (confidence < 0.85) {
    return res.json({ status: 'low_confidence', plate });
  }

  const isRegistered = checkWhitelist(plate);

  if (isRegistered) {
    // 비동기 병렬 처리
    await Promise.all([
      openGate(direction, camera_id),
      recordParkingEvent(plate, direction, camera_id, timestamp),
    ]);
    return res.json({ status: 'access_granted', plate });
  } else {
    return res.json({ status: 'access_denied', plate });
  }
});

function checkWhitelist(plate) {
  const row = db.prepare(
    'SELECT id FROM whitelist WHERE license_plate = ? AND is_active = 1'
  ).get(plate);
  return !!row;
}

async function openGate(direction, cameraId) {
  const gateId = getGateId(cameraId);
  await axios.post(`${GATE_API_URL}/gates/${gateId}/open`, {
    duration_seconds: 10,
    reason: 'lpr_access',
  });
}

function recordParkingEvent(plate, direction, cameraId, timestamp) {
  db.prepare(
    `INSERT INTO parking_log (license_plate, direction, camera_id, event_time)
     VALUES (?, ?, ?, ?)`
  ).run(plate, direction, cameraId, timestamp);
}

function getGateId(cameraId) {
  const mapping = {
    CAM_ENTRANCE_01: 'GATE_01',
    CAM_EXIT_01: 'GATE_02',
  };
  return mapping[cameraId] || 'GATE_DEFAULT';
}

app.listen(8080, () => console.log('WebHook server running on :8080'));
```

## DB 스키마

```sql
-- 화이트리스트 (등록 차량)
CREATE TABLE whitelist (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  license_plate TEXT NOT NULL UNIQUE,
  owner_name  TEXT,
  vehicle_type TEXT DEFAULT 'car',
  is_active   INTEGER DEFAULT 1,
  expires_at  TEXT,
  created_at  TEXT DEFAULT (datetime('now'))
);

-- 입출차 로그
CREATE TABLE parking_log (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  license_plate TEXT NOT NULL,
  direction     TEXT NOT NULL,  -- 'in' or 'out'
  camera_id     TEXT NOT NULL,
  event_time    TEXT NOT NULL,
  created_at    TEXT DEFAULT (datetime('now'))
);

-- 미등록 차량 로그
CREATE TABLE unknown_vehicles (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  license_plate TEXT NOT NULL,
  camera_id     TEXT NOT NULL,
  event_time    TEXT NOT NULL,
  image_url     TEXT,
  created_at    TEXT DEFAULT (datetime('now'))
);
```

## NOX NVR REST API 활용

WebHook이 **NVR → 외부 서버** 방향의 이벤트 전송이라면, REST API는 **외부 서버 → NVR** 방향의 제어다. 두 가지를 함께 활용하면 완전한 양방향 자동화가 가능하다.

### 카메라 목록 조회

```bash
GET /api/v1/cameras
Authorization: Bearer {api_token}
```

응답 예시:
```json
{
  "cameras": [
    {
      "id": "CAM_ENTRANCE_01",
      "name": "입구 카메라",
      "channel": 1,
      "status": "online",
      "resolution": "1920x1080",
      "ai_enabled": true,
      "ai_models": ["lpr", "motion"]
    }
  ]
}
```

### 실시간 스냅샷 요청

특정 이벤트 발생 시 추가 이미지가 필요하면 REST API로 즉시 스냅샷을 요청할 수 있다:

```bash
GET /api/v1/cameras/CAM_ENTRANCE_01/snapshot
Authorization: Bearer {api_token}
```

### 이벤트 히스토리 조회

```bash
GET /api/v1/events?event_type=lpr_detected&from=2026-04-21T00:00:00Z&limit=100
Authorization: Bearer {api_token}
```

관리자 대시보드나 리포트 생성 시 활용한다.

## 운영 팁

### 1. WebHook 재시도 처리

네트워크 문제로 WebHook 수신에 실패할 수 있다. 멱등성(idempotency)을 보장하는 구조로 설계해야 한다:

```python
@app.post("/webhook/nvr/events")
async def handle_nvr_event(request: Request):
    payload = await request.json()
    
    # 중복 처리 방지: event_id 기반 dedup
    event_id = f"{payload['device_id']}_{payload['timestamp']}_{payload['data']['license_plate']}"
    if is_already_processed(event_id):
        return {"status": "duplicate", "event_id": event_id}
    
    mark_processed(event_id)
    # ... 이후 처리
```

### 2. 차단기 API 타임아웃 대응

차단기 제어 API 호출이 실패하면 로그에 기록하고 수동 알림을 발송한다. WebHook 응답은 NVR에 즉시 반환하고, 차단기 제어는 비동기로 처리해야 WebHook 타임아웃을 피할 수 있다.

```python
@app.post("/webhook/nvr/events")
async def handle_nvr_event(request: Request):
    payload = await request.json()
    
    # 즉시 응답 반환 (NVR에 타임아웃 방지)
    asyncio.create_task(process_event(payload))
    return {"status": "received"}
```

### 3. 신뢰도 임계값 조정

`confidence` 값은 카메라 화질, 조명, 번호판 상태에 따라 달라진다. 처음에는 0.85로 시작하고, 실제 운영 데이터를 보면서 조정한다. 야간 운영 환경이라면 0.80으로 낮추는 것도 고려할 수 있다.

## 정리

NOX NVR WebHook을 활용한 주차장 Agentic AI 자동화의 핵심은 단순하다:

| 구성 요소 | 역할 |
|-----------|------|
| NOX NVR + LPR | 번호판 감지 및 WebHook 발송 |
| WebHook 서버 | 이벤트 수신, 비즈니스 로직 처리 |
| 화이트리스트 DB | 등록 차량 관리 |
| 차단기 API | 하드웨어 제어 |
| 주차 DB | 입출차 기록 |

코드 100줄 미만으로 번호판 인식부터 차단기 자동 제어까지 연결할 수 있다. 기존 시스템에 REST API가 있다면 연동 비용은 더 낮아진다.

Agentic AI는 거창한 개념이 아니다. **감지 → 판단 → 실행** 루프를 코드로 구현하는 것이다. NOX NVR이 그 루프의 시작점을 제공한다.

---

*NOX NVR WebHook 연동 기술 문의 및 POC 신청: [yiyolcorp.github.io](https://yiyolcorp.github.io)*
