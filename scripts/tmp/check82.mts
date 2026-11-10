import { HOUSE_VITALS } from "@/data/atlas/parish";
const b82 = HOUSE_VITALS.filter((h) => h.bookSignature === "04455" && h.year === 1882);
console.log("04455/1882 bloki:", b82.length);
b82.forEach((h) => console.log(" h" + h.houseNo, "s" + h.scan, "|", h.whatSi.slice(0, 80)));
console.log("04455 skupaj:", HOUSE_VITALS.filter((h) => h.bookSignature === "04455").length);
console.log("vsi:", HOUSE_VITALS.length);
