# PDDIKTI API

[![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/e637f4e3-a75d-49c8-beb0-0f19f8eb52cd.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/e637f4e3-a75d-49c8-beb0-0f19f8eb52cd)

## INFO

> API ini telah di-update berdasarkan data baru di <https://pddikti.kemdiktisaintek.go.id/>

## Bagaimana cara menggunakan API?

Baca dokumentasi berbahasa indonesia ini [PDDikti Docs](https://pddikti-docs.ridwaanhall.com). mudah dan gampang digunakan.

## API Documentation

[https://pddikti-docs.ridwaanhall.com](https://pddikti-docs.ridwaanhall.com)

![API Documentation](https://github.com/user-attachments/assets/a30872f0-e3d5-45de-a7a1-86609a145fe4)

## Tampilan pada API Endpoint

[https://api-pddikti.ridwaanhall.com](https://api-pddikti.ridwaanhall.com)

![API Overview](images/api-overview.png)

## API Traffic Management

This API includes intelligent traffic management to ensure optimal performance and system stability during high-traffic periods.

### Service Status Monitoring

The API automatically monitors traffic levels and may temporarily limit certain endpoints to maintain service quality for all users.

### Response Format

During high traffic periods, some endpoints may return a professional service notice:

```json
{
    "error": "Service Temporarily Limited",
    "message": "Due to high traffic volume, this endpoint is temporarily unavailable to ensure system stability.",
    "code": 503,
    "status": "Service Unavailable",
    "available_endpoint": {
        "url": "https://api-pddikti.ridwaanhall.com",
        "method": "GET",
        "description": "API Overview - Current service status and available resources"
    },
    "support": {
        "retry_suggestion": "Please try again in a few minutes",
        "contact": "Contact support if this issue persists"
    }
}
```

The response includes proper HTTP headers:

- `Content-Type: application/json`
- `Retry-After: 3600` (suggesting retry after 1 hour)

All API responses maintain consistent formatting and provide clear guidance for users during service limitations.

The API overview endpoint will always remain accessible and will show the current service status and additional information about the traffic management state.
