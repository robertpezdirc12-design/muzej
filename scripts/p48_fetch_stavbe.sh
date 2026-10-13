#!/bin/bash
# P48: prenos sodobnih stavb (obrisi tlorisov) iz GURS eZKN WFS za območje listov
# A02/A03/A04/A05 (celice cf/dg/cg/ch eZKN 1:2880). Vir: SI.GURS.KN:STAVBE,
# geometrijska lastnost OBRIS_GEOM (poligon tlorisa, EPSG:3794).
# KO 1544 GRIBLJE = 403 stavbe (vsi, celotna k.o.); KO 1552 = prenos v bboxu
# celice ch + marža (isti bbox kot P47 parceles-ko1552: 521090,43156–523387,45109).
# Datum prenosa: 2026-10-13.
mkdir -p research/georef-n83/gurs

URL1544="https://ipi.eprostor.gov.si/wfs-si-gurs-kn/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=SI.GURS.KN%3ASTAVBE&outputFormat=application/json&propertyNames=FEATUREID%2CEID_STAVBA%2CKO_ID%2CNAZIV%2CST_STAVBE%2CTIP_STAVBE_ID%2CTIPI_STAVB_NAZIV_SL%2CSTEVILO_ETAZ%2CBRUTO_TLORISNA_POVRSINA%2COBRIS_GEOM&cql_filter=KO_ID%3D%271544%27"
URL1552="https://ipi.eprostor.gov.si/wfs-si-gurs-kn/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=SI.GURS.KN%3ASTAVBE&outputFormat=application/json&propertyNames=FEATUREID%2CEID_STAVBA%2CKO_ID%2CNAZIV%2CST_STAVBE%2CTIP_STAVBE_ID%2CTIPI_STAVB_NAZIV_SL%2CSTEVILO_ETAZ%2CBRUTO_TLORISNA_POVRSINA%2COBRIS_GEOM&cql_filter=KO_ID%3D%271552%27%20AND%20BBOX(OBRIS_GEOM%2C520500%2C42600%2C524000%2C45700)"

fetch_paged () {
  local URL="$1" PREFIX="$2"
  local P=0 I=0
  while true; do
    curl -s -A "Mozilla/5.0" "${URL}&maxFeatures=500&startIndex=$P" --max-time 120 \
      -o research/georef-n83/gurs/${PREFIX}-$I.json
    GOT=$(python3 -c "import json; print(json.load(open('research/georef-n83/gurs/${PREFIX}-$I.json'))['numberReturned'])" 2>/dev/null || echo 0)
    echo "  ${PREFIX} stran $I (offset $P): $GOT"
    if [ "$GOT" = "0" ]; then rm -f research/georef-n83/gurs/${PREFIX}-$I.json; break; fi
    P=$((P+GOT)); I=$((I+1))
    if [ $I -ge 4 ]; then break; fi
  done
  echo "  ${PREFIX} končano: $P stavb v $I datotekah"
}

fetch_paged "$URL1544" "stavbe-ko1544"
fetch_paged "$URL1552" "stavbe-ko1552-south"
echo "prenos končan."
