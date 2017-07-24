### Jira REST API

#### Overview

* The endpoints have the following format `<base-url>/rest/<api-name>/<api-number>/`. The `api-name` is `api` and `api-number` is `2`. A sample rest call to fetch a issue using `Basic Authentication`
```
curl -H "Authorization: Basic <Encoded username-password>" -H "Content-Type: application/json" <base-url>/rest/api/2/issue/<issue-no>`
```

#### Authentication

* A client can authenticate with JIRA REST API using three ways.
    * Basic Authentication
    * OAuth
    * Cookies

