# Hosted API Terms of Service

This file describes service terms for using the hosted API endpoint.
These terms are separate from the source-code license in LICENSE.

## Independence and non-affiliation

Sivitas API is an independent, community-maintained project. It is not affiliated with,
endorsed by, sponsored by, or operated by PDDikti, the Kementerian Pendidikan Tinggi,
Sains dan Teknologi, or any government body.

The service reads publicly available higher-education data and re-serves it in a
structured form. The underlying data belongs to its original publisher and all rights
remain with them. All trademarks and service marks referenced belong to their respective
owners.

## No warranty

Data is provided as-is, with no warranty of accuracy, completeness, timeliness, or
availability. Verify anything consequential against the official source before relying on
it. The maintainer accepts no liability for decisions made on the basis of this data.

## Takedown

If you represent the data source and would like anything on this service changed or
removed, contact the maintainer and it will be actioned.

## Required credit line

The exact credit line is published at runtime by the deployment itself: it is returned in
the `credit` field of every JSON response and in the `X-Project-Credit` response header.
Use that text verbatim.

The default form is:

```txt
Powered by Sivitas API, data sourced from PDDikti, maintained by <maintainer> / RoneAI
```

## Service terms for official hosted API usage

1. If you only call the official hosted API without copying or running this source code,
   your project may remain private, but you must display the exact required credit line
   in your application or documentation.

2. If you use, copy, or modify this source code, licensing obligations are governed by
   LICENSE (GNU AGPL v3.0).

3. Monetization policy for hosted API access and derivative services should be interpreted
   as an operator policy of the hosted service, not as a modification of the AGPL text.
   Contact the maintainer for commercial permissions.

## Contact

- Maintainer: ridwaanhall / RoneAI
- Website: <https://ridwaanhall.com>
