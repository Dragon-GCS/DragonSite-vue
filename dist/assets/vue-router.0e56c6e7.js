import{E as mt,u as Y,d as N,a2 as Ve,l as q,af as gt,F as vt,z as ze,a7 as Ge,p as fe,r as yt,w as We,n as Et,e as Fe}from"./@vue.fb846be3.js";/*!
  * vue-router v4.1.0
  * (c) 2022 Eduardo San Martin Morote
  * @license MIT
  */const j=typeof window!="undefined";function wt(e){return e.__esModule||e[Symbol.toStringTag]==="Module"}const k=Object.assign;function he(e,t){const n={};for(const r in t){const a=t[r];n[r]=I(a)?a.map(e):e(a)}return n}const X=()=>{},I=Array.isArray;function _(e){const t=Array.from(arguments).slice(1);console.warn.apply(console,["[Vue Router warn]: "+e].concat(t))}const Rt=/\/$/,_t=e=>e.replace(Rt,"");function de(e,t,n="/"){let r,a={},l="",h="";const d=t.indexOf("#");let u=t.indexOf("?");return d<u&&d>=0&&(u=-1),u>-1&&(r=t.slice(0,u),l=t.slice(u+1,d>-1?d:t.length),a=e(l)),d>-1&&(r=r||t.slice(0,d),h=t.slice(d,t.length)),r=kt(r!=null?r:t,n),{fullPath:r+(l&&"?")+l+h,path:r,query:a,hash:h}}function bt(e,t){const n=t.query?e(t.query):"";return t.path+(n&&"?")+n+(t.hash||"")}function $e(e,t){return!t||!e.toLowerCase().startsWith(t.toLowerCase())?e:e.slice(t.length)||"/"}function Ae(e,t,n){const r=t.matched.length-1,a=n.matched.length-1;return r>-1&&r===a&&U(t.matched[r],n.matched[a])&&Qe(t.params,n.params)&&e(t.query)===e(n.query)&&t.hash===n.hash}function U(e,t){return(e.aliasOf||e)===(t.aliasOf||t)}function Qe(e,t){if(Object.keys(e).length!==Object.keys(t).length)return!1;for(const n in e)if(!Pt(e[n],t[n]))return!1;return!0}function Pt(e,t){return I(e)?xe(e,t):I(t)?xe(t,e):e===t}function xe(e,t){return I(t)?e.length===t.length&&e.every((n,r)=>n===t[r]):e.length===1&&e[0]===t}function kt(e,t){if(e.startsWith("/"))return e;if(!t.startsWith("/"))return _(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`),e;if(!e)return t;const n=t.split("/"),r=e.split("/");let a=n.length-1,l,h;for(l=0;l<r.length;l++)if(h=r[l],h!==".")if(h==="..")a>1&&a--;else break;return n.slice(0,a).join("/")+"/"+r.slice(l-(l===r.length?1:0)).join("/")}var Z;(function(e){e.pop="pop",e.push="push"})(Z||(Z={}));var J;(function(e){e.back="back",e.forward="forward",e.unknown=""})(J||(J={}));function St(e){if(!e)if(j){const t=document.querySelector("base");e=t&&t.getAttribute("href")||"/",e=e.replace(/^\w+:\/\/[^\/]+/,"")}else e="/";return e[0]!=="/"&&e[0]!=="#"&&(e="/"+e),_t(e)}const Ct=/^[^#]+#/;function $t(e,t){return e.replace(Ct,"#")+t}function At(e,t){const n=document.documentElement.getBoundingClientRect(),r=e.getBoundingClientRect();return{behavior:t.behavior,left:r.left-n.left-(t.left||0),top:r.top-n.top-(t.top||0)}}const re=()=>({left:window.pageXOffset,top:window.pageYOffset});function xt(e){let t;if("el"in e){const n=e.el,r=typeof n=="string"&&n.startsWith("#");if(typeof e.el=="string"&&(!r||!document.getElementById(e.el.slice(1))))try{const l=document.querySelector(e.el);if(r&&l){_(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);return}}catch{_(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);return}const a=typeof n=="string"?r?document.getElementById(n.slice(1)):document.querySelector(n):n;if(!a){_(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);return}t=At(a,e)}else t=e;"scrollBehavior"in document.documentElement.style?window.scrollTo(t):window.scrollTo(t.left!=null?t.left:window.pageXOffset,t.top!=null?t.top:window.pageYOffset)}function Oe(e,t){return(history.state?history.state.position-t:-1)+e}const me=new Map;function Ot(e,t){me.set(e,t)}function It(e){const t=me.get(e);return me.delete(e),t}let Tt=()=>location.protocol+"//"+location.host;function Ye(e,t){const{pathname:n,search:r,hash:a}=t,l=e.indexOf("#");if(l>-1){let d=a.includes(e.slice(l))?e.slice(l).length:1,u=a.slice(d);return u[0]!=="/"&&(u="/"+u),$e(u,"")}return $e(n,e)+r+a}function Nt(e,t,n,r){let a=[],l=[],h=null;const d=({state:c})=>{const m=Ye(e,location),y=n.value,$=t.value;let S=0;if(c){if(n.value=m,t.value=c,h&&h===y){h=null;return}S=$?c.position-$.position:0}else r(m);a.forEach(w=>{w(n.value,y,{delta:S,type:Z.pop,direction:S?S>0?J.forward:J.back:J.unknown})})};function u(){h=n.value}function f(c){a.push(c);const m=()=>{const y=a.indexOf(c);y>-1&&a.splice(y,1)};return l.push(m),m}function o(){const{history:c}=window;!c.state||c.replaceState(k({},c.state,{scroll:re()}),"")}function i(){for(const c of l)c();l=[],window.removeEventListener("popstate",d),window.removeEventListener("beforeunload",o)}return window.addEventListener("popstate",d),window.addEventListener("beforeunload",o),{pauseListeners:u,listen:f,destroy:i}}function Ie(e,t,n,r=!1,a=!1){return{back:e,current:t,forward:n,replaced:r,position:window.history.length,scroll:a?re():null}}function Mt(e){const{history:t,location:n}=window,r={value:Ye(e,n)},a={value:t.state};a.value||l(r.value,{back:null,current:r.value,forward:null,position:t.length-1,replaced:!0,scroll:null},!0);function l(u,f,o){const i=e.indexOf("#"),c=i>-1?(n.host&&document.querySelector("base")?e:e.slice(i))+u:Tt()+e+u;try{t[o?"replaceState":"pushState"](f,"",c),a.value=f}catch(m){_("Error with push/replace State",m),n[o?"replace":"assign"](c)}}function h(u,f){const o=k({},t.state,Ie(a.value.back,u,a.value.forward,!0),f,{position:a.value.position});l(u,o,!0),r.value=u}function d(u,f){const o=k({},a.value,t.state,{forward:u,scroll:re()});t.state||_(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://next.router.vuejs.org/guide/migration/#usage-of-history-state.`),l(o.current,o,!0);const i=k({},Ie(r.value,u,null),{position:o.position+1},f);l(u,i,!1),r.value=u}return{location:r,state:a,push:d,replace:h}}function Un(e){e=St(e);const t=Mt(e),n=Nt(e,t.state,t.location,t.replace);function r(l,h=!0){h||n.pauseListeners(),history.go(l)}const a=k({location:"",base:e,go:r,createHref:$t.bind(null,e)},t,n);return Object.defineProperty(a,"location",{enumerable:!0,get:()=>t.location.value}),Object.defineProperty(a,"state",{enumerable:!0,get:()=>t.state.value}),a}function jt(e){return typeof e=="string"||e&&typeof e=="object"}function Xe(e){return typeof e=="string"||typeof e=="symbol"}const B={path:"/",name:void 0,params:{},query:{},hash:"",fullPath:"/",matched:[],meta:{},redirectedFrom:void 0},Je=Symbol("navigation failure");var Te;(function(e){e[e.aborted=4]="aborted",e[e.cancelled=8]="cancelled",e[e.duplicated=16]="duplicated"})(Te||(Te={}));const Bt={[1]({location:e,currentLocation:t}){return`No match for
 ${JSON.stringify(e)}${t?`
while being at
`+JSON.stringify(t):""}`},[2]({from:e,to:t}){return`Redirected from "${e.fullPath}" to "${Lt(t)}" via a navigation guard.`},[4]({from:e,to:t}){return`Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`},[8]({from:e,to:t}){return`Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`},[16]({from:e,to:t}){return`Avoided redundant navigation to current location: "${e.fullPath}".`}};function z(e,t){return k(new Error(Bt[e](t)),{type:e,[Je]:!0},t)}function D(e,t){return e instanceof Error&&Je in e&&(t==null||!!(e.type&t))}const Dt=["params","query","hash"];function Lt(e){if(typeof e=="string")return e;if("path"in e)return e.path;const t={};for(const n of Dt)n in e&&(t[n]=e[n]);return JSON.stringify(t,null,2)}const Ne="[^/]+?",Ut={sensitive:!1,strict:!1,start:!0,end:!0},Ht=/[.+*?^${}()[\]/\\]/g;function Kt(e,t){const n=k({},Ut,t),r=[];let a=n.start?"^":"";const l=[];for(const f of e){const o=f.length?[]:[90];n.strict&&!f.length&&(a+="/");for(let i=0;i<f.length;i++){const c=f[i];let m=40+(n.sensitive?.25:0);if(c.type===0)i||(a+="/"),a+=c.value.replace(Ht,"\\$&"),m+=40;else if(c.type===1){const{value:y,repeatable:$,optional:S,regexp:w}=c;l.push({name:y,repeatable:$,optional:S});const b=w||Ne;if(b!==Ne){m+=10;try{new RegExp(`(${b})`)}catch(T){throw new Error(`Invalid custom RegExp for param "${y}" (${b}): `+T.message)}}let A=$?`((?:${b})(?:/(?:${b}))*)`:`(${b})`;i||(A=S&&f.length<2?`(?:/${A})`:"/"+A),S&&(A+="?"),a+=A,m+=20,S&&(m+=-8),$&&(m+=-20),b===".*"&&(m+=-50)}o.push(m)}r.push(o)}if(n.strict&&n.end){const f=r.length-1;r[f][r[f].length-1]+=.7000000000000001}n.strict||(a+="/?"),n.end?a+="$":n.strict&&(a+="(?:/|$)");const h=new RegExp(a,n.sensitive?"":"i");function d(f){const o=f.match(h),i={};if(!o)return null;for(let c=1;c<o.length;c++){const m=o[c]||"",y=l[c-1];i[y.name]=m&&y.repeatable?m.split("/"):m}return i}function u(f){let o="",i=!1;for(const c of e){(!i||!o.endsWith("/"))&&(o+="/"),i=!1;for(const m of c)if(m.type===0)o+=m.value;else if(m.type===1){const{value:y,repeatable:$,optional:S}=m,w=y in f?f[y]:"";if(I(w)&&!$)throw new Error(`Provided param "${y}" is an array but it is not repeatable (* or + modifiers)`);const b=I(w)?w.join("/"):w;if(!b)if(S)c.length<2&&e.length>1&&(o.endsWith("/")?o=o.slice(0,-1):i=!0);else throw new Error(`Missing required param "${y}"`);o+=b}}return o}return{re:h,score:r,keys:l,parse:d,stringify:u}}function qt(e,t){let n=0;for(;n<e.length&&n<t.length;){const r=t[n]-e[n];if(r)return r;n++}return e.length<t.length?e.length===1&&e[0]===40+40?-1:1:e.length>t.length?t.length===1&&t[0]===40+40?1:-1:0}function Vt(e,t){let n=0;const r=e.score,a=t.score;for(;n<r.length&&n<a.length;){const l=qt(r[n],a[n]);if(l)return l;n++}if(Math.abs(a.length-r.length)===1){if(Me(r))return 1;if(Me(a))return-1}return a.length-r.length}function Me(e){const t=e[e.length-1];return e.length>0&&t[t.length-1]<0}const zt={type:0,value:""},Gt=/[a-zA-Z0-9_]/;function Wt(e){if(!e)return[[]];if(e==="/")return[[zt]];if(!e.startsWith("/"))throw new Error(`Route paths should start with a "/": "${e}" should be "/${e}".`);function t(m){throw new Error(`ERR (${n})/"${f}": ${m}`)}let n=0,r=n;const a=[];let l;function h(){l&&a.push(l),l=[]}let d=0,u,f="",o="";function i(){!f||(n===0?l.push({type:0,value:f}):n===1||n===2||n===3?(l.length>1&&(u==="*"||u==="+")&&t(`A repeatable param (${f}) must be alone in its segment. eg: '/:ids+.`),l.push({type:1,value:f,regexp:o,repeatable:u==="*"||u==="+",optional:u==="*"||u==="?"})):t("Invalid state to consume buffer"),f="")}function c(){f+=u}for(;d<e.length;){if(u=e[d++],u==="\\"&&n!==2){r=n,n=4;continue}switch(n){case 0:u==="/"?(f&&i(),h()):u===":"?(i(),n=1):c();break;case 4:c(),n=r;break;case 1:u==="("?n=2:Gt.test(u)?c():(i(),n=0,u!=="*"&&u!=="?"&&u!=="+"&&d--);break;case 2:u===")"?o[o.length-1]=="\\"?o=o.slice(0,-1)+u:n=3:o+=u;break;case 3:i(),n=0,u!=="*"&&u!=="?"&&u!=="+"&&d--,o="";break;default:t("Unknown state");break}}return n===2&&t(`Unfinished custom RegExp for param "${f}"`),i(),h(),a}function Ft(e,t,n){const r=Kt(Wt(e.path),n);{const l=new Set;for(const h of r.keys)l.has(h.name)&&_(`Found duplicated params with name "${h.name}" for path "${e.path}". Only the last one will be available on "$route.params".`),l.add(h.name)}const a=k(r,{record:e,parent:t,children:[],alias:[]});return t&&!a.record.aliasOf==!t.record.aliasOf&&t.children.push(a),a}function Qt(e,t){const n=[],r=new Map;t=Be({strict:!1,end:!0,sensitive:!1},t);function a(o){return r.get(o)}function l(o,i,c){const m=!c,y=Xt(o);tn(y,i),y.aliasOf=c&&c.record;const $=Be(t,o),S=[y];if("alias"in o){const A=typeof o.alias=="string"?[o.alias]:o.alias;for(const T of A)S.push(k({},y,{components:c?c.record.components:y.components,path:T,aliasOf:c?c.record:y}))}let w,b;for(const A of S){const{path:T}=A;if(i&&T[0]!=="/"){const H=i.record.path,M=H[H.length-1]==="/"?"":"/";A.path=i.record.path+(T&&M+T)}if(A.path==="*")throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://next.router.vuejs.org/guide/migration/#removed-star-or-catch-all-routes.`);if(w=Ft(A,i,$),i&&T[0]==="/"&&nn(w,i),c?(c.alias.push(w),en(c,w)):(b=b||w,b!==w&&b.alias.push(w),m&&o.name&&!je(w)&&h(o.name)),"children"in y){const H=y.children;for(let M=0;M<H.length;M++)l(H[M],w,c&&c.children[M])}c=c||w,u(w)}return b?()=>{h(b)}:X}function h(o){if(Xe(o)){const i=r.get(o);i&&(r.delete(o),n.splice(n.indexOf(i),1),i.children.forEach(h),i.alias.forEach(h))}else{const i=n.indexOf(o);i>-1&&(n.splice(i,1),o.record.name&&r.delete(o.record.name),o.children.forEach(h),o.alias.forEach(h))}}function d(){return n}function u(o){let i=0;for(;i<n.length&&Vt(o,n[i])>=0&&(o.record.path!==n[i].record.path||!Ze(o,n[i]));)i++;n.splice(i,0,o),o.record.name&&!je(o)&&r.set(o.record.name,o)}function f(o,i){let c,m={},y,$;if("name"in o&&o.name){if(c=r.get(o.name),!c)throw z(1,{location:o});$=c.record.name,m=k(Yt(i.params,c.keys.filter(b=>!b.optional).map(b=>b.name)),o.params),y=c.stringify(m)}else if("path"in o)y=o.path,y.startsWith("/")||_(`The Matcher cannot resolve relative paths but received "${y}". Unless you directly called \`matcher.resolve("${y}")\`, this is probably a bug in vue-router. Please open an issue at https://new-issue.vuejs.org/?repo=vuejs/router.`),c=n.find(b=>b.re.test(y)),c&&(m=c.parse(y),$=c.record.name);else{if(c=i.name?r.get(i.name):n.find(b=>b.re.test(i.path)),!c)throw z(1,{location:o,currentLocation:i});$=c.record.name,m=k({},i.params,o.params),y=c.stringify(m)}const S=[];let w=c;for(;w;)S.unshift(w.record),w=w.parent;return{name:$,path:y,params:m,matched:S,meta:Zt(S)}}return e.forEach(o=>l(o)),{addRoute:l,resolve:f,removeRoute:h,getRoutes:d,getRecordMatcher:a}}function Yt(e,t){const n={};for(const r of t)r in e&&(n[r]=e[r]);return n}function Xt(e){return{path:e.path,redirect:e.redirect,name:e.name,meta:e.meta||{},aliasOf:void 0,beforeEnter:e.beforeEnter,props:Jt(e),children:e.children||[],instances:{},leaveGuards:new Set,updateGuards:new Set,enterCallbacks:{},components:"components"in e?e.components||null:e.component&&{default:e.component}}}function Jt(e){const t={},n=e.props||!1;if("component"in e)t.default=n;else for(const r in e.components)t[r]=typeof n=="boolean"?n:n[r];return t}function je(e){for(;e;){if(e.record.aliasOf)return!0;e=e.parent}return!1}function Zt(e){return e.reduce((t,n)=>k(t,n.meta),{})}function Be(e,t){const n={};for(const r in e)n[r]=r in t?t[r]:e[r];return n}function ge(e,t){return e.name===t.name&&e.optional===t.optional&&e.repeatable===t.repeatable}function en(e,t){for(const n of e.keys)if(!n.optional&&!t.keys.find(ge.bind(null,n)))return _(`Alias "${t.record.path}" and the original record: "${e.record.path}" should have the exact same param named "${n.name}"`);for(const n of t.keys)if(!n.optional&&!e.keys.find(ge.bind(null,n)))return _(`Alias "${t.record.path}" and the original record: "${e.record.path}" should have the exact same param named "${n.name}"`)}function tn(e,t){t&&t.record.name&&!e.name&&!e.path&&_(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`)}function nn(e,t){for(const n of t.keys)if(!e.keys.find(ge.bind(null,n)))return _(`Absolute path "${e.record.path}" should have the exact same param named "${n.name}" as its parent "${t.record.path}".`)}function Ze(e,t){return t.children.some(n=>n===e||Ze(e,n))}const et=/#/g,rn=/&/g,on=/\//g,an=/=/g,sn=/\?/g,tt=/\+/g,ln=/%5B/g,cn=/%5D/g,nt=/%5E/g,un=/%60/g,rt=/%7B/g,fn=/%7C/g,ot=/%7D/g,hn=/%20/g;function we(e){return encodeURI(""+e).replace(fn,"|").replace(ln,"[").replace(cn,"]")}function dn(e){return we(e).replace(rt,"{").replace(ot,"}").replace(nt,"^")}function ve(e){return we(e).replace(tt,"%2B").replace(hn,"+").replace(et,"%23").replace(rn,"%26").replace(un,"`").replace(rt,"{").replace(ot,"}").replace(nt,"^")}function pn(e){return ve(e).replace(an,"%3D")}function mn(e){return we(e).replace(et,"%23").replace(sn,"%3F")}function gn(e){return e==null?"":mn(e).replace(on,"%2F")}function ee(e){try{return decodeURIComponent(""+e)}catch{_(`Error decoding "${e}". Using original value`)}return""+e}function vn(e){const t={};if(e===""||e==="?")return t;const r=(e[0]==="?"?e.slice(1):e).split("&");for(let a=0;a<r.length;++a){const l=r[a].replace(tt," "),h=l.indexOf("="),d=ee(h<0?l:l.slice(0,h)),u=h<0?null:ee(l.slice(h+1));if(d in t){let f=t[d];I(f)||(f=t[d]=[f]),f.push(u)}else t[d]=u}return t}function De(e){let t="";for(let n in e){const r=e[n];if(n=pn(n),r==null){r!==void 0&&(t+=(t.length?"&":"")+n);continue}(I(r)?r.map(l=>l&&ve(l)):[r&&ve(r)]).forEach(l=>{l!==void 0&&(t+=(t.length?"&":"")+n,l!=null&&(t+="="+l))})}return t}function yn(e){const t={};for(const n in e){const r=e[n];r!==void 0&&(t[n]=I(r)?r.map(a=>a==null?null:""+a):r==null?r:""+r)}return t}const En=Symbol("router view location matched"),Le=Symbol("router view depth"),oe=Symbol("router"),Re=Symbol("route location"),ye=Symbol("router view location");function F(){let e=[];function t(r){return e.push(r),()=>{const a=e.indexOf(r);a>-1&&e.splice(a,1)}}function n(){e=[]}return{add:t,list:()=>e,reset:n}}function L(e,t,n,r,a){const l=r&&(r.enterCallbacks[a]=r.enterCallbacks[a]||[]);return()=>new Promise((h,d)=>{const u=i=>{i===!1?d(z(4,{from:n,to:t})):i instanceof Error?d(i):jt(i)?d(z(2,{from:t,to:i})):(l&&r.enterCallbacks[a]===l&&typeof i=="function"&&l.push(i),h())},f=e.call(r&&r.instances[a],t,n,wn(u,t,n));let o=Promise.resolve(f);if(e.length<3&&(o=o.then(u)),e.length>2){const i=`The "next" callback was never called inside of ${e.name?'"'+e.name+'"':""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;if(typeof f=="object"&&"then"in f)o=o.then(c=>u._called?c:(_(i),Promise.reject(new Error("Invalid navigation guard"))));else if(f!==void 0&&!u._called){_(i),d(new Error("Invalid navigation guard"));return}}o.catch(i=>d(i))})}function wn(e,t,n){let r=0;return function(){r++===1&&_(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`),e._called=!0,r===1&&e.apply(null,arguments)}}function pe(e,t,n,r){const a=[];for(const l of e){!l.components&&!l.children.length&&_(`Record with path "${l.path}" is either missing a "component(s)" or "children" property.`);for(const h in l.components){let d=l.components[h];{if(!d||typeof d!="object"&&typeof d!="function")throw _(`Component "${h}" in record with path "${l.path}" is not a valid component. Received "${String(d)}".`),new Error("Invalid route component");if("then"in d){_(`Component "${h}" in record with path "${l.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);const u=d;d=()=>u}else d.__asyncLoader&&!d.__warnedDefineAsync&&(d.__warnedDefineAsync=!0,_(`Component "${h}" in record with path "${l.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`))}if(!(t!=="beforeRouteEnter"&&!l.instances[h]))if(Rn(d)){const f=(d.__vccOpts||d)[t];f&&a.push(L(f,n,r,l,h))}else{let u=d();"catch"in u||(_(`Component "${h}" in record with path "${l.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`),u=Promise.resolve(u)),a.push(()=>u.then(f=>{if(!f)return Promise.reject(new Error(`Couldn't resolve component "${h}" at "${l.path}"`));const o=wt(f)?f.default:f;l.components[h]=o;const c=(o.__vccOpts||o)[t];return c&&L(c,n,r,l,h)()}))}}}return a}function Rn(e){return typeof e=="object"||"displayName"in e||"props"in e||"__vccOpts"in e}function Ue(e){const t=q(oe),n=q(Re),r=N(()=>t.resolve(Y(e.to))),a=N(()=>{const{matched:u}=r.value,{length:f}=u,o=u[f-1],i=n.matched;if(!o||!i.length)return-1;const c=i.findIndex(U.bind(null,o));if(c>-1)return c;const m=He(u[f-2]);return f>1&&He(o)===m&&i[i.length-1].path!==m?i.findIndex(U.bind(null,u[f-2])):c}),l=N(()=>a.value>-1&&kn(n.params,r.value.params)),h=N(()=>a.value>-1&&a.value===n.matched.length-1&&Qe(n.params,r.value.params));function d(u={}){return Pn(u)?t[Y(e.replace)?"replace":"push"](Y(e.to)).catch(X):Promise.resolve()}if(j){const u=Fe();if(u){const f={route:r.value,isActive:l.value,isExactActive:h.value};u.__vrl_devtools=u.__vrl_devtools||[],u.__vrl_devtools.push(f),Et(()=>{f.route=r.value,f.isActive=l.value,f.isExactActive=h.value},{flush:"post"})}}return{route:r,href:N(()=>r.value.href),isActive:l,isExactActive:h,navigate:d}}const _n=ze({name:"RouterLink",compatConfig:{MODE:3},props:{to:{type:[String,Object],required:!0},replace:Boolean,activeClass:String,exactActiveClass:String,custom:Boolean,ariaCurrentValue:{type:String,default:"page"}},useLink:Ue,setup(e,{slots:t}){const n=Ve(Ue(e)),{options:r}=q(oe),a=N(()=>({[Ke(e.activeClass,r.linkActiveClass,"router-link-active")]:n.isActive,[Ke(e.exactActiveClass,r.linkExactActiveClass,"router-link-exact-active")]:n.isExactActive}));return()=>{const l=t.default&&t.default(n);return e.custom?l:Ge("a",{"aria-current":n.isExactActive?e.ariaCurrentValue:null,href:n.href,onClick:n.navigate,class:a.value},l)}}}),bn=_n;function Pn(e){if(!(e.metaKey||e.altKey||e.ctrlKey||e.shiftKey)&&!e.defaultPrevented&&!(e.button!==void 0&&e.button!==0)){if(e.currentTarget&&e.currentTarget.getAttribute){const t=e.currentTarget.getAttribute("target");if(/\b_blank\b/i.test(t))return}return e.preventDefault&&e.preventDefault(),!0}}function kn(e,t){for(const n in t){const r=t[n],a=e[n];if(typeof r=="string"){if(r!==a)return!1}else if(!I(a)||a.length!==r.length||r.some((l,h)=>l!==a[h]))return!1}return!0}function He(e){return e?e.aliasOf?e.aliasOf.path:e.path:""}const Ke=(e,t,n)=>e!=null?e:t!=null?t:n,Sn=ze({name:"RouterView",inheritAttrs:!1,props:{name:{type:String,default:"default"},route:Object},compatConfig:{MODE:3},setup(e,{attrs:t,slots:n}){$n();const r=q(ye),a=N(()=>e.route||r.value),l=q(Le,0),h=N(()=>{let f=Y(l);const{matched:o}=a.value;let i;for(;(i=o[f])&&!i.components;)f++;return f}),d=N(()=>a.value.matched[h.value]);fe(Le,N(()=>h.value+1)),fe(En,d),fe(ye,a);const u=yt();return We(()=>[u.value,d.value,e.name],([f,o,i],[c,m,y])=>{o&&(o.instances[i]=f,m&&m!==o&&f&&f===c&&(o.leaveGuards.size||(o.leaveGuards=m.leaveGuards),o.updateGuards.size||(o.updateGuards=m.updateGuards))),f&&o&&(!m||!U(o,m)||!c)&&(o.enterCallbacks[i]||[]).forEach($=>$(f))},{flush:"post"}),()=>{const f=a.value,o=d.value,i=o&&o.components[e.name],c=e.name;if(!i)return qe(n.default,{Component:i,route:f});const m=o.props[e.name],y=m?m===!0?f.params:typeof m=="function"?m(f):m:null,S=Ge(i,k({},y,t,{onVnodeUnmounted:w=>{w.component.isUnmounted&&(o.instances[c]=null)},ref:u}));if(j&&S.ref){const w={depth:h.value,name:o.name,path:o.path,meta:o.meta};(I(S.ref)?S.ref.map(A=>A.i):[S.ref.i]).forEach(A=>{A.__vrv_devtools=w})}return qe(n.default,{Component:S,route:f})||S}}});function qe(e,t){if(!e)return null;const n=e(t);return n.length===1?n[0]:n}const Cn=Sn;function $n(){const e=Fe(),t=e.parent&&e.parent.type.name;if(t&&(t==="KeepAlive"||t.includes("Transition"))){const n=t==="KeepAlive"?"keep-alive":"transition";_(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${n}>
    <component :is="Component" />
  </${n}>
</router-view>`)}}function Q(e,t){const n=k({},e,{matched:e.matched.map(r=>Bn(r,["instances","children","aliasOf"]))});return{_custom:{type:null,readOnly:!0,display:e.fullPath,tooltip:t,value:n}}}function ne(e){return{_custom:{display:e}}}let An=0;function xn(e,t,n){if(t.__hasDevtools)return;t.__hasDevtools=!0;const r=An++;gt({id:"org.vuejs.router"+(r?"."+r:""),label:"Vue Router",packageName:"vue-router",homepage:"https://router.vuejs.org",logo:"https://router.vuejs.org/logo.png",componentStateTypes:["Routing"],app:e},a=>{typeof a.now!="function"&&console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."),a.on.inspectComponent((o,i)=>{o.instanceData&&o.instanceData.state.push({type:"Routing",key:"$route",editable:!1,value:Q(t.currentRoute.value,"Current Route")})}),a.on.visitComponentTree(({treeNode:o,componentInstance:i})=>{if(i.__vrv_devtools){const c=i.__vrv_devtools;o.tags.push({label:(c.name?`${c.name.toString()}: `:"")+c.path,textColor:0,tooltip:"This component is rendered by &lt;router-view&gt;",backgroundColor:at})}I(i.__vrl_devtools)&&(i.__devtoolsApi=a,i.__vrl_devtools.forEach(c=>{let m=lt,y="";c.isExactActive?(m=it,y="This is exactly active"):c.isActive&&(m=st,y="This link is active"),o.tags.push({label:c.route.path,textColor:0,tooltip:y,backgroundColor:m})}))}),We(t.currentRoute,()=>{u(),a.notifyComponentUpdate(),a.sendInspectorTree(d),a.sendInspectorState(d)});const l="router:navigations:"+r;a.addTimelineLayer({id:l,label:`Router${r?" "+r:""} Navigations`,color:4237508}),t.onError((o,i)=>{a.addTimelineEvent({layerId:l,event:{title:"Error during Navigation",subtitle:i.fullPath,logType:"error",time:a.now(),data:{error:o},groupId:i.meta.__navigationId}})});let h=0;t.beforeEach((o,i)=>{const c={guard:ne("beforeEach"),from:Q(i,"Current Location during this navigation"),to:Q(o,"Target location")};Object.defineProperty(o.meta,"__navigationId",{value:h++}),a.addTimelineEvent({layerId:l,event:{time:a.now(),title:"Start of navigation",subtitle:o.fullPath,data:c,groupId:o.meta.__navigationId}})}),t.afterEach((o,i,c)=>{const m={guard:ne("afterEach")};c?(m.failure={_custom:{type:Error,readOnly:!0,display:c?c.message:"",tooltip:"Navigation Failure",value:c}},m.status=ne("\u274C")):m.status=ne("\u2705"),m.from=Q(i,"Current Location during this navigation"),m.to=Q(o,"Target location"),a.addTimelineEvent({layerId:l,event:{title:"End of navigation",subtitle:o.fullPath,time:a.now(),data:m,logType:c?"warning":"default",groupId:o.meta.__navigationId}})});const d="router-inspector:"+r;a.addInspector({id:d,label:"Routes"+(r?" "+r:""),icon:"book",treeFilterPlaceholder:"Search routes"});function u(){if(!f)return;const o=f;let i=n.getRoutes().filter(c=>!c.parent);i.forEach(ft),o.filter&&(i=i.filter(c=>Ee(c,o.filter.toLowerCase()))),i.forEach(c=>ut(c,t.currentRoute.value)),o.rootNodes=i.map(ct)}let f;a.on.getInspectorTree(o=>{f=o,o.app===e&&o.inspectorId===d&&u()}),a.on.getInspectorState(o=>{if(o.app===e&&o.inspectorId===d){const c=n.getRoutes().find(m=>m.record.__vd_id===o.nodeId);c&&(o.state={options:In(c)})}}),a.sendInspectorTree(d),a.sendInspectorState(d)})}function On(e){return e.optional?e.repeatable?"*":"?":e.repeatable?"+":""}function In(e){const{record:t}=e,n=[{editable:!1,key:"path",value:t.path}];return t.name!=null&&n.push({editable:!1,key:"name",value:t.name}),n.push({editable:!1,key:"regexp",value:e.re}),e.keys.length&&n.push({editable:!1,key:"keys",value:{_custom:{type:null,readOnly:!0,display:e.keys.map(r=>`${r.name}${On(r)}`).join(" "),tooltip:"Param keys",value:e.keys}}}),t.redirect!=null&&n.push({editable:!1,key:"redirect",value:t.redirect}),e.alias.length&&n.push({editable:!1,key:"aliases",value:e.alias.map(r=>r.record.path)}),Object.keys(e.record.meta).length&&n.push({editable:!1,key:"meta",value:e.record.meta}),n.push({key:"score",editable:!1,value:{_custom:{type:null,readOnly:!0,display:e.score.map(r=>r.join(", ")).join(" | "),tooltip:"Score used to sort routes",value:e.score}}}),n}const at=15485081,st=2450411,it=8702998,Tn=2282478,lt=16486972,Nn=6710886;function ct(e){const t=[],{record:n}=e;n.name!=null&&t.push({label:String(n.name),textColor:0,backgroundColor:Tn}),n.aliasOf&&t.push({label:"alias",textColor:0,backgroundColor:lt}),e.__vd_match&&t.push({label:"matches",textColor:0,backgroundColor:at}),e.__vd_exactActive&&t.push({label:"exact",textColor:0,backgroundColor:it}),e.__vd_active&&t.push({label:"active",textColor:0,backgroundColor:st}),n.redirect&&t.push({label:typeof n.redirect=="string"?`redirect: ${n.redirect}`:"redirects",textColor:16777215,backgroundColor:Nn});let r=n.__vd_id;return r==null&&(r=String(Mn++),n.__vd_id=r),{id:r,label:n.path,tags:t,children:e.children.map(ct)}}let Mn=0;const jn=/^\/(.*)\/([a-z]*)$/;function ut(e,t){const n=t.matched.length&&U(t.matched[t.matched.length-1],e.record);e.__vd_exactActive=e.__vd_active=n,n||(e.__vd_active=t.matched.some(r=>U(r,e.record))),e.children.forEach(r=>ut(r,t))}function ft(e){e.__vd_match=!1,e.children.forEach(ft)}function Ee(e,t){const n=String(e.re).match(jn);if(e.__vd_match=!1,!n||n.length<3)return!1;if(new RegExp(n[1].replace(/\$$/,""),n[2]).test(t))return e.children.forEach(h=>Ee(h,t)),e.record.path!=="/"||t==="/"?(e.__vd_match=e.re.test(t),!0):!1;const a=e.record.path.toLowerCase(),l=ee(a);return!t.startsWith("/")&&(l.includes(t)||a.includes(t))||l.startsWith(t)||a.startsWith(t)||e.record.name&&String(e.record.name).includes(t)?!0:e.children.some(h=>Ee(h,t))}function Bn(e,t){const n={};for(const r in e)t.includes(r)||(n[r]=e[r]);return n}function Hn(e){const t=Qt(e.routes,e),n=e.parseQuery||vn,r=e.stringifyQuery||De,a=e.history;if(!a)throw new Error('Provide the "history" option when calling "createRouter()": https://next.router.vuejs.org/api/#history.');const l=F(),h=F(),d=F(),u=mt(B);let f=B;j&&e.scrollBehavior&&"scrollRestoration"in history&&(history.scrollRestoration="manual");const o=he.bind(null,s=>""+s),i=he.bind(null,gn),c=he.bind(null,ee);function m(s,g){let p,v;return Xe(s)?(p=t.getRecordMatcher(s),v=g):v=s,t.addRoute(v,p)}function y(s){const g=t.getRecordMatcher(s);g?t.removeRoute(g):_(`Cannot remove non-existent route "${String(s)}"`)}function $(){return t.getRoutes().map(s=>s.record)}function S(s){return!!t.getRecordMatcher(s)}function w(s,g){if(g=k({},g||u.value),typeof s=="string"){const E=de(n,s,g.path),C=t.resolve({path:E.path},g),K=a.createHref(E.fullPath);return K.startsWith("//")?_(`Location "${s}" resolved to "${K}". A resolved location cannot start with multiple slashes.`):C.matched.length||_(`No match found for location with path "${s}"`),k(E,C,{params:c(C.params),hash:ee(E.hash),redirectedFrom:void 0,href:K})}let p;if("path"in s)"params"in s&&!("name"in s)&&Object.keys(s.params).length&&_(`Path "${s.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`),p=k({},s,{path:de(n,s.path,g.path).path});else{const E=k({},s.params);for(const C in E)E[C]==null&&delete E[C];p=k({},s,{params:i(s.params)}),g.params=i(g.params)}const v=t.resolve(p,g),P=s.hash||"";P&&!P.startsWith("#")&&_(`A \`hash\` should always start with the character "#". Replace "${P}" with "#${P}".`),v.params=o(c(v.params));const x=bt(r,k({},s,{hash:dn(P),path:v.path})),R=a.createHref(x);return R.startsWith("//")?_(`Location "${s}" resolved to "${R}". A resolved location cannot start with multiple slashes.`):v.matched.length||_(`No match found for location with path "${"path"in s?s.path:s}"`),k({fullPath:x,hash:P,query:r===De?yn(s.query):s.query||{}},v,{redirectedFrom:void 0,href:R})}function b(s){return typeof s=="string"?de(n,s,u.value.path):k({},s)}function A(s,g){if(f!==s)return z(8,{from:g,to:s})}function T(s){return G(s)}function H(s){return T(k(b(s),{replace:!0}))}function M(s){const g=s.matched[s.matched.length-1];if(g&&g.redirect){const{redirect:p}=g;let v=typeof p=="function"?p(s):p;if(typeof v=="string"&&(v=v.includes("?")||v.includes("#")?v=b(v):{path:v},v.params={}),!("path"in v)&&!("name"in v))throw _(`Invalid redirect found:
${JSON.stringify(v,null,2)}
 when navigating to "${s.fullPath}". A redirect must contain a name or path. This will break in production.`),new Error("Invalid redirect");return k({query:s.query,hash:s.hash,params:"path"in v?{}:s.params},v)}}function G(s,g){const p=f=w(s),v=u.value,P=s.state,x=s.force,R=s.replace===!0,E=M(p);if(E)return G(k(b(E),{state:P,force:x,replace:R}),g||p);const C=p;C.redirectedFrom=g;let K;return!x&&Ae(r,v,p)&&(K=z(16,{to:C,from:v}),Se(v,v,!0,!1)),(K?Promise.resolve(K):_e(C,v)).catch(O=>D(O)?D(O,2)?O:ie(O):se(O,C,v)).then(O=>{if(O){if(D(O,2))return Ae(r,w(O.to),C)&&g&&(g._count=g._count?g._count+1:1)>10?(_(`Detected an infinite redirection in a navigation guard when going from "${v.fullPath}" to "${C.fullPath}". Aborting to avoid a Stack Overflow. This will break in production if not fixed.`),Promise.reject(new Error("Infinite redirect in navigation guard"))):G(k(b(O.to),{state:P,force:x,replace:R}),g||C)}else O=Pe(C,v,!0,R,P);return be(C,v,O),O})}function ht(s,g){const p=A(s,g);return p?Promise.reject(p):Promise.resolve()}function _e(s,g){let p;const[v,P,x]=Dn(s,g);p=pe(v.reverse(),"beforeRouteLeave",s,g);for(const E of v)E.leaveGuards.forEach(C=>{p.push(L(C,s,g))});const R=ht.bind(null,s,g);return p.push(R),V(p).then(()=>{p=[];for(const E of l.list())p.push(L(E,s,g));return p.push(R),V(p)}).then(()=>{p=pe(P,"beforeRouteUpdate",s,g);for(const E of P)E.updateGuards.forEach(C=>{p.push(L(C,s,g))});return p.push(R),V(p)}).then(()=>{p=[];for(const E of s.matched)if(E.beforeEnter&&!g.matched.includes(E))if(I(E.beforeEnter))for(const C of E.beforeEnter)p.push(L(C,s,g));else p.push(L(E.beforeEnter,s,g));return p.push(R),V(p)}).then(()=>(s.matched.forEach(E=>E.enterCallbacks={}),p=pe(x,"beforeRouteEnter",s,g),p.push(R),V(p))).then(()=>{p=[];for(const E of h.list())p.push(L(E,s,g));return p.push(R),V(p)}).catch(E=>D(E,8)?E:Promise.reject(E))}function be(s,g,p){for(const v of d.list())v(s,g,p)}function Pe(s,g,p,v,P){const x=A(s,g);if(x)return x;const R=g===B,E=j?history.state:{};p&&(v||R?a.replace(s.fullPath,k({scroll:R&&E&&E.scroll},P)):a.push(s.fullPath,P)),u.value=s,Se(s,g,p,R),ie()}let W;function dt(){W||(W=a.listen((s,g,p)=>{if(!Ce.listening)return;const v=w(s),P=M(v);if(P){G(k(P,{replace:!0}),v).catch(X);return}f=v;const x=u.value;j&&Ot(Oe(x.fullPath,p.delta),re()),_e(v,x).catch(R=>D(R,12)?R:D(R,2)?(G(R.to,v).then(E=>{D(E,20)&&!p.delta&&p.type===Z.pop&&a.go(-1,!1)}).catch(X),Promise.reject()):(p.delta&&a.go(-p.delta,!1),se(R,v,x))).then(R=>{R=R||Pe(v,x,!1),R&&(p.delta?a.go(-p.delta,!1):p.type===Z.pop&&D(R,20)&&a.go(-1,!1)),be(v,x,R)}).catch(X)}))}let ae=F(),ke=F(),te;function se(s,g,p){ie(s);const v=ke.list();return v.length?v.forEach(P=>P(s,g,p)):(_("uncaught error during route navigation:"),console.error(s)),Promise.reject(s)}function pt(){return te&&u.value!==B?Promise.resolve():new Promise((s,g)=>{ae.add([s,g])})}function ie(s){return te||(te=!s,dt(),ae.list().forEach(([g,p])=>s?p(s):g()),ae.reset()),s}function Se(s,g,p,v){const{scrollBehavior:P}=e;if(!j||!P)return Promise.resolve();const x=!p&&It(Oe(s.fullPath,0))||(v||!p)&&history.state&&history.state.scroll||null;return vt().then(()=>P(s,g,x)).then(R=>R&&xt(R)).catch(R=>se(R,s,g))}const le=s=>a.go(s);let ce;const ue=new Set,Ce={currentRoute:u,listening:!0,addRoute:m,removeRoute:y,hasRoute:S,getRoutes:$,resolve:w,options:e,push:T,replace:H,go:le,back:()=>le(-1),forward:()=>le(1),beforeEach:l.add,beforeResolve:h.add,afterEach:d.add,onError:ke.add,isReady:pt,install(s){const g=this;s.component("RouterLink",bn),s.component("RouterView",Cn),s.config.globalProperties.$router=g,Object.defineProperty(s.config.globalProperties,"$route",{enumerable:!0,get:()=>Y(u)}),j&&!ce&&u.value===B&&(ce=!0,T(a.location).catch(P=>{_("Unexpected error when starting the router:",P)}));const p={};for(const P in B)p[P]=N(()=>u.value[P]);s.provide(oe,g),s.provide(Re,Ve(p)),s.provide(ye,u);const v=s.unmount;ue.add(s),s.unmount=function(){ue.delete(s),ue.size<1&&(f=B,W&&W(),W=null,u.value=B,ce=!1,te=!1),v()},j&&xn(s,g,t)}};return Ce}function V(e){return e.reduce((t,n)=>t.then(()=>n()),Promise.resolve())}function Dn(e,t){const n=[],r=[],a=[],l=Math.max(t.matched.length,e.matched.length);for(let h=0;h<l;h++){const d=t.matched[h];d&&(e.matched.find(f=>U(f,d))?r.push(d):n.push(d));const u=e.matched[h];u&&(t.matched.find(f=>U(f,u))||a.push(u))}return[n,r,a]}function Kn(){return q(oe)}function qn(){return q(Re)}export{Un as a,qn as b,Hn as c,Kn as u};
