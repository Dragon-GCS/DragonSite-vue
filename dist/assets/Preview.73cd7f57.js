import{c as g}from"./element-plus.a0c6cafa.js";import{b as w,u as x}from"./vue-router.0e56c6e7.js";import{i as l,p as b,d as R}from"./index.b7be826d.js";import{z as q,r as k,o as n,c as s,u as t,a as y,S as j,Q as c,O as u,a5 as p}from"./@vue.fb846be3.js";import"./@vueuse.048c5a89.js";import"./lodash-es.dd08ea16.js";import"./async-validator.fb49d0f5.js";import"./@element-plus.2111aa6d.js";import"./@popperjs.36402333.js";import"./@ctrl.82a509e0.js";import"./axios.5bc38a7d.js";import"./qs.3fd877a9.js";import"./side-channel.70f74c3b.js";import"./get-intrinsic.89e72507.js";import"./has-symbols.caae0f97.js";import"./function-bind.cb3858f2.js";import"./has.c1051c46.js";import"./call-bind.b701f999.js";import"./object-inspect.186a03c9.js";const L={id:"content"},N=["src"],U=["src"],B={key:2},C={class:"controls"},F=p("Previous"),O=p("Download"),P=p("Next"),oe=q({__name:"Preview",setup(V){const o=w(),d=x(),e=Number.parseInt(o.query.idx),m=l.value[e].category,i=l.value;console.log(l,e);const r=k("");b(i[e].path,o.query.logRequire==="true").then(_=>{r.value=URL.createObjectURL(new Blob([_]))});const h=()=>{R(i[e].path,o.query.logRequire==="true")},v=()=>{e<=0||(d.push({name:"preview",query:{idx:e-1,logRequire:o.query.logRequire}}),window.URL.revokeObjectURL(r.value))},f=()=>{e>=i.length-1||(d.push({name:"preview",query:{idx:e+1,logRequire:o.query.logRequire}}),window.URL.revokeObjectURL(r.value))};return(_,D)=>{const a=g;return n(),s("div",L,[t(m)==="image"?(n(),s("img",{key:0,src:r.value,class:"content"},null,8,N)):t(m)==="video"?(n(),s("video",{key:1,src:r.value,controls:"",class:"content"},null,8,U)):(n(),s("div",B," Not support ")),y("h2",null,j(t(i)[t(e)].name),1),y("div",C,[c(a,{type:"primary",onClick:v,disabled:t(e)<=0},{default:u(()=>[F]),_:1},8,["disabled"]),c(a,{type:"primary",onClick:h},{default:u(()=>[O]),_:1}),c(a,{type:"primary",onClick:f,disabled:t(e)>=t(i).length-1},{default:u(()=>[P]),_:1},8,["disabled"])])])}}});export{oe as default};