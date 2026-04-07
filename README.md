# PDDikti API

Production API service for structured access to Indonesia higher-education data (PDDikti), including universities, study programs, lecturers, and students.

## Production Endpoint

alternative endpoint

```txt
https://pddikti.fastapicloud.dev
```

- Base URL: [https://pddikti.rone.dev](https://pddikti.rone.dev)
- API Root: [https://pddikti.rone.dev/api/](https://pddikti.rone.dev/api/)
- Swagger UI: [https://pddikti.rone.dev/api/docs](https://pddikti.rone.dev/api/docs)
- ReDoc: [https://pddikti.rone.dev/api/redoc](https://pddikti.rone.dev/api/redoc)
- Interactive Web Explorer: [https://pddikti.rone.dev/web](https://pddikti.rone.dev/web)

## About This Project

PDDikti API is built to provide consistent, production-grade endpoint access over public higher-education datasets. It includes:

- Modular FastAPI routing by domain (`search`, `pt`, `prodi`, `dosen`, `mhs`, `stats`, `prodi-bidang-ilmu`)
- OpenAPI documentation with Swagger and ReDoc
- Interactive `/web` explorer with route groups, endpoint details, and live request testing
- Availability gating and service metadata for traffic management
- SEO-ready landing and endpoint discovery pages

## How to Use the API

1. Open the API overview to inspect service metadata and status:
    - GET [https://pddikti.rone.dev/api/](https://pddikti.rone.dev/api/)
2. Browse endpoint documentation:
    - Swagger: [https://pddikti.rone.dev/api/docs](https://pddikti.rone.dev/api/docs)
    - ReDoc: [https://pddikti.rone.dev/api/redoc](https://pddikti.rone.dev/api/redoc)
3. Call endpoints directly from your app or client.

### Example Request

```bash
curl "https://pddikti.rone.dev/api/search/all/informatika/"
```

### Example Response Shape

```json
{
    "code": 200,
    "message": "ok",
    "data": {
        "pt": [],
        "prodi": [],
        "dosen": [],
        "mahasiswa": []
    }
}
```

## Service Availability Behavior

When traffic protection is active, non-overview API endpoints may return a temporary limitation response (`HTTP 503`) with guidance to retry later. The API overview endpoint remains available as the primary status source.

## Stack

- FastAPI
- Starlette
- Requests
- httpx
- uv (dependency and lock management)

## Source Code License

- This project uses GNU Affero General Public License v3.0 (`LICENSE`) with unmodified upstream license text.
- If you use, copy, modify, or redistribute this source code, follow the requirements stated in `LICENSE`.
- Any project-specific hosted-service rules are documented separately in `HOSTED_API_TERMS.md`.

## Hosted API Usage

- Calling the official hosted API does not by itself mean you are using, copying, or redistributing this source code.
- Rules for use of the hosted API are described separately as service terms in `HOSTED_API_TERMS.md`, not as source-code license obligations.
- If you need attribution, commercial-use, or other usage guidance for the hosted service, consult the API operator's terms or contact the maintainer.
