# Use-Case Flow Specification

## Use Case: Recommend Missing Index Candidate

**Actors:** Database Administrator (primary), System (parsing/recommendation engine)

**Preconditions:**
- A slow query log entry has been ingested and parsed (UC: *Ingest slow query logs* complete).
- The `EXPLAIN` plan for the query has been successfully parsed.
- A sequential scan has been detected on a table exceeding the configured row threshold (UC: *Detect sequential scan* triggered, extension point reached).

**Postconditions:**
- An index recommendation is generated, stored, and linked to the originating query.
- The recommendation appears in the DBA's dashboard review queue with status "Pending Review."
- The recommendation is queued for inclusion in the next weekly digest.

**Main Success Scenario:**
1. System detects a sequential scan on a table over the size threshold during `EXPLAIN` parsing.
2. System extracts the columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses of the query.
3. System queries table statistics (cardinality, existing indexes) from `information_schema`/`pg_stats`.
4. System computes the optimal column order for a composite index, ranking by selectivity (most selective column first).
5. System checks whether a semantically equivalent index already exists on the table; none is found.
6. System generates a `CREATE INDEX` statement along with an estimated performance improvement, based on projected row-scan reduction.
7. System stores the recommendation with status "Pending Review," linked to the source query.
8. System notifies the DBA via a dashboard badge.
9. DBA reviews the recommendation and marks it "Approved" or "Rejected."

**Alternate Flow — Equivalent Index Already Exists** *(branches at step 5)*
5a. System finds an existing index that already covers the filter columns (possibly in a different column order, or as a superset).
5b. System marks the query as "No New Index Needed" and instead flags it as a candidate for query rewrite (e.g. the existing composite index has the wrong column order, or the query filters on a low-selectivity column first).
5c. System logs the finding for inclusion in the weekly digest, without creating a `CREATE INDEX` recommendation.
5d. Use case ends at the postcondition variant: "Query flagged for rewrite; no index recommendation created."