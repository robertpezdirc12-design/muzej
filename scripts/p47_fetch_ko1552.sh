#!/bin/bash
# P47: prenos poligonov parcel KO 1552 (južni del, celica ch / list A05) iz GURS WFS.
# KO 1544 poligoni (parceles-0..4.json) so bili preneseni v P10 z istim virom;
# KO 1552 takrat ni bil potreben (P47 razširi overlay na celico ch).
# Prostorski omejitev: bbox celice ch eZKN + marža (EPSG:3794: 521090,43156–523387,45109).
# Datum prenosa: 2026-10-13; število: 1113 parcel (3 datoteke po 500/500/113).
mkdir -p research/georef-n83/gurs
URL="https://ipi.eprostor.gov.si/wfs-si-gurs-kn/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=SI.GURS.KN%3APARCELE&outputFormat=application/json&cql_filter=KO_ID%3D%271552%27%20AND%20BBOX(GEOM%2C521090%2C43156%2C523387%2C45109)"
P=0; I=0
while true; do
  curl -s -A "Mozilla/5.0" "${URL}&maxFeatures=500&startIndex=$P" --max-time 60 \
    -o research/georef-n83/gurs/parceles-ko1552-ch-$I.json
  GOT=$(python3 -c "import json; print(json.load(open('research/georef-n83/gurs/parceles-ko1552-ch-$I.json'))['numberReturned'])" 2>/dev/null || echo 0)
  echo "  stran $I (offset $P): $GOT"
  if [ "$GOT" = "0" ]; then rm -f research/georef-n83/gurs/parceles-ko1552-ch-$I.json; break; fi
  P=$((P+GOT)); I=$((I+1))
  if [ $I -ge 4 ]; then break; fi
done
echo "prenos končan: $P parcel v $I datotekah"
