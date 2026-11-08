#!/bin/bash
# P10: prenos vseh parcel k.o. Griblje (1544) iz GURS WFS (strani po 500)
mkdir -p research/georef-n83/gurs
URL="https://ipi.eprostor.gov.si/wfs-si-gurs-kn/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=SI.GURS.KN%3APARCELE&outputFormat=application/json&cql_filter=KO_ID%3D%271544%27"
# najprej števec
curl -s -A "Mozilla/5.0" "${URL}&maxFeatures=1" --max-time 40 -o /tmp/par-count.json
N=$(python3 -c "import json; print(json.load(open('/tmp/par-count.json'))['numberMatched'])")
echo "skupaj parcel: $N"
P=0; I=0
while [ $P -lt $N ]; do
  curl -s -A "Mozilla/5.0" "${URL}&maxFeatures=500&startIndex=$P" --max-time 60 -o research/georef-n83/gurs/parceles-$I.json
  GOT=$(python3 -c "import json; d=json.load(open('research/georef-n83/gurs/parceles-$I.json')); print(d['numberReturned'])" 2>/dev/null || echo 0)
  echo "  stran $I (offset $P): $GOT"
  if [ "$GOT" = "0" ]; then break; fi
  P=$((P+GOT)); I=$((I+1))
done
echo "prenos končan: $P parcel v $I datotekah"
