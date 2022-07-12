import{g as A,h as V,c as R,i as z,j,k as I,l as H,m as N,n as P}from"./element-plus.43cc11f7.js";import{z as M,r as w,Y as G,o as d,c as g,a as s,H as k,I as $,Q as l,O as t,a5 as h,S as f,u as m,K as q,a8 as C,M as D}from"./@vue.9a5f94f1.js";import{b as S,u as K}from"./vue-router.4b78d7a0.js";import"./@vueuse.443630ee.js";import"./lodash-es.dd08ea16.js";import"./async-validator.fb49d0f5.js";import"./@element-plus.15ddef21.js";import"./@ctrl.82a509e0.js";import"./@popperjs.36402333.js";const L={class:"check-box"},O=["src","alt"],Q=h("\u5220\u9664"),T=h("\u91CD\u547D\u540D"),U=M({__name:"Item",props:["data"],emits:["select"],setup(o,{emit:n}){const r=o,e=S(),i=w(!1),c=w(!1),b=()=>{c.value=!c.value,n("select",c.value,r.data.full_path)};return(a,u)=>{const _=A,E=G("router-link"),p=R,B=V,F=z;return d(),g("div",{class:"item-box",onMouseenter:u[1]||(u[1]=y=>i.value=!0),onMouseleave:u[2]||(u[2]=y=>i.value=!1)},[s("div",L,[k(l(_,{onChange:b},null,512),[[$,i.value||c.value]])]),l(E,{to:{name:"main",query:{path:o.data.full_path,logRequire:m(e).query.logRequire,filter:m(e).query.filter}}},{default:t(()=>[s("img",{src:`/assets/${o.data.type}.png`,alt:o.data.name,width:"64"},null,8,O),h(" "+f(o.data.name),1)]),_:1},8,["to"]),k(l(F,{style:{margin:"5px 0px"}},{default:t(()=>[l(B,{title:`\u786E\u8BA4\u5220\u9664${o.data.name}`},{reference:t(()=>[l(p,{type:"info",size:"small",onClick:u[0]||(u[0]=y=>i.value=!0)},{default:t(()=>[Q]),_:1})]),_:1},8,["title"]),l(p,{type:"info",size:"small"},{default:t(()=>[T]),_:1})]),_:1},512),[[$,i.value||c.value]])],32)}}});function Y(o){if(o=="/")return[["Home",o]];for(var n=[["Home",""]],r=o.split("/"),e=1;e<r.length;e++)n.push([r[e],n[e-1][1]+"/"+r[e]]);return n[0][1]="/",n}const x=[{name:"folder",type:"folder",full_path:"/folder"},{name:"image.jpg",type:"image",full_path:"/image.jpg"},{name:"file.txt",type:"file",full_path:"/file.txt"},{name:"video.mp4",type:"video",full_path:"/video.mp4"}];const Z=s("i",{class:"i-ic-baseline-file-upload",style:{"font-size":"20px"}},null,-1),J={style:{display:"flex","flex-wrap":"wrap"}},se=M({__name:"MainView",emits:["pointerenter","pointerleave"],setup(o){const n=S();K();const r=Y((n.query.path||"/").toString()),e=w([]),i=(a,u)=>{a?e.value.push(u):e.value=e.value.filter(_=>_!==u)},c=()=>{P.prompt("\u8BF7\u8F93\u5165\u6587\u4EF6\u5939\u540D\u79F0","\u65B0\u5EFA\u6587\u4EF6\u5939",{inputPattern:/^[a-zA-Z0-9_]+$/,inputErrorMessage:"\u6587\u4EF6\u5939\u540D\u79F0\u53EA\u80FD\u5305\u542B\u5B57\u6BCD\u3001\u6570\u5B57\u548C\u4E0B\u5212\u7EBF"}).then(async({value:a})=>{a&&(x.push({name:a,full_path:`${n.query.path}/${a}`,type:"folder"}),x.sort(),console.log(x))}).catch(()=>{console.log("\u53D6\u6D88")})},b=async()=>{console.log("Remove all files")};return(a,u)=>{const _=j,E=I,p=R,B=H,F=z,y=N;return d(),g(q,null,[l(y,{class:"func-bar"},{default:t(()=>[l(E,null,{default:t(()=>[(d(!0),g(q,null,C(m(r),v=>(d(),D(_,{to:{name:"main",query:{path:v[1],logRequire:a.$route.query.logRequire,filter:a.$route.query.filter}}},{default:t(()=>[h(f(v[0]),1)]),_:2},1032,["to"]))),256))]),_:1}),l(F,null,{default:t(()=>[l(p,{type:"primary"},{default:t(()=>[s("i",{class:"i-ic-outline-create-new-folder",style:{"font-size":"20px"},onClick:c})]),_:1}),k(l(p,{type:"primary"},{default:t(()=>[s("i",{class:"i-ph-trash-fill",style:{"font-size":"20px"},onClick:b})]),_:1},512),[[$,e.value.length!==0]]),l(p,{type:"primary"},{default:t(()=>[l(B,{style:{display:"flex"},action:"post_url",multiple:!0,data:{logRequire:a.$route.query.logRequire}},{default:t(()=>[Z]),_:1},8,["data"])]),_:1})]),_:1})]),_:1}),s("div",null,"querys: "+f(m(n).query),1),s("div",null,"full_path: "+f(m(n).fullPath),1),s("div",null,"select: "+f(e.value),1),s("div",J,[(d(!0),g(q,null,C(m(x),v=>(d(),D(U,{data:v,onSelect:i},null,8,["data"]))),256))])],64)}}});export{se as default};
