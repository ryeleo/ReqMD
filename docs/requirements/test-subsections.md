# Test Subsections

Scope: testing H2 subsection parsing.

<!-- acceptance-status-summary:start -->
Summary: 2💡 0🔧 1✅ 0⚠️ 0⛔ 0🗑️
<!-- acceptance-status-summary:end -->

## Query API

This subsection covers read-only operations.


### RQMD-TEST-001: Simple query

- **Status:** ✅ Verified
- **Priority:** 🟢 P3 - Low
- Given a simple query
- When executed
- Then results are returned.


### RQMD-TEST-002: Complex query

- **Status:** 💡 Proposed
- **Priority:** 🟢 P3 - Low
- Given a complex query with joins
- When executed
- Then optimized results are returned.

## Mutation API

This subsection covers write operations.


### RQMD-TEST-003: Create operation

- **Status:** 💡 Proposed
- **Priority:** 🟢 P3 - Low
- Given valid input
- When create endpoint is called
- Then entity is persisted.
