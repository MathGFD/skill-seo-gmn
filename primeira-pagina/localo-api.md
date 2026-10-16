# Localo MCP — referência da API (snapshot 2026-10-09)

> Puxado via `docs(<categoria>)`. Se uma query falhar, rodar `docs` de novo: a API muda.

---

# Localo MCP API

This API exposes the Localo local-SEO platform via GraphQL. Use these MCP tools:

- **docs** — Read documentation for a category (you are here).
- **query** — Execute a read-only GraphQL query. Pass `query` and optional `variables`.
- **mutation** — Execute a GraphQL mutation. Pass `query` and optional `variables`.

All IDs are GUID type — 22-character base64url strings (e.g. "aBcDeFgHiJkLmNoPqRsTuV").
Dates use ISO 8601 format. DateTime includes time, Date is date-only (YYYY-MM-DD).

## Available documentation categories:
  - overview: All categories and how to use the query/mutation/docs tools
  - introspection: Schema introspection query
  - places: Search, list, view, update Business Profiles and tags
  - keywords: Add Keywords, view suggestions, refresh monitoring
  - grids: Position Maps: positions, difficulty, history
  - audits: Competitive analysis — competitor profiles, SEO phrases, citations
  - reviews: List reviews, sync from Google, Statistics
  - content: View Google posts and photo schedules
  - citations: View/manage business citations, change status
  - competitors: Competitor tracking and activity history
  - tasks: Smart Tasks: list, complete, generate
  - research: Client acquisition with Research mode, Sales mode, Leads finder, and Visibility scans
  - reports: Create reports, Reports manager, Auto-reports, sharing, and email delivery
  - insights: Statistics, Profile views, Website visits, Position Maps
  - scripting: How to call the API directly from custom scripts

Start with `docs("places")` to discover Business Profiles, then explore Keywords,
Position Maps, audits, etc.
Use `docs("introspection")` to discover the full schema programmatically.

## Passwords and other secrets

Queries and variables are logged for debugging. Pass every password, token, or other
secret as a variable and never write it into the query text. Give the variable a name
that contains one of `password`, `secret`, `token`, `authorization` (any letter case), for example `$password`,
`$smtpPassword`, or `$apiKeySecret`. The value of such a variable is left out of the
logs, and so is any field with such a name inside an input object.

```graphql
mutation($providerSecret: String!) {
  ...
}
```

```json
{"providerSecret": "the value that must stay private"}
```

## Google Business Profile publishing

MCP does not create, schedule, or publish posts or Google Maps / Google Business
Profile changes. It can read published posts, scheduled posts, and photo schedules
from the `content` category. This limitation is intentional for Google policy and
safety reasons.

## Batching: fetch data for multiple Business Profiles in one request

Use GraphQL aliases to query multiple Business Profiles in a single request instead of
sending separate requests for each Business Profile:

```graphql
query {
  p1: place(id: "aaa") { id activePlaceKeywords { id keyword visibility { current } } }
  p2: place(id: "bbb") { id activePlaceKeywords { id keyword visibility { current } } }
  p3: place(id: "ccc") { id activePlaceKeywords { id keyword visibility { current } } }
}
```

Batch up to 10-20 Business Profiles per request to stay within complexity limits.
This pattern works with any Business Profile-level query: Keywords, Position Maps,
reviews, etc.


---

# Business Profiles

Manage Google Business Profiles: search, list, view details, update, and tag.

## Search Business Profiles (find a business to add)

```graphql
query SearchPlaces($input: ListQueryPlaceSnapshotsInput!) {
  listQueryPlaceSnapshots(input: $input) {
    id title address mainImage country language ...
  }
}
```

```json
{ "input": { "query": "pizza new york", "country": "us", "language": "en" } }
```

## List Business Profiles (your managed Business Profiles)

```graphql
query PlaceList($input: PlaceListFiltersInput!) {
  placesList(input: $input) {
    places { id title address ... }
    placesTags { id name }
    totalCount
  }
}
```

```json
{ "input": { "pageNo": 1, "pageSize": 20, "active": true } }
```

`pageNo`, `pageSize`, and `active` are required. Set `active` to `true` for active
Business Profiles or `false` for inactive. Use `totalCount` to paginate through all results.
Filter by tags:
```json
{ "input": { "pageNo": 1, "pageSize": 20, "active": true, "tags": ["restaurant"] } }
```

## Get Business Profile Details

