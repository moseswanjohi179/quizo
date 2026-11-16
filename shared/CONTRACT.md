# Quizo Contract

This file is the single source of truth. `app.py`, `player.py` and `host.py` must all follow it exactly. If something here is wrong, fix it here first, then fix the code.

---

## 1. Rules

1. The server keeps ALL game state. Players and the host only ask it things.
2. Clients (`player.py`, `host.py`) talk only to the server, never to each other.
3. The server uses its own clock for time. Clients never send a time.
4. The server never sends the right answer while a question is open.
5. All data is sent and received as JSON.

---

## 2. Stages

The game is always in exactly one stage. Use these exact words.

| Stage | Meaning | Moves to next when |
|---|---|---|
| `lobby` | Waiting room, players join | host calls `/host/start` |
| `question` | Question open, timer running | time runs out, or host calls `/host/reveal` |
| `reveal` | Right answer and vote counts shown | host calls `/host/next` |
| `final` | Winner and leaderboard | host calls `/host/reset` |

After `/host/next`: next question (`question`) if one is left, otherwise `final`.

---

## 3. Question format (`questions.json`)

The file is a list of questions:

```json
[
  {
    "text": "Which planet is closest to the Sun?",
    "options": ["Venus", "Mercury", "Mars", "Earth"],
    "answer": 1,
    "seconds": 20
  }
]
```

| Field | Type | Meaning |
|---|---|---|
| `text` | string | The question |
| `options` | list of strings | 2 to 4 choices |
| `answer` | number | Position of the right option, **counting from 0** (1 = Mercury above) |
| `seconds` | number | Time players get |

**Numbering rule:** players see choices as 1, 2, 3, 4. `player.py` adds 1 when showing and subtracts 1 before sending. Everything sent to or from the server counts from 0.

---

## 4. Requests

The server link is in `config.py` as `SERVER_URL`.

### Player requests

| Request | Sends | Gets back |
|---|---|---|
| `POST /join` | `{"name": "Ann"}` | `{"player_id": "a1b2c3d4"}` |
| `GET /state` | nothing | the state (section 5) |
| `POST /answer` | `{"player_id": "a1b2c3d4", "choice": 1}` | `{"ok": true}` |

### Host requests

Every host request must include the header `X-Host-Key` with the secret password.

| Request | Does |
|---|---|
| `GET /host/state` | Same as `/state`, plus `counts` (section 5) |
| `POST /host/start` | `lobby` to first question |
| `POST /host/reveal` | Close the question, go to `reveal` |
| `POST /host/next` | Next question, or `final` after the last |
| `POST /host/reset` | Back to `lobby` with a fresh game |

Wrong or missing key: the server replies with status `401`.

---

## 5. State (`GET /state`)

```json
{
  "phase": "question",
  "question_number": 3,
  "total_questions": 10,
  "question": {"text": "...", "options": ["...", "..."], "seconds": 20},
  "seconds_left": 14.2,
  "players": 8,
  "answered": 5,
  "correct": null,
  "leaderboard": [{"name": "Ann", "score": 2390}]
}
```

| Field | Rule |
|---|---|
| `phase` | One of `lobby`, `question`, `reveal`, `final` |
| `question_number` | Starts at 1. Use 0 in `lobby` |
| `total_questions` | How many questions the game has |
| `question` | `null` in `lobby` and `final` |
| `seconds_left` | Counted by the server, never below 0 |
| `players` | How many have joined |
| `answered` | How many have answered this question |
| `correct` | Right option number (from 0). Only filled in `reveal` and `final`. `null` otherwise |
| `leaderboard` | Highest score first |

`/host/state` adds:

```json
"counts": [1, 3, 1, 0]
```

`counts` has one number per option: how many votes each got.

---

## 6. Errors

Every error uses a clear message that clients can show directly.

| When | Status | Body |
|---|---|---|
| `/join` with no name | `400` | `{"error": "Enter a name"}` |
| `/answer` after time is up | `400` | `{"ok": false, "error": "Too late"}` |
| `/answer` a second time | `400` | `{"ok": false, "error": "Already answered"}` |
| `/answer` with an unknown `player_id` | `400` | `{"ok": false, "error": "Unknown player"}` |
| Host request with a bad key | `401` | `{"error": "Wrong host key"}` |

Two players may use the same name. Players are told apart by `player_id`.

---

## 7. Scoring (`scoring.py`)

```python
def score(correct, seconds_taken, seconds_total):
    # returns a whole number:
    # 0 if wrong, up to 1000 if right and fast
```

`correct` is `True` or `False`. The server works out `seconds_taken` itself.

---

## 8. How the clients behave

**`player.py`**
1. Say "Waking the server, please wait..." and use a long wait (about 70 seconds) on the first request, because the free server may be asleep.
2. `POST /join`, keep the `player_id`.
3. Every second, `GET /state`.
4. Redraw only when `phase` or `question_number` changes.
5. Send answers with `POST /answer` and show any error message.

**`host.py`**
1. Same waiting message and long first wait.
2. Every second, `GET /host/state`, with the `X-Host-Key` header.
3. Show live vote bars from `counts`.
4. Keys: `Enter` reveal, `n` next question, `q` quit.

---

## 9. Server settings

| Setting | Value |
|---|---|
| Start command | `gunicorn app:app --workers 1 --threads 8` |
| Secret `HOST_KEY` | Set only in Render's settings. Never in the repo |
| Link | `QUIZO_URL` environment variable, default set in `config.py` |

Use `--workers 1`. The game lives in the server's memory, so more than one copy would split the game.

---

## 10. Changing this contract

1. Ask in the group chat first.
2. Edit this file in the same change as the code.
3. Tell everyone what changed.
