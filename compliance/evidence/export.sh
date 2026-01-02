#!/usr/bin/env bash

# Manual helper — run only when needed
# Creates an exportable zip for auditors

DATE=$(date +%Y%m%d)
zip -r "evidence-export-$DATE.zip" policies access security training notes
