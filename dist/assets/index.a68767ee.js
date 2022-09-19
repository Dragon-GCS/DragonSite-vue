import{r as h,z as I,m as P,s as F,o as l,M as f,O as u,c as w,a8 as R,a as v,S as k,K as b,u as g,Q as _,a5 as N,Y as O,ag as D}from"./@vue.fb846be3.js";import{E as M,a as B,b as H,c as V,d as $,e as z,f as T,g as W}from"./element-plus.a0c6cafa.js";import{u as q,c as U,a as j}from"./vue-router.0e56c6e7.js";import{a as m}from"./axios.5bc38a7d.js";import{l as K}from"./qs.3fd877a9.js";import"./@vueuse.048c5a89.js";import"./lodash-es.dd08ea16.js";import"./async-validator.fb49d0f5.js";import"./@element-plus.2111aa6d.js";import"./@popperjs.36402333.js";import"./@ctrl.82a509e0.js";import"./side-channel.70f74c3b.js";import"./get-intrinsic.89e72507.js";import"./has-symbols.caae0f97.js";import"./function-bind.cb3858f2.js";import"./has.c1051c46.js";import"./call-bind.b701f999.js";import"./object-inspect.186a03c9.js";const Q=function(){const n=document.createElement("link").relList;if(n&&n.supports&&n.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))t(o);new MutationObserver(o=>{for(const a of o)if(a.type==="childList")for(const s of a.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&t(s)}).observe(document,{childList:!0,subtree:!0});function e(o){const a={};return o.integrity&&(a.integrity=o.integrity),o.referrerpolicy&&(a.referrerPolicy=o.referrerpolicy),o.crossorigin==="use-credentials"?a.credentials="include":o.crossorigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function t(o){if(o.ep)return;o.ep=!0;const a=e(o);fetch(o.href,a)}};Q();const c=r=>`https://api.iconify.design/${r}?color=currentColor`,Y=[{name:"\u516C\u5171\u7F51\u76D8",logRequire:"false",icon:c("fxemoji:harddisk.svg")},{name:"\u4E2A\u4EBA\u7F51\u76D8",logRequire:"true",icon:c("arcticons:password.svg")}],G=[{name:"\u5168\u90E8",icon:c("flat-color-icons:database.svg"),type:""},{name:"\u56FE\u7247",icon:c("vscode-icons:file-type-image.svg"),type:"image"},{name:"\u89C6\u9891",icon:c("vscode-icons:file-type-video.svg"),type:"video"},{name:"\u97F3\u9891",icon:c("vscode-icons:file-type-audio.svg"),type:"audio"},{name:"\u6587\u6863",icon:c("emojione-v1:document-with-text.svg"),type:"document"},{name:"\u6587\u672C",icon:c("vscode-icons:file-type-text.svg"),type:"text"},{name:"\u5176\u4ED6",icon:c("flat-color-icons:answers.svg"),type:"other"}],C="DragonSite",S=h(localStorage.getItem("username")||"");h(localStorage.getItem("token")||"");h(localStorage.getItem("expired_time")||"");const y=h(S.value!==""),Ie=["image","video","audio","document","text"],Re=h([]);const J=["src"],X=["src"],Z=I({__name:"SideMenu",setup(r){let n=h(document.body.clientWidth<768);return P(()=>{window.onresize=()=>{n.value=document.body.clientWidth<768}}),F(()=>{window.onresize=null}),(e,t)=>{const o=M,a=B,s=H;return l(),f(s,{collapse:g(n),"unique-opened":!0,router:!0,"default-active":"0-0"},{default:u(()=>[(l(!0),w(b,null,R(g(Y),(i,p)=>(l(),f(a,{index:`${p}`},{title:u(()=>[v("img",{width:"20",src:i.icon},null,8,J),v("span",null,k(i.name),1)]),default:u(()=>[(l(!0),w(b,null,R(g(G),(d,A)=>(l(),f(o,{index:`${p}-${A}`,route:{name:"main",query:{path:"/",logRequire:i.logRequire,filter:d.type}}},{default:u(()=>[v("img",{src:d.icon},null,8,X),v("span",null,k(d.name),1)]),_:2},1032,["index","route"]))),256))]),_:2},1032,["index"]))),256))]),_:1},8,["collapse"])}}}),x=()=>({token:localStorage.getItem("token")||"",username:localStorage.getItem("username")||"",expired_time:localStorage.getItem("expired_time")||0}),$e=async(r,n,e)=>m.get("/api/disk",{params:{path:r,login_require:n,category:e},headers:x()}).then(t=>t,t=>(console.log("err",t),t)),Ce=async(r,n,e,t)=>m.delete("/api/disk",{params:{path:r,login_require:t,name:n,is_dir:e},headers:x()}).then(o=>o).catch(o=>o),Le=async(r,n,e)=>m.post("/api/disk",{},{params:{path:r,name:n,login_require:e},headers:x()}).then(t=>t.data),qe=(r,n=!1)=>{window.open(`/api/disk/download?path=${r}&preview=false&login_require=${n}`,"_self")},Ae=(r,n=!1)=>m.get("/api/disk/download",{params:{path:r,preview:!0,login_require:n},headers:x(),responseType:"blob"}).then(e=>e.data),Pe=(r,n,e,t)=>m.patch("/api/disk",{},{params:{path:r,target:n,is_dir:e,login_require:t},headers:x()}).then(o=>o.data),Fe=(r,n)=>{const e=new URLSearchParams;return e.append("username",r),e.append("password",n),m.post("/api/auth/login",e).then(t=>{if(t.status===200)return localStorage.setItem("token",t.data.token),localStorage.setItem("username",t.data.username),localStorage.setItem("expired_time",t.data.expired_time),y.value=!0,S.value=t.data.username,!0})},ee=()=>{localStorage.removeItem("token"),localStorage.removeItem("username"),localStorage.removeItem("expired_time"),y.value=!1,S.value=""},te=N("\u767B\u5F55"),oe=I({__name:"Header",props:{siteName:String},emits:["pointerenter","pointerleave"],setup(r){const n=q(),e=()=>n.push({path:"/login"}),t=()=>n.push({path:"/"}),o=()=>{ee(),n.push({path:"/"})};return(a,s)=>{const i=V;return l(),w(b,null,[_(i,{onClick:t,link:!0},{default:u(()=>[v("h1",null,k(r.siteName),1)]),_:1}),g(y)?(l(),w("h1",{key:1,onClick:o,style:{cursor:"pointer"}},"Welcome "+k(g(S)),1)):(l(),f(i,{key:0,onClick:e,"auto-insert-space":""},{default:u(()=>[te]),_:1}))],64)}}});const ne=I({__name:"App",setup(r){document.title=C;const n=q();return m.defaults.paramsSerializer=e=>K.stringify(e,{indices:!1}),m.interceptors.response.use(e=>(console.log("response",e),e),e=>(e.response.status===401&&($.info(e.response.data.detail),y.value=!1,n.push({name:"login",query:{redirect:n.currentRoute.value.fullPath}})),e.response.status===400&&($.info(e.response.data.detail),y.value=!1),e.response.status===422&&console.log(e.response.data.detail),e)),(e,t)=>{const o=oe,a=z,s=Z,i=O("router-view"),p=T,d=W;return l(),f(d,null,{default:u(()=>[_(a,null,{default:u(()=>[_(o,{"site-name":g(C)},null,8,["site-name"])]),_:1}),_(d,null,{default:u(()=>[_(s),_(p,null,{default:u(()=>[(l(),f(i,{key:e.$route.fullPath}))]),_:1})]),_:1})]),_:1})}}}),re="modulepreload",L={},ae="./",E=function(n,e){return!e||e.length===0?n():Promise.all(e.map(t=>{if(t=`${ae}${t}`,t in L)return;L[t]=!0;const o=t.endsWith(".css"),a=o?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${t}"]${a}`))return;const s=document.createElement("link");if(s.rel=o?"stylesheet":re,o||(s.as="script",s.crossOrigin=""),s.href=t,document.head.appendChild(s),o)return new Promise((i,p)=>{s.addEventListener("load",i),s.addEventListener("error",()=>p(new Error(`Unable to preload CSS for ${t}`)))})})).then(()=>n())},se=[{path:"/",redirect:{name:"main",query:{path:"/",logRequire:"false"}}},{path:"/home",name:"main",component:()=>E(()=>import("./MainView.740f7d6b.js"),["assets/MainView.740f7d6b.js","assets/MainView.a8c7d486.css","assets/element-plus.a0c6cafa.js","assets/element-plus.dd0e05f1.css","assets/@vue.fb846be3.js","assets/@vueuse.048c5a89.js","assets/lodash-es.dd08ea16.js","assets/async-validator.fb49d0f5.js","assets/@element-plus.2111aa6d.js","assets/@popperjs.36402333.js","assets/@ctrl.82a509e0.js","assets/vue-router.0e56c6e7.js","assets/axios.5bc38a7d.js","assets/qs.3fd877a9.js","assets/side-channel.70f74c3b.js","assets/get-intrinsic.89e72507.js","assets/has-symbols.caae0f97.js","assets/function-bind.cb3858f2.js","assets/has.c1051c46.js","assets/call-bind.b701f999.js","assets/object-inspect.186a03c9.js"])},{path:"/login",name:"login",component:()=>E(()=>import("./Login.9703c2e4.js"),["assets/Login.9703c2e4.js","assets/Login.48399566.css","assets/element-plus.a0c6cafa.js","assets/element-plus.dd0e05f1.css","assets/@vue.fb846be3.js","assets/@vueuse.048c5a89.js","assets/lodash-es.dd08ea16.js","assets/async-validator.fb49d0f5.js","assets/@element-plus.2111aa6d.js","assets/@popperjs.36402333.js","assets/@ctrl.82a509e0.js","assets/vue-router.0e56c6e7.js","assets/axios.5bc38a7d.js","assets/qs.3fd877a9.js","assets/side-channel.70f74c3b.js","assets/get-intrinsic.89e72507.js","assets/has-symbols.caae0f97.js","assets/function-bind.cb3858f2.js","assets/has.c1051c46.js","assets/call-bind.b701f999.js","assets/object-inspect.186a03c9.js"])},{path:"/preview",name:"preview",component:()=>E(()=>import("./Preview.0423417c.js"),["assets/Preview.0423417c.js","assets/Preview.49472dc0.css","assets/element-plus.a0c6cafa.js","assets/element-plus.dd0e05f1.css","assets/@vue.fb846be3.js","assets/@vueuse.048c5a89.js","assets/lodash-es.dd08ea16.js","assets/async-validator.fb49d0f5.js","assets/@element-plus.2111aa6d.js","assets/@popperjs.36402333.js","assets/@ctrl.82a509e0.js","assets/vue-router.0e56c6e7.js","assets/axios.5bc38a7d.js","assets/qs.3fd877a9.js","assets/side-channel.70f74c3b.js","assets/get-intrinsic.89e72507.js","assets/has-symbols.caae0f97.js","assets/function-bind.cb3858f2.js","assets/has.c1051c46.js","assets/call-bind.b701f999.js","assets/object-inspect.186a03c9.js"])}],ie=U({history:j(),routes:se});D(ne).use(ie).mount("#app");export{Ie as a,Pe as b,Le as c,qe as d,Fe as e,x as g,Re as i,$e as l,Ae as p,Ce as r};