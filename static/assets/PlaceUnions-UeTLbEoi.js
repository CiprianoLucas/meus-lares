import{d as b,r as d,f,e as u,c as l,a as e,b as y,v as k,t as m,i as g,F as x,m as U,l as E,o as s}from"./index-CEv88vVO.js";import{_ as C}from"./_plugin-vue_export-helper-DlAUqK2U.js";const $={class:"container mt-5"},N={class:"input-group mb-3"},V=["disabled"],B={key:0,class:"alert alert-danger text-center"},D={key:1,class:"alert alert-info text-center"},M={key:2},S={class:"table table-striped"},w=["onClick"],A=b({__name:"PlaceUnions",setup(F){const n=d([]),i=d(""),r=d(""),v=E(),c=d(v.params.id);f(()=>{p()});function p(){u.get(`/place/${c.value}/unions/`).then(t=>{n.value=t.data}).catch(t=>{console.error("Erro ao obter a lista de síndicos:",t)})}function _(t){u.delete(`/place/${c.value}/unions/${t}`).then(()=>{n.value=n.value.filter(o=>o.id!==t)}).catch(o=>{console.error("Erro ao deletar o síndico:",o)})}function h(){u.post(`/place/${c.value}/unions/`,{email:i.value}).then(t=>{n.value.push(t.data),i.value="",r.value=""}).catch(t=>{console.error("Erro ao adicionar o síndico:",t),r.value="Não foi possível adicionar o síndico. Verifique o email e tente novamente."})}return(t,o)=>(s(),l("div",$,[o[2]||(o[2]=e("h1",{class:"text-center"},"Síndicos",-1)),e("div",N,[y(e("input",{type:"email",class:"form-control","onUpdate:modelValue":o[0]||(o[0]=a=>i.value=a),placeholder:"Digite o email do síndico","aria-label":"Email do Síndico","aria-describedby":"button-addon2"},null,512),[[k,i.value]]),e("button",{class:"btn btn-primary",type:"button",id:"button-addon2",onClick:h,disabled:!i.value}," Adicionar ",8,V)]),r.value?(s(),l("div",B,m(r.value),1)):g("",!0),n.value.length===0?(s(),l("div",D," Nenhum síndico encontrado. ")):(s(),l("div",M,[e("table",S,[o[1]||(o[1]=e("thead",null,[e("tr",null,[e("th",null,"Username"),e("th",null,"Email"),e("th",null,"Ação")])],-1)),e("tbody",null,[(s(!0),l(x,null,U(n.value,a=>(s(),l("tr",{key:a.id},[e("td",null,m(a.username),1),e("td",null,m(a.email),1),e("td",null,[e("a",{onClick:P=>_(a.id)},"excluir",8,w)])]))),128))])])]))]))}}),L=C(A,[["__scopeId","data-v-4d363924"]]);export{L as default};
