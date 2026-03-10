# SideGuy Auto Hub Discovery

Purpose:

Automatically detect emerging topic clusters across the SideGuy site.

As the site grows to tens of thousands of pages,
new clusters naturally appear.

This system identifies those clusters so SideGuy
can create new knowledge hubs.

--------------------------------------------------

PROCESS

1. Scan all HTML files
2. Extract common keywords
3. Count occurrences
4. Identify strong clusters
5. Suggest new hubs

--------------------------------------------------

EXAMPLE

If many pages reference:

stablecoin payments

Then SideGuy should create:

stablecoin-payments-hub.html

--------------------------------------------------

RULE

A topic becomes a hub candidate when:

20+ pages reference the concept.
