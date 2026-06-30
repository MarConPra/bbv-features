# Collab — AI-Powered Mentor Recommendation & Matching Engine

One intelligent platform where Indian learners go from idea to mentor to published paper / filed patent.

## Overview

Collab is an AI-driven layer inside your LMS that connects learners with verified professors, researchers, and IP professionals. This module handles the **first two stages** of the learner journey:

1. **Recommendation** — when a scholar creates a project, the system semantically matches it against a pool of verified mentors and returns a ranked list.
2. **Matching** — the scholar sends a connect request to a mentor; the mentor accepts or rejects; on acceptance the workspace unlocks.

## Architecture

```
                    TWO-STAGE MENTOR SYSTEM

  STAGE 1: RECOMMENDATION (AI embedding similarity)
  ┌─────────────────────────────────────────────────────┐
  │  Scholar creates project                            │
  │  └─> title + abstract + domain                      │
  │      └─> embed with all-MiniLM-L6-v2 (384-dim)      │
  │          └─> cosine similarity vs mentor embeddings  │
  │              └─> domain boost + availability filter  │
  │                  └─> top 3-5 mentors recommended     │
  └─────────────────────────────────────────────────────┘

  STAGE 2: MATCHING (Bidirectional confirmation)
  ┌─────────────────────────────────────────────────────┐
  │  Scholar reviews profile -> clicks "Connect"         │
  │  └─> Match created (status: pending)                 │
  │      └─> Mentor notified -> Accepts or Rejects       │
  │          └─> Accepted -> Workspace opens             │
  └─────────────────────────────────────────────────────┘
```

### Embedding Model

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension**: 384
- **Normalization**: L2-normalized (cosine similarity = dot product)
- **Mentor text**: `bio + research_areas + publication_titles`
- **Project text**: `title + abstract + domain`

### Ranking Algorithm

```
score = cosine_similarity(project_emb, mentor_emb)
  * domain_boost (1.15 if domain matches)
  * availability_penalty (0.5 if unavailable)
  + recency_bonus (0.05 if recent_publications_2yr > 0)
```

## Project Structure

```
collab/
├── README.md
├── requirements.txt             # Python dependencies
├── main.py                      # FastAPI entry point (uvicorn)
├── mentor_matching/             # Core package
│   ├── __init__.py
│   ├── models.py                # Pydantic schemas
│   ├── embedding.py             # Sentence-transformer wrapper
│   ├── recommender.py           # Similarity + ranking + filters
│   ├── matcher.py               # Match state machine
│   ├── data.py                  # 10 seed mentors + 5 sample projects
│   └── api.py                   # FastAPI router (8 endpoints)
├── data/
│   ├── mentors.json             # Persisted mentor profiles
│   └── embeddings/              # Cached embeddings (auto-generated)
└── tests/
    └── test_pipeline.py         # End-to-end pipeline validation
```

## Data Models

### Mentor
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Auto-generated |
| name | str | Full name |
| affiliation | str | University/Institute |
| department | str | Department |
| domain | str | Primary research domain |
| research_areas | list[str] | Keywords from Scopus/ORCID |
| bio | str | Academic bio |
| h_index | int | Scopus h-index |
| total_publications | int | Lifetime count |
| recent_publications_2yr | int | Papers in last 2 years |
| availability | bool | Accepting new scholars? |
| verified | bool | Credentials verified |
| embedding | list[float] | 384-dim vector (computed) |

### Project
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Auto-generated |
| title | str | Project title |
| abstract | str | Project description |
| domain | str | Research domain |
| goal | enum | paper / patent / invention |
| embedding | list[float] | 384-dim vector (computed) |

### Match
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Auto-generated |
| project_id | UUID | Linked project |
| mentor_id | UUID | Linked mentor |
| scholar_id | UUID | Who requested |
| status | enum | pending / accepted / rejected |
| similarity_score | float | Score at time of request |

## API Reference

All endpoints are under the `/api` prefix.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/mentors` | List all mentors |
| GET | `/api/mentors/{id}` | Get mentor profile |
| POST | `/api/projects` | Create project + auto-recommend |
| GET | `/api/projects` | List all projects |
| GET | `/api/projects/{id}/recommendations` | Get recommendations for a project |
| POST | `/api/matches` | Scholar sends connect request |
| GET | `/api/matches/{id}` | Get match status |
| PATCH | `/api/matches/{id}/respond` | Mentor accepts/rejects |
| GET | `/api/scholars/{id}/matches` | Scholar's match history |
| GET | `/api/debug/sample-projects` | Run all 5 sample projects |

### Example: Create Project & Get Recommendations

```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI for diabetic retinopathy screening",
    "abstract": "Deep learning model to detect diabetic retinopathy from retinal fundus images using CNNs and attention mechanisms.",
    "domain": "computer vision",
    "goal": "paper",
    "scholar_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Example: Connect to a Mentor

```bash
curl -X POST http://localhost:8000/api/matches \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "<project-uuid>",
    "mentor_id": "<mentor-uuid>",
    "scholar_id": "<scholar-uuid>"
  }'
```

### Example: Mentor Responds

```bash
curl -X PATCH http://localhost:8000/api/matches/<match-id>/respond \
  -H "Content-Type: application/json" \
  -d '{"action": "accepted"}'
```

## Seed Mentors (10 profiles)

The system ships with 10 pre-built mentor profiles mirroring real Indian research talent:

| Mentor | Affiliation | Domain | h-index |
|--------|-------------|--------|---------|
| Dr. Arjun Mehta | IIT Delhi | machine learning | 38 |
| Dr. Priya Sharma | IISc Bangalore | signal processing | 25 |
| Dr. Vikram Patel | IIT Bombay | natural language processing | 42 |
| Dr. Ananya Gupta | NIT Karnataka | computer vision | 20 |
| Dr. Suresh Kumar | Central Univ. Rajasthan | reinforcement learning | 15 |
| Dr. Neha Singh | IIT Madras (IP Office) | intellectual property | 8 |
| Dr. Rajesh Iyer | BARC / HBNI | physics | 30 |
| Dr. Kavita Joshi | University of Delhi | data science | 22 |
| Dr. Aditya Rao | IIT Kharagpur | generative AI | 18 |
| Dr. Sunita Reddy | IIT Hyderabad | computer vision | 28 |

5 sample projects are also included for testing across domains like computer vision, signal processing, IP, RL, and generative AI.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
# -> FastAPI running at http://localhost:8000
# -> Interactive docs at http://localhost:8000/docs

# Run the pipeline test
python tests/test_pipeline.py
```

## How to Add Real Mentors

The `data.py` file contains a `SEED_MENTORS` list. To load real mentors from IRINS, Scopus, or faculty directories:

1. Scrape profiles into the `Mentor` schema format
2. Append them to `SEED_MENTORS` or write them directly to `data/mentors.json`
3. Run the server — embeddings will auto-compute on first request

## Dependencies

- `fastapi` + `uvicorn` — API server
- `sentence-transformers` — Embedding model (all-MiniLM-L6-v2)
- `numpy` + `scikit-learn` — Cosine similarity
- `pydantic` — Data validation
