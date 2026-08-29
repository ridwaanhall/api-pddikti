# Sivitas API

Structured access to Indonesian higher-education data — universities, study programs,
lecturers, and students — behind a clean, documented, production-grade FastAPI service.

The name comes from *sivitas akademika*, the Indonesian term for a university's academic
community.

> [!IMPORTANT]
> **Sivitas API is an independent, community-maintained project.** It is not affiliated
> with, endorsed by, sponsored by, or operated by PDDikti, the Kementerian Pendidikan
> Tinggi, Sains dan Teknologi, or any government body. It reads publicly available
> higher-education data and re-serves it in a structured form; the underlying data belongs
> to its original publisher and all rights remain with them.
>
> Data is provided **as-is**, with no warranty of accuracy, completeness, or availability.
> Verify anything consequential against the official source before relying on it. If you
> represent the data source and would like something changed or taken down, contact the
> maintainer and it will be actioned.

## Configuration

**No upstream, deployment, or third-party host is hardcoded in this repository.** Every URL
is read from the environment at startup, so the source can be published without disclosing
which services a deployment talks to.

Copy `.env.example` to `.env` and fill it in. The three values the API needs in order to
return data at all are:

| Variable | Purpose |
| --- | --- |
| `UPSTREAM_BASE_URL` | Base that entity paths are appended to |
| `UPSTREAM_ORIGIN` | Origin/referer sent with upstream requests |
| `UPSTREAM_DECRYPT_URL` | Endpoint that exchanges an encrypted payload for JSON |

Anything left blank disables the feature that needs it rather than failing at boot. `GET
/api/` reports which upstreams a running deployment actually resolved, so a misconfigured
environment is diagnosable without reading logs.

See `.env.example` for the full annotated surface, including branding, the optional
authenticated fallback upstream, caller-IP forwarding, support links, and analytics.

### Getting past upstream bot protection

The upstream sits behind an edge that fingerprints the **TLS handshake**, not just the
request headers. A plain Python HTTP client is rejected from datacenter IP ranges even
when every header is byte-identical to a browser, which is why a deployment can return
`403` while the same code works from a laptop.

Two things address this:

1. **Header parity** — the client sends the complete browser header set: the full
   `sec-ch-ua-*` client-hint family, `accept-encoding`, `accept-language`, `priority`,
   `dnt`, `sec-fetch-*`, and a contextual `referer`. It deliberately does *not* send
   `X-Forwarded-For` or `X-Real-IP`, because no browser does and a client-supplied
   forwarding header reads as proxy spoofing.
2. **TLS impersonation** — `UPSTREAM_IMPERSONATE=chrome` (the default) makes the
   client perform a real Chrome handshake via `curl_cffi`. This is the part that
   actually gets a datacenter IP through. Set it to `none` to opt out.

When a request still fails, the error body names the cause rather than hiding it:
`upstreams_tried` lists each base and why it failed, `decrypt_failure` gives the reason
the second leg failed, and `transport` reports which HTTP stack was used.

## Endpoints

Set `PUBLIC_BASE_URL` to your deployment, then:

- API Root — `/api/` (service metadata, upstream status, disclaimer)
- Swagger UI — `/api/docs`
- ReDoc — `/api/redoc`
- Interactive Web Playground — `/web`
- OpenAPI schema — `/api/openapi.json`

## About This Project

- Modular FastAPI routing by domain (`search`, `pt`, `prodi`, `dosen`, `mhs`, `stats`,
  `prodi-bidang-ilmu`)
- OpenAPI documentation with Swagger and ReDoc
- Interactive `/web` explorer with route groups, endpoint detail views, and live testing
- Availability gating and service metadata for traffic management
- SEO-ready landing and endpoint discovery pages

### Privacy in the web playground

Executing a request from `/web` does **not** put your input in a URL. The playground POSTs
to a single internal endpoint with parameters in the request body, so what you type never
reaches the address bar, the browser's network log, or server access logs. The copy-paste
code snippets still show the real public URL, because that is what a caller needs.

## Example Request

```bash
curl "$PUBLIC_BASE_URL/api/search/all/informatika/"
```

### Example Response Shape

```json
{
    "status": "success",
    "data": {
        "pt": [],
        "prodi": [],
        "dosen": [],
        "mahasiswa": []
    },
    "credit": "..."
}
```

## Service Availability Behavior

When traffic protection is active, non-overview API endpoints may return a temporary
limitation response (`HTTP 503`) with guidance to retry later. The API overview endpoint
remains available as the primary status source.

## Development

```bash
uv sync --group dev
uv run pytest
uv run fastapi dev app/main.py
```

## Stack

- FastAPI
- Starlette
- Requests (fallback HTTP transport)
- curl_cffi (primary HTTP transport, browser TLS impersonation)
- httpx
- uv (dependency and lock management)

## Source Code License

- This project uses GNU Affero General Public License v3.0 (`LICENSE`) with unmodified
  upstream license text.
- If you use, copy, modify, or redistribute this source code, follow the requirements
  stated in `LICENSE`.
- Any project-specific hosted-service rules are documented separately in
  `HOSTED_API_TERMS.md`.

## Hosted API Usage

- Calling the official hosted API does not by itself mean you are using, copying, or
  redistributing this source code.
- Rules for use of the hosted API are described separately as service terms in
  `HOSTED_API_TERMS.md`, not as source-code license obligations.
- If you need attribution, commercial-use, or other usage guidance for the hosted service,
  consult the API operator's terms or contact the maintainer.
