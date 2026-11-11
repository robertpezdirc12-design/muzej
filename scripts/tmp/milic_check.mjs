import { HOUSE_VITALS } from './src/data/atlas/parish.ts';
import { MILIC_FAMILY_RE, MILIC_FAMILY_TOTAL, MILIC_PER_BOOK } from './src/data/atlas/parish-forensics';
console.log('križ:', HOUSE_VITALS.filter(h => MILIC_FAMILY_RE.test(h.whatSi)).length);
console.log('MILIC_FAMILY_TOTAL:', MILIC_FAMILY_TOTAL);
console.log('PER_BOOK:', MILIC_PER_BOOK.map(b => `${b.book || b.sig}:${b.mentions}`).join(','));
