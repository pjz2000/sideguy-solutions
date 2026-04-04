
# SideGuy Retrieval Memory Layer v1



Purpose:

Create a lightweight repo-native retrieval layer that lets Claude reuse winning patterns

from existing pages, manifests, and docs before upgrading or generating new pages.



## Sources of memory

- docs/lattice/lattice-manifest.tsv

- docs/expansion/cluster-expansion.md

- docs/hubs/hub-architecture.md

- docs/gravity/content-gravity.md

- sitemap-index.xml

- top impression pages from GSC exports

- winning calculators / FAQ blocks

- local trust sections

- high-CTR hero sections

- best Text PJ orb implementations



## Retrieval loop

1. identify target page

2. extract page intent from URL + H1

3. find 5 nearest sibling pages by topic

4. extract strongest:

   - title patterns

   - intro blocks

   - FAQ blocks

   - calculator widgets

   - local trust cues

   - CTA placements

5. apply improvements to target page

6. log upgrade memory

