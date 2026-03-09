#!/usr/bin/env python3
"""
Auto Quality Loop — SideGuy Solutions
====================================
Runs quality scoring and freshness checks after each build.
Links new pages into authority hubs and clusters.
"""
import os
os.system('python3 tools/quality-loop/page_scorer.py || true')
os.system('python3 tools/freshness-engine/freshness_upgrader.py || true')
os.system('python3 tools/topic-cluster-engine/topic_cluster_builder.py || true')
os.system('python3 tools/topic-cluster-engine/semantic_link_injector.py || true')
os.system('python3 tools/hub-engine/build_hubs.py || true')
os.system('python3 tools/hub-engine/add_hubs_to_sitemap.py || true')
print("Auto quality loop complete.")
