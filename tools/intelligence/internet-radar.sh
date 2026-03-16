#!/usr/bin/env bash

STAMP=$(date "+%Y-%m-%d %H:%M:%S")

SIGNALS="data/signals/signal-database.txt"
OUT="internet-radar.html"

if [ ! -f "$SIGNALS" ]; then
echo "Signal database not found."
exit 0
fi


cat > "$OUT" <<HTML
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>SideGuy Internet Radar</title>

<style>

body{
font-family:Arial, sans-serif;
background:#0f172a;
color:white;
padding:40px;
}

h1{
color:#38bdf8;
}

h2{
color:#22c55e;
margin-top:40px;
}

.signal{
background:#1e293b;
padding:12px;
margin:8px 0;
border-radius:6px;
}

.footer{
margin-top:50px;
color:#94a3b8;
}

</style>

</head>

<body>

<h1>SideGuy Internet Radar</h1>

<p>Signals SideGuy is watching across AI, payments, robotics, energy, and infrastructure.</p>

<p>Generated: $STAMP</p>

<h2>Technology Signals</h2>

HTML


while read -r signal
do

echo "<div class=\"signal\">$signal</div>" >> "$OUT"

done < "$SIGNALS"


cat >> "$OUT" <<HTML

<div class="footer">

SideGuy monitors emerging technology infrastructure so operators and businesses can understand what is coming next.

</div>

</body>
</html>
HTML


echo
echo "Internet Radar page created:"
echo "$OUT"