```graphql
query Place($placeId: GUID!) {
  place(id: $placeId) {
    id
    googlePlaceId
    country
    language
    latitude
    longitude
    activationTier
    isOpen
    verified
    userTags { id name }
    latestPlaceSnapshot {
      id title address rating reviewsCount category description mainImage link ...
    }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

## Update Business Profile

```graphql
mutation UpdatePlace($placeId: GUID!, $attrs: UpdatePlaceAttrs!) {
  updatePlace(placeId: $placeId, attrs: $attrs) {
    id
    latestPlaceSnapshot {
      id
      title
      address
    }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "attrs": { "country": "us", "language": "en" } }
```

Supported attrs: `country` (string), `language` (string), `latitude` (float), `longitude` (float).

## Refresh Business Profile (re-fetch from Google)

```graphql
mutation RefreshPlace($placeId: GUID!) {
  refreshPlace(placeId: $placeId) {
    id
    latestPlaceSnapshot { id title }
  }
}
```

## Set Business Profile Tags

```graphql
mutation SetPlaceTags($placeId: GUID!, $tags: [String!]!) {
  setPlaceTags(placeId: $placeId, tags: $tags) {
    id
    userTags { id name }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "tags": ["restaurant", "priority"] }
```

## Import a Business Profile (from search results)

After finding a business via `listQueryPlaceSnapshots`, import it to your account:

```graphql
mutation ImportPlace($placeSnapshotId: GUID!) {
  importGooglePlaceFromPlaceSnapshot(placeSnapshotId: $placeSnapshotId) {
    id
    latestPlaceSnapshot { title address }
  }
}
```

```json
{ "placeSnapshotId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

The `placeSnapshotId` comes from the `id` field in `listQueryPlaceSnapshots` results.

## List User Tags

```graphql
query UserTags {
  listUserTags {
    id
    name
  }
}
```

## Current User & Workspace

```graphql
query Me {
  me { id email locale timezone }
  organization {
    id name
    hasResearchMode
    researchModeQuota
  }
}
```

Use `me` to see who is authenticated. `organization` returns the current Workspace with plan details.


---

# Keywords

Add Keywords to monitor, get suggestions, view search terms, and refresh rankings.

## Keyword Research Workflow

To research the best Keywords for a Business Profile:

1. **Start with Google Search Terms** — call `placeGoogleSearchTerms` to see what keywords
   Google already associates with the Business Profile, sorted by impressions. These are real
   search terms from Google users that triggered the Business Profile to appear.
2. **Get AI suggestions** — call `placeKeywordSuggestions` with an optional seed search term
   in the `query` field to get Keyword ideas. Pass already-selected Keywords in
   `pendingKeywords` to avoid duplicates.
   Each suggestion includes `ahrefsOverview` with search volume and intent data.
3. **Add the best Keywords** — use `addPlaceKeyword` or `addPlaceKeywords` to start monitoring.
4. **Track performance** — on tracked Keywords, use `visibility` (current/previous/change score)
   and `ahrefsOverview` for ongoing search volume data.

## List Active Keywords (via Business Profile)

```graphql
query PlaceKeywords($placeId: GUID!) {
  place(id: $placeId) {
    id
    activePlaceKeywords {
      id keyword monitoringScheduledAt
      visibility { current previous change }
      ahrefsOverview { volume }
      latestGrids(limit: 1) {
        id orderedPlacePosition insertedAt
      }
    }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

Returns only actively monitored Keywords with ranking and search volume data.
Alternative: `listPlaceActiveKeywords(placeId: ...)` returns the same PlaceKeyword type
but as a flat list (without `ahrefsOverview` support).

## Add a Keyword

```graphql
mutation AddPlaceKeyword($input: AddPlaceKeywordInput!) {
  grid: addPlaceKeyword(input: $input) {
    id query country language
    placeKeyword { id keyword monitoringScheduledAt ... }
  }
}
```

```json
{ "input": { "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "query": "pizza delivery" } }
```

Note: the field is `query` (the search term), not `keyword`.
This creates a Keyword and triggers the first Position Map scan. Returns the Position Map metadata.

## Add Multiple Keywords at Once

```graphql
mutation AddPlaceKeywords($input: AddPlaceKeywordsInput!) {
  grids: addPlaceKeywords(input: $input) {
    id query placeKeyword { id keyword }
  }
}
```

```json
{ "input": { "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "keywords": ["pizza delivery", "best pizza"] } }
```

## Keyword Suggestions

```graphql
query PlaceKeywordSuggestions($placeId: GUID!, $query: String, $pendingKeywords: [String!]!) {
  placeKeywordSuggestions(placeId: $placeId, query: $query, pendingKeywords: $pendingKeywords) {
    id keyword value
    ahrefsOverview { volume intents { local commercial transactional } }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "query": "pizza", "pendingKeywords": [] }
```

`pendingKeywords` excludes already-selected keywords from suggestions.

## Google Search Terms (from Google Business Profile)

Returns real search terms that triggered the Business Profile to appear in Google results,
sorted by impressions. This is the best starting point for Keyword research:
these are search terms the Business Profile already ranks for.

```graphql
query PlaceGoogleSearchTerms($placeId: GUID!) {
  placeGoogleSearchTerms(placeId: $placeId) {
    keyword
    impressions
  }
}
```

Returns top 20 terms. Requires the Business Profile to have a connected Google account.

## Refresh a Keyword (trigger re-scan)

```graphql
mutation RefreshPlaceKeyword($placeKeywordId: GUID!) {
  refreshPlaceKeyword(placeKeywordId: $placeKeywordId) {
    id
  }
}
```

## Cancel Keyword Monitoring

```graphql
mutation CancelMonitoring($gridId: GUID!) {
  cancelMonitoring(gridId: $gridId) {
    id
    placeKeyword {
      id
      monitoringScheduledAt
    }
  }
}
```


---

# Position Maps

Position Maps show your position across a geographic area for a Keyword.
Each map point is an audit with a position and difficulty score.

## Get Position Map Details

```graphql
query Grid($gridId: GUID) {
  grid(id: $gridId) {
    id query sharedPermalink insertedAt
    centerLatitude centerLongitude
    orderedPlacePosition isError
    place {
      id
      latestPlaceSnapshot { title address ... }
    }
  }
}
```

```json
{ "gridId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

## Position Map Competitors

```graphql
query GridCompetitors($gridId: GUID) {
  grid(id: $gridId) {
    id orderedPlacePosition
    competitors {
      id orderedPosition
      queryPlace {
        id position distance
        placeSnapshot { title address rating reviewsCount ... }
      }
    }
  }
}
```

## Position Map Audits (individual map points)

```graphql
query GridAudits($gridId: GUID) {
  grid(id: $gridId) {
    id orderedPlacePosition
    audits {
      id latitude longitude difficulty position isError insertedAt ...
    }
  }
}
```

Each audit is one geographic point. `difficulty` and `position` show how hard it is
to rank at that point and your current position.

## Position Map History (for a Keyword)

```graphql
query GridsHistory($placeKeywordId: GUID!, $before: DateTime) {
  placeKeyword(id: $placeKeywordId) {
    id
    keyword
    latestGrids(limit: 25, before: $before) {
      id sharedPermalink insertedAt orderedPlacePosition competitorsCount
    }
  }
}
```

```json
{ "placeKeywordId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

Use `before` for pagination: pass the `insertedAt` of the last Position Map to get older ones.

## Latest Position Map for a Business Profile

```graphql
query LatestPlaceGrid($placeId: GUID!) {
  grid: latestPlaceGrid(placeId: $placeId) {
    id query centerLatitude centerLongitude country language
    placeKeyword { id keyword monitoringScheduledAt }
  }
}
```

## Get Business Profile Guidelines (SEO recommendations)

```graphql
query GetPlaceGuidelines($placeId: GUID!) {
  audit: getPlaceGuidelines(placeId: $placeId) {
    id query latitude longitude hasDescriptions
    grid { id query sharedPermalink gridSize }
    queryPlaces {
      id position distance
      placeSnapshot { id title address rating ... }
    }
    titleProminentPhrases { phrase occurrences scoreSum }
  }
}
```


---

# Audits

Competitive analysis at a single Position Map point. Shows competitor profiles,
SEO-relevant phrases, citations, and more.

## Get Audit Details

```graphql
query Audit($auditId: GUID!) {
  audit(id: $auditId) {
    id query difficulty position latitude longitude insertedAt
    grid { id query }
    placeKeyword { id keyword }
    queryPlaces {
      id position distance
      placeSnapshot { title address rating reviewsCount category ... }
    }
    titleProminentPhrases { phrase occurrences scoreSum inTop5: inTopN(n: 5) ... }
    descriptionProminentPhrases { phrase occurrences scoreSum ... }
    reviewsProminentPhrases { phrase occurrences scoreSum }
    citations { id rootDomain isWellKnown occurrences defaultPlaceHasReference ... }
    place { id latestPlaceSnapshot { title ... } }
  }
}
```

```json
{ "auditId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

Use introspection to discover all available fields on the Audit type.
Optionally pass `compareToPlaceSnapshotId` to compare against a specific competitor:
```json
{ "auditId": "...", "compareToPlaceSnapshotId": "..." }
```

## Get Audit Score

Overall Business Profile score (0-100 percent) with the 24 underlying checks.

```graphql
query AuditScore($auditId: GUID!) {
  audit(id: $auditId) {
    id scoreInputStatus
    score {
      percent earnedPoints maxPoints calculatedAt
      checks {
        checkId status
        stats {
          __typename
          ... on AuditBusinessNameLengthCheckStats { optimalMax optimalMin }
          ... on AuditBusinessNameKeywordsCheckStats { matchedSuggested suggestedKeywords }
          ... on AuditOpeningHoursCheckStats { competitorsWithHours criticalSlotsTotal }
          ... on AuditBusinessDescriptionLengthCheckStats { suggestedMax suggestedMin }
          ... on AuditBusinessDescriptionKeywordsCheckStats {
            matchedSuggested optimalMax optimalMin suggestedKeywords
          }
          ... on AuditPrimaryCategoryCheckStats {
            selectedPrimaryCategory selectedPrimaryCategoryId
          }
          ... on AuditAdditionalCategoriesCountCheckStats {
            hardMax hasCompetitorReference irrelevantCategoryIds
            noAdditionalCategoriesSuggested target
          }
          ... on AuditRatingCheckStats { displayRating }
          ... on AuditReviewsCountCheckStats { optimalMax optimalMin reviewsCount }
          ... on AuditReviewsGrowthCheckStats {
            highFrequencyWarning monthly reviewsGrowthAverage
          }
          ... on AuditReviewsTextRatioCheckStats { ratio }
          ... on AuditReviewsResponseRateCheckStats { responseRate }
          ... on AuditCitationsCheckStats { citationsCount }
          ... on AuditWebsiteCheckStats { isLocaloSite link ok }
          ... on AuditSocialMediaLinksCheckStats {
            competitorAverage socialLinksCount
            platformsActive { id name score competitorsWithPlatform }
            platformsMissed { id name score competitorsWithPlatform }
          }
          ... on AuditPhotosCountCheckStats { imagesCount optimalMax optimalMin }
          ... on AuditPhotosGrowthCheckStats { monthly photosGrowthAverage }
          ... on AuditPostsCountCheckStats { total }
          ... on AuditPostsFrequencyCheckStats { monthly }
          ... on AuditOffersCheckStats { total }
        }
      }
    }
  }
}
```

```json
{ "auditId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

`score` is null while the audit is still processing or when it does not have a
stored score (for example Position Map and older-version audits). `status` is
`OK`, `WARNING`, `ERROR`, or null when a check is not applicable. `checks[].stats`
is a typed union and is null for checks without statistics.


---

# Reviews

List and manage Google reviews for a single Business Profile or across all Business Profiles.

## List Reviews (single Business Profile)

```graphql
query PlaceReviews($input: ListReviewsInput!) {
  listReviews(input: $input) {
    id comment starRating reviewCreatedAt reviewerDisplayName
    replyComment replyUpdatedAt removedAt ...
  }
}
```

```json
{ "input": { "placeId": "aBcDeFgHiJkLmNoPqRsTuV" } }
```

Filter by star rating: `{ "input": { "placeId": "...", "starRating": 1 } }`

Reply filter options via `replyFilter`: `ALL_REVIEWS` (default), `WITH_REPLY`, `NO_REPLY`, `REMOVED`
```json
{ "input": { "placeId": "...", "replyFilter": "NO_REPLY" } }
```

Sort options via `orderBy`: `REVIEW_CREATED_AT` (default), `REVIEW_UPDATED_AT`, `REPLY_UPDATED_AT`, `STAR_RATING`, `INSERTED_AT`, `UPDATED_AT`
Direction via `orderDirection`: `DESC` (default), `ASC`

## List Reviews (all Business Profiles)

Omit `placeId` to query reviews across **all** Business Profiles in the Workspace.
Use the `place` field on each review to identify which Business Profile it belongs to.

```graphql
query AllReviews($input: ListReviewsInput!) {
  listReviews(input: $input) {
    id comment starRating reviewCreatedAt reviewerDisplayName
    replyComment removedAt
    place { id latestPlaceSnapshot { title address } }
  }
}
```

```json
{ "input": { "replyFilter": "NO_REPLY", "pageNo": 1, "pageSize": 20 } }
```

## Reviews Stats

```graphql
query ReviewsStats($placeId: GUID, $starRating: Int) {
  reviewsStats(placeId: $placeId, starRating: $starRating) {
    reviewsCount
    repliedCount
    removedCount
  }
}
```

`placeId` is optional: omit it to get stats across all Business Profiles.

## Reviews Chart (monthly trends)

```graphql
query ReviewsChart($placeId: GUID) {
  reviewsChart(placeId: $placeId) {
    month
    stats { total reviewsOneStars reviewsTwoStars reviewsThreeStars reviewsFourStars reviewsFiveStars }
  }
}
```

Returns monthly aggregated review counts by star rating. `placeId` is optional.

## Synchronize Reviews from Google

```graphql
mutation SynchronizeGoogleReviews($placeId: GUID!) {
  synchronizeGoogleReviews(placeId: $placeId) {
    id
    lastReviewsRefreshAt
  }
}
```

Triggers a fresh pull of reviews from Google. Use when you want the latest data.


---

# Statistics

View Statistics over time, usage metrics, and create shared reports.

## Google Metric Series (Profile views, Website visits, calls, directions, etc.)

```graphql
query MetricSeries($args: GoogleMetricSeriesArgs!) {
  googleMetricSeries(args: $args) { value date }
}
```

```json
{
  "args": {
    "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
    "metrics": ["BUSINESS_IMPRESSIONS_DESKTOP_MAPS"],
    "dateStart": "2026-01-01",
    "dateEnd": "2026-01-31"
  }
}
```

Common metrics: `BUSINESS_IMPRESSIONS_DESKTOP_MAPS`, `BUSINESS_IMPRESSIONS_MOBILE_MAPS`,
`BUSINESS_IMPRESSIONS_DESKTOP_SEARCH`, `BUSINESS_IMPRESSIONS_MOBILE_SEARCH`,
`CALL_CLICKS`, `WEBSITE_CLICKS`, `BUSINESS_DIRECTION_REQUESTS`

## Reviews Metric Series

```graphql
query ReviewsMetricSeries($args: ReviewsMetricSeriesArgs!) {
  reviewsMetricSeries(args: $args) { metric points { date value } }
}
```

```json
{
  "args": {
    "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
    "metrics": ["REVIEWS_RECEIVED", "REPLIES_CREATED"],
    "dateStart": "2026-01-01",
    "dateEnd": "2026-01-31"
  }
}
```

## Publication Metric Series

```graphql
query PublicationMetricSeries($args: PublicationMetricSeriesArgs!) {
  publicationMetricSeries(args: $args) { metric points { date value } }
}
```

```json
{
  "args": {
    "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
    "metrics": ["POSTS_CREATED", "PHOTOS_ADDED"],
    "dateStart": "2026-01-01",
    "dateEnd": "2026-01-31"
  }
}
```

## Position Map Usage Statistics

```graphql
query UsageMetrics($placeId: GUID!, $metrics: [String!]!, $dateStart: Date!, $dateEnd: Date!,
  $comparisonDateStart: Date, $comparisonDateEnd: Date) {
  usageMetrics(placeId: $placeId, metrics: $metrics, dateStart: $dateStart, dateEnd: $dateEnd,
    comparisonDateStart: $comparisonDateStart, comparisonDateEnd: $comparisonDateEnd) {
    metric total previousTotal
  }
}
```

```json
{
  "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
  "metrics": ["CREATED_GRIDS", "CREATED_AUDITS", "COMPETITORS_OVERTAKEN"],
  "dateStart": "2026-01-01",
  "dateEnd": "2026-01-31",
  "comparisonDateStart": "2025-12-01",
  "comparisonDateEnd": "2025-12-31"
}
```

Pass comparison dates to see period-over-period changes via `previousTotal`.

## Create Shared Statistics Report

```graphql
mutation CreateSharedInsights(
  $placeId: GUID!
  $period: String!
  $dateStart: Date!
  $dateEnd: Date!
  $compareEnabled: Boolean
) {
  createSharedInsights(
    placeId: $placeId
    period: $period
    dateStart: $dateStart
    dateEnd: $dateEnd
    compareEnabled: $compareEnabled
  ) {
    id
    sharedPermalink
  }
}
```

```json
{
  "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
  "period": "month",
  "dateStart": "2026-01-01",
  "dateEnd": "2026-01-31",
  "compareEnabled": true
}
```

Returns a `sharedPermalink` that can be used to view the report without authentication.


---

# Smart Tasks

Smart Tasks are AI-generated optimization tasks for Business Profiles. Each Smart Task is a
specific action to improve a Business Profile's local SEO (e.g. add a post, check
hours, update category).

## List Smart Tasks

```graphql
query ListPlaceTasks($placeId: GUID!, $status: TaskStatus) {
  listPlaceTasks(placeId: $placeId, status: $status) {
    id type status completionMethod completedAt
    metadata {
      ... on AddAdditionalCategoryMetadata { additionalCategoryToAddDisplayValue additionalCategoryToAddGcid }
      ... on RemoveAdditionalCategoryMetadata { additionalCategoryToRemoveDisplayValue additionalCategoryToRemoveGcid }
      ... on UpdateMainCategoryMetadata { currentMainCategoryDisplayValue mainCategoryToAddDisplayValue mainCategoryToAddGcid }
      ... on AddCitationMetadata { rootDomain citationGuid }
      ... on SocialLinksMetadata { socialLinkStatus }
      ... on PhoneMetadata { phoneStatus }
    }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

Default `status` is `PROPOSED` (pending Smart Tasks). Pass `COMPLETED` to see
completed Smart Tasks. Note: this query has a side effect: it generates new Smart Tasks
on first call for a Business Profile.

The `metadata` field is a union type — use inline fragments to access type-specific data.
Most Smart Task types return `null` for metadata; only category, citation, social link, and phone
Smart Tasks have structured metadata.

## Task Cycle (weekly boundaries)

```graphql
query TaskCycle {
  tasksCycleStart
  tasksCycleFinish
}
```

Returns the Monday 00:00 and Sunday 23:59 of the current week in the user's timezone.

## Mark Task as Completed

```graphql
mutation MarkTaskCompleted($taskId: GUID!) {
  markTaskAsCompleted(taskId: $taskId, completionMethod: USER_ACTION) {
    id status completedAt
  }
}
```

```json
{ "taskId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

Always use `USER_ACTION` as the completion method.

## Generate One More Smart Task

```graphql
mutation GetOneMoreTask($placeId: GUID!) {
  getOneMoreTask(placeId: $placeId) {
    id type status
  }
}
```

Returns `null` if no more Smart Tasks can be generated.


---

# Client Acquisition, Research Mode & Sales Mode

Research mode creates one-off Visibility scans without Keyword monitoring.
Sales mode adds client acquisition metadata (city, status) to Visibility scans.

## Prospecting outside managed Business Profiles

Research mode can handle Leads finder and potential client lists beyond already managed
Business Profiles. Use `listQueryPlaceSnapshots` from `docs("places")` to search for
businesses first. The app uses this for Research mode and Sales mode search results with fields
like `id`, `title`, `country`, `language`, `latitude`, `longitude`, and `category`.
If the workflow needs a `placeId`, import the Business Profile from the snapshot with
`importGooglePlaceFromPlaceSnapshot` and then create a Research mode or Sales mode
Visibility scan for that `placeId`.

Client acquisition workflows are available through `listSalesGrids`,
`listResearchPlaces`, `listResearchPlaceGrids`, and `upsertSalesProspect`.

## Check Research Mode Availability

```graphql
query ResearchModeStatus {
  organization {
    hasResearchMode
    researchModeQuota
    researchModeRenewsAt
  }
  researchModeUsage
}
```

`researchModeUsage` returns Visibility scans used this billing period. `researchModeQuota`
returns remaining quota.

## Create a Research Mode Visibility Scan

```graphql
mutation CreateResearchGrid($input: CreateResearchGridInput!) {
  createResearchGrid(input: $input) {
    id query isResearchMode insertedAt
    place { id latestPlaceSnapshot { title } }
  }
}
```

```json
{
  "input": {
    "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
    "query": "pizza delivery",
    "country": "us",
    "language": "en",
    "latitude": 40.7128,
    "longitude": -74.006,
    "gridSize": 5,
    "areaWidth": 5000.0,
    "areaHeight": 5000.0
  }
}
```

Technical `gridSize` values: `0` = smart grid; `3`, `5`, `7`, and `9` create
square 3x3, 5x5, 7x7, and 9x9 grids.
`areaWidth`/`areaHeight` are in meters, only used for square grids (`3`, `5`, `7`, `9`).

## Create a Sales Mode Visibility Scan

Add a `sales` object to attach client acquisition metadata:

```json
{
  "input": {
    "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
    "query": "pizza delivery",
    "country": "us",
    "language": "en",
    "latitude": 40.7128,
    "longitude": -74.006,
    "gridSize": 5,
    "areaWidth": 5000.0,
    "areaHeight": 5000.0,
    "sales": { "city": "New York" }
  }
}
```

## List Sales Mode Visibility Scans

```graphql
query ListSalesGrids($input: ListSalesGridsInput!) {
  listSalesGrids(input: $input) {
    id query insertedAt gridSize
    sales { city status }
    place { id latestPlaceSnapshot { title address } }
  }
  countSalesGrids
}
```

```json
{ "input": { "pageNo": 1, "pageSize": 20 } }
```

Filter by status or text:
```json
{ "input": { "pageNo": 1, "pageSize": 20, "filter": { "statuses": ["ONGOING"], "text": "pizza" } } }
```

## Update Sales Mode Visibility Scan Status

```graphql
mutation UpdateSalesGridStatus($gridId: GUID!, $status: SalesGridStatus!) {
  updateSalesGridStatus(gridId: $gridId, status: $status) {
    id
    sales { status }
  }
}
```

```json
{ "gridId": "aBcDeFgHiJkLmNoPqRsTuV", "status": "ARCHIVED" }
```

Status values: `ONGOING`, `ARCHIVED`

## List Potential Clients (Business Profiles with Research mode Visibility scans)

```graphql
query ListResearchPlaces($input: ListResearchPlacesInput!) {
  listResearchPlaces(input: $input) {
    latestGridAt
    place { id latestPlaceSnapshot { title address } }
  }
  countResearchPlaces
}
```

```json
{ "input": { "pageNo": 1, "pageSize": 20 } }
```

## List Research Mode Visibility Scans for a Business Profile

```graphql
query ListResearchPlaceGrids($placeId: String!, $input: ListResearchPlaceGridsInput!) {
  listResearchPlaceGrids(placeId: $placeId, input: $input) {
    id query insertedAt gridSize orderedPlacePosition isError
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "input": { "pageNo": 1, "pageSize": 20 } }
```

## Leads List (potential clients)

Track potential clients by Google Place ID with a status flow.

```graphql
mutation UpsertSalesProspect($input: UpsertSalesProspectInput!) {
  upsertSalesProspect(input: $input) {
    id status comment
  }
}
```

```json
{ "input": { "googlePlaceId": "ChIJ...", "status": "TODO", "comment": "Interested in SEO" } }
```

Status flow: `TODO` → `CONTACTED` → `CONVERTED` (or `IGNORED`)

The `salesProspect` field is also available on `PlaceSnapshot` to check if a prospect
exists for a given Business Profile when viewing Position Map results.


---

# Reports

Create, list, view, print, share, and email Reports.

MCP supports Reports manager queries and mutations through the normal `query` and `mutation`
tools. The `reportsUpdated` GraphQL subscription is not available through MCP; poll
`placeReports` or `report` instead when waiting for status changes.

## Create a Monthly or One-off Report

Reports can be created through MCP. Use the exact mutation name `createSingleRaport`
(one "p" in Raport) with the Localo place GUID and inclusive start/end dates:

```graphql
mutation CreateSingleRaport($input: CreateSingleRaportInput!) {
  createSingleRaport(input: $input)
}
```

```json
{ "input": { "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "startDate": "2026-08-01", "endDate": "2026-08-31" } }
```

The mutation returns `true` when generation is queued, not when the report is ready.
Before creating it, list existing reports for this place and reuse a suitable report
when one already covers the requested dates. After creation, poll `placeReports`
without a status filter to find the new report by date range and ID. Do not repeat
the creation mutation while waiting. Poll `report` until `readyForEmail` is true.
If generation fails, inspect `sections.*.errorMessage` and explain the failure.

## List Reports

```graphql
query PlaceReports($placeId: GUID!, $status: ReportStatus) {
  placeReports(placeId: $placeId, status: $status) {
    id
    startDate
    endDate
    status
    readyForEmail
    generationCompletedAt
    emailSentAt
    emailError
    emailErrorMessage
    insertedAt
    sendTo
    sendCopyTo
    sharedPermalink
    pdfDownloadedAt
    linkGeneratedAt
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "status": "SENT" }
```

Omit `status` to list reports regardless of status.

## Get Report Details

```graphql
query Report($reportId: GUID!) {
  report(reportId: $reportId) {
    id
    placeName
    startDate
    endDate
    status
    readyForEmail
    generationCompletedAt
    emailSentAt
    emailError
    emailErrorMessage
    customMessage
    sendTo
    sendCopyTo
    sharedPermalink
    sections {
      statistics {
        status
        errorMessage
        data {
          phoneCalls
          profileViews
          websiteVisits
          directions
          visibilityMaps
          competitorsBeaten
          profileAudits
        }
      }
      keywords {
        status
        errorMessage
        data {
          keywordId
          keywordText
          positionChange
          previousPosition
          currentPosition
          oldestInsertedAt
          oldestSharedPermalink
          newestInsertedAt
          newestSharedPermalink
        }
      }
      reviews {
        status
        errorMessage
        data {
          oneStar
          twoStars
          threeStars
          fourStars
          fiveStars
        }
      }
      keyActions {
        status
        errorMessage
        data {
          addedMedia
          addedPosts
          reviewsReplies
          offersPublished
          reviewsReceived
          totalActions
        }
      }
      catalogs {
        status
        errorMessage
        data {
          guid
          rootDomain
        }
      }
      competitors { status errorMessage data }
    }
  }
}
```

```json
{ "reportId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

## Get a Printable Report URL

```graphql
query ReportPrintUrl($reportId: GUID!, $format: PrintFormat, $language: String) {
  reportPrintUrl(reportId: $reportId, format: $format, language: $language)
}
```

```json
{ "reportId": "aBcDeFgHiJkLmNoPqRsTuV", "format": "A4", "language": "en" }
```

## Create a Shared Permalink

```graphql
mutation CreateReportSharedPermalink($reportId: GUID!) {
  createReportSharedPermalink(reportId: $reportId)
}
```

```json
{ "reportId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

The mutation returns only the `sharedPermalink` token. Build the full share URL as:

    https://app.localo.com/shared-reports/<sharedPermalink>/reports/<reportId>

Replace `<sharedPermalink>` with the mutation result and `<reportId>` with the report ID.

## Send a Report by Email

Send only when `readyForEmail` is true. `sendReportEmail: true` means the request
was queued, not that the email was sent. Poll the report until `status` changes
from `SENDING`. On `FAILED`, read `emailError` and `emailErrorMessage`, explain
the failure, and let the user correct their email settings before retrying.
`SENT` alone can also mean a PDF was requested or a sharing link was generated.
These actions mark a draft report as sent without changing email delivery fields
or replacing a pending or failed email status. `SENT` with `emailSentAt` confirms
acceptance by the email server, not inbox delivery.
`sendTo` records requested recipients and is not proof of delivery. A previous
`emailSentAt` can remain after a failed resend, so always check the latest status.

If `SENDING` does not resolve, report that delivery is unconfirmed and stop polling
after a bounded wait. A user-requested retry is allowed after an interrupted attempt,
but do not resend automatically: the first attempt may already have been accepted.

```graphql
mutation SendReportEmail(
  $reportId: GUID!
  $toEmails: [String!]!
  $sendCopyToMe: Boolean
  $copyToEmails: [String!]
  $language: String!
  $subject: String
) {
  sendReportEmail(
    reportId: $reportId
    toEmails: $toEmails
    sendCopyToMe: $sendCopyToMe
    copyToEmails: $copyToEmails
    language: $language
    subject: $subject
  )
}
```

```json
{
  "reportId": "aBcDeFgHiJkLmNoPqRsTuV",
  "toEmails": ["client@example.com"],
  "sendCopyToMe": true,
  "copyToEmails": [],
  "language": "en",
  "subject": "Your Localo report"
}
```


---

# Competitors

Track competitor changes over time with Competitor Activity Tracker.
Mark competitors as favorites to monitor their profile changes.

## How it works (two-phase loading)

1. **Get current state**: Call `getPlaceGuidelines` (see "Position Maps" docs) to get the
   latest audit with all current competitor positions and snapshots.
2. **Load competitor activity history**: Call `auditActionsTrack` **repeatedly** to walk backwards
   through time. Each response returns one audit snapshot with the changes detected
   since the previous audit.

## Competitor Activity History (paginated)

```graphql
query AuditActionsTrack($placeId: GUID!, $auditInsertedBefore: DateTime) {
  auditActionsTrack(placeId: $placeId, auditInsertedBefore: $auditInsertedBefore) {
    id
    audit { id insertedAt }
    previousAudit { id }
    changedPlaces {
      id
      queryPlace {
        id position
        placeSnapshot { id title address googlePlaceId ... }
      }
      previousQueryPlace { id position }
      title { current previous }
      description { current previous }
      reviewsCount { current previous }
      address { current previous }
      freshPosts { id placePost { id title body createdAt ... } }
      ...
    }
  }
}
```

### Pagination — recursive calls

**Step 1** — First call (most recent changes), omit `auditInsertedBefore`:
```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

**Step 2** — Take `audit.insertedAt` from the response and pass it as
`auditInsertedBefore` to get the **next older** audit:
```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "auditInsertedBefore": "2026-02-15T08:30:00Z" }
```

**Step 3** — Repeat until you have enough history. Each response returns one audit
snapshot. The `changedPlaces` array contains only competitors whose data **changed**
between that audit and the previous one.

### Change diff fields

Each item in `changedPlaces` includes diff fields with `current` and `previous` values:
- `title`, `description`, `address`, `link` — string diffs
- `reviewsCount`, `imagesCount` — integer diffs
- `categories` — list of strings diffs
- `location` — lat/lng diffs
- `queryPlace.position` vs `previousQueryPlace.position` — ranking position change
  (audits created with guidelines v6 leave the audited business unranked, so its `position` is null there)
- `freshPosts` — new Google posts published since the previous audit

## List Favorite Competitors

```graphql
query ListFavoriteCompetitors($placeId: GUID!) {
  competitors: listPlaceActionTrackerFavoriteCompetitors(placeId: $placeId) {
    id
    googlePlaceId
    favorite
    changesCount
  }
}
```

## Set Favorite Competitor

```graphql
mutation SetFavoriteCompetitor($placeId: GUID!, $googlePlaceId: String!) {
  competitor: setPlaceActionTrackerFavoriteCompetitor(
    placeId: $placeId
    googlePlaceId: $googlePlaceId
  ) {
    id
    favorite
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "googlePlaceId": "ChIJ..." }
```

Note: `googlePlaceId` here is a Google Place ID string (e.g. "ChIJ..."), not a GUID.

## Remove Favorite Competitor

```graphql
mutation RemoveFavoriteCompetitor($placeId: GUID!, $googlePlaceId: String!) {
  success: removePlaceActionTrackerFavoriteCompetitor(
    placeId: $placeId
    googlePlaceId: $googlePlaceId
  )
}
```


---

# Content

View published Google posts, scheduled Business Profile posts, and photo schedules.

## Read-only boundary

MCP content tools are read-only. They do not create, schedule, publish, or push
posts or Google Maps / Google Business Profile changes. This limitation is intentional
for Google policy and safety reasons.
The available MCP surface here is reading published Google posts via `listGooglePosts`,
scheduled Business Profile posts via `listScheduledLocalPosts`, and photo schedules via
`getSchedules`.

## List Published Google Posts

```graphql
query PublishedPosts($placeId: GUID!, $topicType: InputGooglePostTopicType!) {
  listGooglePosts(placeId: $placeId, topicType: $topicType) {
    id summary state topicType createdAt
    callToAction { actionType url }
    media { mediaFormat googleUrl }
    ...
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV", "topicType": "STANDARD" }
```

Topic types: `STANDARD`, `EVENT`, `OFFER`

## List Scheduled Business Profile Posts

```graphql
query ListScheduledPosts($placeId: GUID!, $topicType: InputGooglePostTopicType!) {
  listScheduledLocalPosts(placeId: $placeId, topicType: $topicType) {
    id scheduledAt state apiError
    post { topicType summary callToAction { actionType url } media { sourceUrl } ... }
  }
}
```

## Get Photo Schedules

```graphql
query GetSchedules($placeId: GUID!) {
  getSchedules(placeId: $placeId) {
    customSchedule {
      id
      uploads { id publishDate photos { id sourceUrl } }
    }
    localoSchedule {
      id lastPublishedAt
      nextPublicationPhotos { id sourceUrl }
      upload { id publishDate photos { id sourceUrl } }
    }
  }
}
```


---

# Citations

Business citations are mentions of your business on external websites.
Managing citations helps with local SEO authority.

## List Business Profile Citations

```graphql
query FetchPlaceCitations(
  $placeId: GUID!
  $orderBy: PlaceCitationsOrder
  $statusFilter: PlaceCitationStatus
  $search: String
) {
  fetchPlaceCitations(
    placeId: $placeId
    orderBy: $orderBy
    statusFilter: $statusFilter
    search: $search
  ) {
    id status linksToTarget competitorsOccurrencesCount isNew
    placeCitationDomain { id rootDomain domainRating isWellKnown canBeLinked activationLink }
  }
}
```

```json
{ "placeId": "aBcDeFgHiJkLmNoPqRsTuV" }
```

Filter by status: `{ "placeId": "...", "statusFilter": "ACTIVE" }`
Status values: `ACTIVE`, `PENDING`, `IGNORED`, `NOT_FOUND`
Order options: `DOMAIN_RATING_DESC`, `COMPETITORS_OCCURRENCES_DESC`, etc.

## Citations Stats

```graphql
query FetchPlaceCitationsStats($placeId: GUID!) {
  fetchPlaceCitationsStats(placeId: $placeId) {
    status
    count
  }
}
```

## Change Citation Status

```graphql
mutation ChangeCitationStatus(
  $placeId: GUID!
  $placeCitationGuid: GUID!
  $toStatus: PlaceCitationStatus!
  $ignoreReason: String
) {
  changeCitationStatus(
    placeId: $placeId
    placeCitationGuid: $placeCitationGuid
    toStatus: $toStatus
    ignoreReason: $ignoreReason
  ) {
    id
    status
    statusChangedAt
  }
}
```

```json
{
  "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
  "placeCitationGuid": "xYzAbCdEfGhIjKlMnOpQrS",
  "toStatus": "ACTIVE"
}
```

## Create a New Citation

```graphql
mutation CreateNewPlaceCitation(
  $placeId: GUID!
  $rootDomain: String!
  $canBeLinked: Boolean!
  $status: PlaceCitationStatus!
  $linksToTarget: [String!]
) {
  createNewPlaceCitation(
    placeId: $placeId
    rootDomain: $rootDomain
    canBeLinked: $canBeLinked
    status: $status
    linksToTarget: $linksToTarget
  ) {
    id status
    placeCitationDomain { rootDomain domainRating }
  }
}
```

```json
{
  "placeId": "aBcDeFgHiJkLmNoPqRsTuV",
  "rootDomain": "yelp.com",
  "canBeLinked": true,
  "status": "ACTIVE",
  "linksToTarget": ["https://yelp.com/biz/my-restaurant"]
}
```

