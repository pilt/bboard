
(function($){
/*************************************************
 * **  jQuery Masonry version 1.3.2
 * **  Copyright David DeSandro, licensed MIT
 * **  http://desandro.com/resources/jquery-masonry
 * **************************************************/
 (function(e){var n=e.event,o;n.special.smartresize={setup:function(){e(this).bind("resize",n.special.smartresize.handler)},teardown:function(){e(this).unbind("resize",n.special.smartresize.handler)},handler:function(j,l){var g=this,d=arguments;j.type="smartresize";o&&clearTimeout(o);o=setTimeout(function(){jQuery.event.handle.apply(g,d)},l==="execAsap"?0:100)}};e.fn.smartresize=function(j){return j?this.bind("smartresize",j):this.trigger("smartresize",["execAsap"])};e.fn.masonry=function(j,l){var g=
  {getBricks:function(d,b,a){var c=a.itemSelector===undefined;b.$bricks=a.appendedContent===undefined?c?d.children():d.find(a.itemSelector):c?a.appendedContent:a.appendedContent.filter(a.itemSelector)},placeBrick:function(d,b,a,c,h){b=Math.min.apply(Math,a);for(var i=b+d.outerHeight(true),f=a.length,k=f,m=c.colCount+1-f;f--;)if(a[f]==b)k=f;d.applyStyle({left:c.colW*k+c.posLeft,top:b},e.extend(true,{},h.animationOptions));for(f=0;f<m;f++)c.colY[k+f]=i},setup:function(d,b,a){g.getBricks(d,a,b);if(a.masoned)a.previousData=
  d.data("masonry");a.colW=b.columnWidth===undefined?a.masoned?a.previousData.colW:a.$bricks.outerWidth(true):b.columnWidth;a.colCount=Math.floor(d.width()/a.colW);a.colCount=Math.max(a.colCount,1)},arrange:function(d,b,a){var c;if(!a.masoned||b.appendedContent!==undefined)a.$bricks.css("position","absolute");if(a.masoned){a.posTop=a.previousData.posTop;a.posLeft=a.previousData.posLeft}else{d.css("position","relative");var h=e(document.createElement("div"));d.prepend(h);a.posTop=Math.round(h.position().top);
  a.posLeft=Math.round(h.position().left);h.remove()}if(a.masoned&&b.appendedContent!==undefined){a.colY=a.previousData.colY;for(c=a.previousData.colCount;c<a.colCount;c++)a.colY[c]=a.posTop}else{a.colY=[];for(c=a.colCount;c--;)a.colY.push(a.posTop)}e.fn.applyStyle=a.masoned&&b.animate?e.fn.animate:e.fn.css;b.singleMode?a.$bricks.each(function(){var i=e(this);g.placeBrick(i,a.colCount,a.colY,a,b)}):a.$bricks.each(function(){var i=e(this),f=Math.ceil(i.outerWidth(true)/a.colW);f=Math.min(f,a.colCount);
      if(f===1)g.placeBrick(i,a.colCount,a.colY,a,b);else{var k=a.colCount+1-f,m=[];for(c=0;c<k;c++){var p=a.colY.slice(c,c+f);m[c]=Math.max.apply(Math,p)}g.placeBrick(i,k,m,a,b)}});a.wallH=Math.max.apply(Math,a.colY);d.applyStyle({height:a.wallH-a.posTop},e.extend(true,[],b.animationOptions));a.masoned||setTimeout(function(){d.addClass("masoned")},1);l.call(a.$bricks);d.data("masonry",a)},resize:function(d,b,a){a.masoned=!!d.data("masonry");var c=d.data("masonry").colCount;g.setup(d,b,a);a.colCount!=c&&
  g.arrange(d,b,a)}};return this.each(function(){var d=e(this),b={};b.masoned=!!d.data("masonry");var a=b.masoned?d.data("masonry").options:{},c=e.extend({},e.fn.masonry.defaults,a,j),h=a.resizeable;b.options=c.saveOptions?c:a;l=l||function(){};g.getBricks(d,b,c);if(!b.$bricks.length)return this;g.setup(d,c,b);g.arrange(d,c,b);!h&&c.resizeable&&e(window).bind("smartresize.masonry",function(){g.resize(d,c,b)});h&&!c.resizeable&&e(window).unbind("smartresize.masonry")})};e.fn.masonry.defaults={singleMode:false,
  columnWidth:undefined,itemSelector:undefined,appendedContent:undefined,saveOptions:true,resizeable:true,animate:false,animationOptions:{}}})(jQuery);

jQuery.fn.highlight=function(b){function a(e,j){var l=0;if(e.nodeType==3){var k=e.data.toUpperCase().indexOf(j);if(k>=0){var h=document.createElement("span");h.className="highlight";var f=e.splitText(k);var c=f.splitText(j.length);var d=f.cloneNode(true);h.appendChild(d);f.parentNode.replaceChild(h,f);l=1}}else{if(e.nodeType==1&&e.childNodes&&!/(script|style)/i.test(e.tagName)){for(var g=0;g<e.childNodes.length;++g){g+=a(e.childNodes[g],j)}}}return l}return this.each(function(){a(this,b.toUpperCase())})};jQuery.fn.removeHighlight=function(){return this.find("span.highlight").each(function(){this.parentNode.firstChild.nodeName;with(this.parentNode){replaceChild(this.firstChild,this);normalize()}}).end()};


/*
jQuery Url Plugin
	* Version 1.0
	* 2009-03-22 19:30:05
	* URL: http://ajaxcssblog.com/jquery/url-read-get-variables/
	* Description: jQuery Url Plugin gives the ability to read GET parameters from the actual URL
	* Author: Matthias Jäggli
	* Copyright: Copyright (c) 2009 Matthias Jäggli 
	* Licence: dual, MIT/GPLv2
    *
    * Changed by me: use decodeURI instead of unescape.
*/
(function($){$.url={};$.extend($.url,{_params:{},init:function(){var paramsRaw="";try{paramsRaw=(document.location.href.split("?",2)[1]||"").split("#")[0].split("&")||[];for(var i=0;i<paramsRaw.length;i++){var single=paramsRaw[i].split("=");if(single[0])this._params[single[0]]=decodeURI(single[1]);}}catch(e){alert(e);}},param:function(name){return this._params[name]||"";},paramAll:function(){return this._params;}});$.url.init();})(jQuery);

})(this.jQuery);




window.log = function(){
  log.history = log.history || [];   
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};
(function(doc){
  var write = doc.write;
  doc.write = function(q){ 
    log('document.write(): ',arguments); 
    if (/docwriteregexwhitelist/.test(q)) write.apply(doc,arguments);  
  };
})(document);


