# Official Domain Allowlist

Only these domains may be fetched by the source refresh pipeline. All other domains are blocked.

## Allowed domains

```
belastingdienst.nl          -- primary tax authority
www.belastingdienst.nl      -- main website
over-ons.belastingdienst.nl -- algoritmeregister
odb.belastingdienst.nl      -- developer portal
wetten.overheid.nl          -- legislation database
regels.overheid.nl          -- rule methodology
platform.claude.com         -- Anthropic Agent Skills docs
code.claude.com             -- Claude Code docs
```

## Rules

1. **HTTPS only** -- all connections must use `https://`. Plain HTTP is never permitted.
2. **No off-list redirects** -- if a response redirects to a domain not on this list, the fetch must abort and report the redirect target.
3. **No user-provided URLs** -- only URLs from `source-register.yaml` are permitted. A developer may not pass an arbitrary URL to the fetch script.
4. **No authentication required** -- all sources on this list are publicly accessible. If a source starts requiring authentication, report it as an error rather than prompting for credentials.
5. **Rate limiting** -- max 1 request per 2 seconds to any single domain. This respects server load and avoids triggering rate-limit responses.
6. **TLS verification** -- TLS certificate verification must be enabled. Never disable certificate checks.

## Domain categories

| Domain                        | Category            | Content type                     |
|-------------------------------|---------------------|----------------------------------|
| `belastingdienst.nl`          | Tax authority       | Redirects to www subdomain       |
| `www.belastingdienst.nl`      | Tax authority       | Guidance, rates, filing info     |
| `over-ons.belastingdienst.nl` | Tax authority       | Algorithm register, transparency |
| `odb.belastingdienst.nl`      | Tax authority       | Developer/software specs         |
| `wetten.overheid.nl`          | Government          | Full text of Dutch legislation   |
| `regels.overheid.nl`          | Government          | Rule authoring methodology       |
| `platform.claude.com`        | Anthropic           | Agent Skills documentation       |
| `code.claude.com`            | Anthropic           | Claude Code documentation        |
