import os
import glob

pages = len(glob.glob("*.html"))

operators = 0
affiliates = 0

if os.path.exists("data/operators"):
    operators = len(os.listdir("data/operators"))

if os.path.exists("docs/monetization/affiliate-programs.tsv"):
    affiliates = sum(1 for line in open("docs/monetization/affiliate-programs.tsv"))

print("")
print("SIDEGUY MONETIZATION STATUS")
print("---------------------------")
print("Pages:", pages)
print("Operators:", operators)
print("Affiliate Programs:", affiliates)
print("")
print("Primary Revenue Streams Ready:")
print("1 Resolution Consulting")
print("2 Lead Brokerage")
print("3 Payment Processing")
print("4 AI Automation Services")
print("5 Affiliate Programs")
print("")
