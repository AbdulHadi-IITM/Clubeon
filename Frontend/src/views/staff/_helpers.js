export function today(){const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`}
export function time(v){if(!v)return '—';const [h,m='00']=String(v).split(':');const n=Number(h);return `${n%12||12}:${m} ${n>=12?'PM':'AM'}`}
export function date(v){if(!v)return '—';return new Intl.DateTimeFormat('en-IN',{day:'numeric',month:'short',year:'numeric'}).format(new Date(`${v}T00:00:00`))}
export function errorMessage(e,fallback='Something went wrong.'){return e?.response?.data?.message||e?.response?.data?.error||fallback}
export function list(data,key){if(Array.isArray(data))return data;if(Array.isArray(data?.[key]))return data[key];return []}
