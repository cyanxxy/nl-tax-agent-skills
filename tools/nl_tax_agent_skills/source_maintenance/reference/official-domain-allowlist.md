# Official Domain Allowlist

Only these domains may be fetched by the source refresh pipeline. All other domains are blocked.

## Allowed domains

```
belastingdienst.nl          -- primary tax authority
www.belastingdienst.nl      -- main website
download.belastingdienst.nl -- official forms and explanatory PDFs
stichtingenvereniging.belastingdienst.nl -- official rubric structure (sector conditions remain scoped)
over-ons.belastingdienst.nl -- algoritmeregister
odb.belastingdienst.nl      -- developer portal
wetten.overheid.nl          -- legislation database
zoek.officielebekendmakingen.nl -- official Dutch legal publications
vat-one-stop-shop.ec.europa.eu -- European Commission OSS/IOSS guidance
eur-lex.europa.eu           -- EU legislation (VAT Directive 2006/112/EC)
regels.overheid.nl          -- rule methodology
platform.claude.com         -- Anthropic Agent Skills docs
code.claude.com             -- Claude Code docs
svb.nl                      -- SVB state-pension authority
www.svb.nl                  -- SVB (AOW-leeftijd)
rijksoverheid.nl            -- central government portal
www.rijksoverheid.nl        -- Rijksoverheid (AOW-leeftijd schedule)
rvo.nl                      -- RVO (Energielijst / Milieulijst)
www.rvo.nl                  -- RVO (EIA, MIA and Vamil lists and maxima)
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
| `www.svb.nl`                  | Government (SVB)    | AOW-leeftijd (state-pension age)  |
| `www.rijksoverheid.nl`        | Government          | AOW-leeftijd schedule             |
| `rvo.nl`                      | Government (RVO)    | Redirects to www subdomain        |
| `www.rvo.nl`                  | Government (RVO)    | Energielijst / Milieulijst, EIA, MIA and Vamil maxima |
| `download.belastingdienst.nl` | Tax authority      | Official forms and explanatory PDFs (toelichtingen) |
| `stichtingenvereniging.belastingdienst.nl` | Tax authority | Stichting/vereniging loket; VAT rubric structure only |
| `zoek.officielebekendmakingen.nl` | Government      | Staatscourant decrees and ministerial regulations |
| `vat-one-stop-shop.ec.europa.eu` | European Commission | OSS/IOSS guidance and explanatory notes |
| `eur-lex.europa.eu`           | European Union      | EU legislation; VAT Directive 2006/112/EC currency-conversion articles for OSS. Automated fetches get an HTTP 202 bot challenge, so a human confirms the text in a browser |
