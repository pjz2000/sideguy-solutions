Claude,

SideGuy now uses a Semantic Topic Lattice to scale toward 100k pages cleanly.

Read first:
- docs/lattice/semantic-topic-lattice.md

Then run in order:

1. tools/lattice/estimate-lattice-size.sh
2. tools/lattice/build-lattice-manifest.sh
3. tools/lattice/build-lattice-batch.sh 500

For each newly created page:
- improve the title so it is human-readable
- write a clean meta description
- add canonical
- add a real H1
- add intro copy
- add at least 3 structured sections
- add Text PJ orb
- add Back to Home link
- add sideguy-command-center.html link
- add most relevant knowledge hub link
- add at least 2 sibling page links from the same lattice family
- add a related guides block

Then:
- add the pages to sitemap.xml using the repo's current sitemap process
- append representative discovery links to index.html without clutter
- run health checks
- commit with:

Build: semantic topic lattice batch 001

Rules:
- append-only
- no mass rewrites
- no deleting content
- keep pages readable and useful
- follow the million-dollar-site-standard
- do not generate all pages at once; build in clean batches
