### OAuth QuickBooks example project

This project demonstrates how to build a pipeline that integrates the OAuth 2.0 authentication flow for the QuickBooks API from Intuit.

In its essence, it consists of the following steps:

1. Visit the authentication URL (view output of initial-auth.ipynb)
2. The Flask server (oauth-server.py) handles the auth_code and stores the initial refresh_token and access_token
3. Update refresh token is run indefinitely to keep the refresh_token and access_token fresh

From any data pipeline in the project, the auth_client can be requested and used to fetch data. See the `main.orchest` pipeline with the `fetch-quickbooks.ipynb` example.

It makes most sense to run the `oauth.orchest` pipeline as a job. Although technically it can also run as an interactive pipeline. Note, it has no end time. It will run indefinitely (and keep refreshing the access/refresh tokens).

Note: it's important that only a single OAuth pipeline runs at a time (oauth.orchest). The auth flow does not support concurrently executing pipelines. This does _not_ affect "consumers" of the QuickBooks API. There _can_ be multiple auth_clients active at the same time (using the same access/refresh tokens).

Environment variables that need to be set (at the project level):

`HOST` e.g. `optimistic-newton-174ed1128.orchestapp.io` \
`QB_CLIENT_ENVIRONMENT` e.g. `sandbox` \
`QB_CLIENT_ID` \
`QB_CLIENT_SECRET`

**OAuth pipeline**

![OAuth pipeline](https://pviz.orchest.io/?pipeline=https://github.com/ricklamers/orchest-quickbooks-oauth/blob/master/oauth.orchest)

**Main pipeline (reading data)**

![Main pipeline](https://pviz.orchest.io/?pipeline=https://github.com/ricklamers/orchest-quickbooks-oauth/blob/master/main.orchest)
