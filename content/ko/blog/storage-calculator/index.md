---
title: "CCTV 녹화 저장 용량 계산기"
date: 2026-03-29
description: "CCTV 카메라 채널 수, 해상도, 녹화 시간에 따른 저장 용량과 보관 기간을 자동으로 계산해 보세요. NVR/DVR 스토리지 설계에 유용한 무료 온라인 도구입니다."
isCJKLanguage: true
tags: ["CCTV", "NVR", "저장용량", "계산기", "보안"]
---

CCTV 시스템을 구축할 때 가장 자주 받는 질문 중 하나는 **"HDD 용량이 얼마나 필요한가요?"** 입니다.

카메라 수, 해상도, 녹화 시간에 따라 필요한 저장 공간이 크게 달라지므로, 아래 계산기로 간편하게 확인해 보세요.

---

<style>
.sc-wrap{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:720px;margin:0 auto}
.sc-tabs{display:flex;gap:0;margin-bottom:0}
.sc-tab{flex:1;padding:12px 0;text-align:center;cursor:pointer;font-weight:600;font-size:15px;border:2px solid #1a1a4e;background:#f0f0f8;color:#1a1a4e;transition:all .2s;user-select:none}
.sc-tab:first-child{border-radius:8px 0 0 0}
.sc-tab:last-child{border-radius:0 8px 0 0}
.sc-tab.active{background:linear-gradient(135deg,#1a1a4e,#4a3f8f);color:#fff;border-color:#1a1a4e}
.sc-body{border:2px solid #1a1a4e;border-top:none;border-radius:0 0 8px 8px;padding:24px;background:#fafaff}
.sc-row{display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap}
.sc-field{flex:1;min-width:200px}
.sc-field label{display:block;font-weight:600;font-size:13px;color:#1a1a4e;margin-bottom:6px}
.sc-field select,.sc-field input{width:100%;padding:10px 12px;border:1.5px solid #ccc;border-radius:6px;font-size:15px;background:#fff;box-sizing:border-box;transition:border-color .2s}
.sc-field select:focus,.sc-field input:focus{outline:none;border-color:#4a3f8f;box-shadow:0 0 0 3px rgba(74,63,143,0.15)}
.sc-custom-br{display:none;margin-top:8px}
.sc-custom-br.show{display:block}
.sc-results{margin-top:20px;display:flex;gap:12px;flex-wrap:wrap}
.sc-card{flex:1;min-width:140px;background:linear-gradient(135deg,#1a1a4e,#4a3f8f);color:#fff;border-radius:10px;padding:18px;text-align:center;box-shadow:0 4px 15px rgba(26,26,78,0.3)}
.sc-card .sc-val{font-size:28px;font-weight:700;margin:6px 0}
.sc-card .sc-lbl{font-size:12px;opacity:.85}
.sc-hdd{margin-top:12px;padding:14px;background:#eef;border-radius:8px;font-size:14px;color:#1a1a4e;line-height:1.6}
.sc-ref{margin-top:28px}
.sc-ref summary{font-weight:600;cursor:pointer;color:#1a1a4e;font-size:15px}
.sc-ref table{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}
.sc-ref th,.sc-ref td{padding:8px 12px;border:1px solid #ddd;text-align:center}
.sc-ref th{background:#1a1a4e;color:#fff}
.sc-ref tr:nth-child(even){background:#f4f4fa}
@media(max-width:600px){.sc-row{flex-direction:column;gap:10px}.sc-field{min-width:auto}.sc-results{flex-direction:column}.sc-card .sc-val{font-size:24px}.sc-body{padding:16px}}
</style>

<div class="sc-wrap" id="sc-app">
<div class="sc-tabs">
<div class="sc-tab active" onclick="scMode(0)">📦 용량 → 저장 기간</div>
<div class="sc-tab" onclick="scMode(1)">📅 기간 → 필요 용량</div>
</div>
<div class="sc-body">

<div class="sc-row">
<div class="sc-field">
<label>카메라 채널 수</label>
<input type="number" id="sc-ch" value="4" min="1" max="256">
</div>
<div class="sc-field">
<label>해상도 / 품질</label>
<select id="sc-preset" onchange="scPreset()">
<option value="25">4K Ultra — 25 Mbps</option>
<option value="16">4K — 16 Mbps</option>
<option value="8">1080p High — 8 Mbps</option>
<option value="4" selected>1080p Standard — 4 Mbps</option>
<option value="2">720p — 2 Mbps</option>
<option value="custom">커스텀 (직접 입력)</option>
</select>
<input type="number" class="sc-custom-br" id="sc-br-custom" value="4" min="0.1" max="100" step="0.1" placeholder="Mbps 입력">
</div>
</div>

<div class="sc-row">
<div class="sc-field">
<label>프레임 레이트 (FPS)</label>
<input type="number" id="sc-fps" value="20" min="1" max="60">
<span style="font-size:12px;color:#666;">기본 20fps / 프리셋 기준 30fps</span>
</div>
</div>

<div class="sc-row">
<div class="sc-field">
<label>일일 녹화 시간</label>
<input type="number" id="sc-hours" value="24" min="1" max="24">
</div>
<div class="sc-field" id="sc-cap-field">
<label>총 저장 용량 (TB)</label>
<input type="number" id="sc-cap" value="4" min="0.1" step="0.1">
</div>
<div class="sc-field" id="sc-days-field" style="display:none">
<label>원하는 보관 기간 (일)</label>
<input type="number" id="sc-days" value="30" min="1" max="3650">
</div>
</div>

<div class="sc-results" id="sc-results"></div>
<div class="sc-hdd" id="sc-hdd" style="display:none"></div>
</div>

<details class="sc-ref">
<summary>📋 해상도별 비트레이트 참고 가이드</summary>
<table>
<tr><th>해상도</th><th>화질</th><th>비트레이트</th><th>1채널 일일 용량 (30fps)</th></tr>
<tr><td>4K (8MP)</td><td>Ultra</td><td>25 Mbps</td><td>~270 GB</td></tr>
<tr><td>4K (8MP)</td><td>Standard</td><td>16 Mbps</td><td>~173 GB</td></tr>
<tr><td>1080p (2MP)</td><td>High</td><td>8 Mbps</td><td>~86 GB</td></tr>
<tr><td>1080p (2MP)</td><td>Standard</td><td>4 Mbps</td><td>~43 GB</td></tr>
<tr><td>720p (1MP)</td><td>Standard</td><td>2 Mbps</td><td>~22 GB</td></tr>
</table>
<p style="font-size:13px;color:#666;margin-top:8px;">※ 실제 용량은 코덱(H.264/H.265), 장면 복잡도, 움직임 감지 설정 등에 따라 달라질 수 있습니다. H.265 사용 시 약 30~50% 절감됩니다.</p>
</details>
</div>

<script>
(function(){
var mode=0;
function $(id){return document.getElementById(id)}
function getBr(){
  var p=$('sc-preset');
  if(p.value==='custom')return parseFloat($('sc-br-custom').value)||4;
  return parseFloat(p.value);
}
function calc(){
  var ch=Math.max(1,Math.min(256,parseInt($('sc-ch').value)||1));
  var br=getBr();
  var hrs=Math.max(1,Math.min(24,parseInt($('sc-hours').value)||24));
  var fps=Math.max(1,Math.min(60,parseInt($('sc-fps').value)||20));
  var daily=br*(fps/30)*3600*hrs*ch/8/1000;
  var monthly=daily*30;
  var r=$('sc-results');
  var h=$('sc-hdd');
  if(mode===0){
    var cap=parseFloat($('sc-cap').value)||1;
    var days=cap*1000/daily;
    r.innerHTML=
      '<div class="sc-card"><div class="sc-lbl">예상 저장 기간</div><div class="sc-val">'+days.toFixed(1)+'일</div><div class="sc-lbl">≈ '+(days/30).toFixed(1)+'개월</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">일일 데이터량</div><div class="sc-val">'+daily.toFixed(1)+'</div><div class="sc-lbl">GB / 일</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">월간 데이터량</div><div class="sc-val">'+(monthly>=1000?(monthly/1000).toFixed(2)+' TB':monthly.toFixed(1)+' GB')+'</div><div class="sc-lbl">30일 기준</div></div>';
    h.style.display='none';
  }else{
    var d=Math.max(1,parseInt($('sc-days').value)||30);
    var need=daily*d/1000;
    r.innerHTML=
      '<div class="sc-card"><div class="sc-lbl">필요 저장 용량</div><div class="sc-val">'+need.toFixed(2)+'</div><div class="sc-lbl">TB</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">일일 데이터량</div><div class="sc-val">'+daily.toFixed(1)+'</div><div class="sc-lbl">GB / 일</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">총 데이터량</div><div class="sc-val">'+(daily*d>=1000?(daily*d/1000).toFixed(2)+' TB':(daily*d).toFixed(1)+' GB')+'</div><div class="sc-lbl">'+d+'일 기준</div></div>';
    var hddSizes=[2,4,6,8,10,12,14,16,18,20];
    var rec='';
    for(var i=0;i<hddSizes.length;i++){
      var s=hddSizes[i];
      var cnt=Math.ceil(need/s);
      if(cnt<=8){rec+='💾 '+s+'TB HDD × '+cnt+'개 = '+(s*cnt)+'TB';if(cnt>1)rec+=' (RAID 구성 가능)';rec+='<br>';if(cnt<=2)break;}
    }
    if(!rec)rec='💾 대용량 스토리지 또는 NAS 구성이 필요합니다.';
    h.innerHTML='<strong>💡 권장 HDD 구성:</strong><br>'+rec;
    h.style.display='block';
  }
}
window.scMode=function(m){
  mode=m;
  var tabs=document.querySelectorAll('#sc-app .sc-tab');
  tabs[0].className='sc-tab'+(m===0?' active':'');
  tabs[1].className='sc-tab'+(m===1?' active':'');
  $('sc-cap-field').style.display=m===0?'':'none';
  $('sc-days-field').style.display=m===1?'':'none';
  calc();
};
window.scPreset=function(){
  var c=$('sc-br-custom');
  c.className='sc-custom-br'+($('sc-preset').value==='custom'?' show':'');
  calc();
};
var inputs=document.querySelectorAll('#sc-app input, #sc-app select');
for(var i=0;i<inputs.length;i++)inputs[i].addEventListener('input',calc);
calc();
})();
</script>

---

## 활용 팁

- **H.265(HEVC)** 코덱 지원 NVR을 사용하면 동일 화질에서 저장 용량을 **30~50% 절감**할 수 있습니다.
- **움직임 감지 녹화**를 활용하면 실제 녹화량이 연속 녹화 대비 크게 줄어듭니다.
- 중요 채널은 고화질, 보조 채널은 저화질로 **혼합 구성**하면 비용을 최적화할 수 있습니다.
- 안정적인 운영을 위해 계산 결과보다 **10~20% 여유 용량**을 확보하는 것을 권장합니다.

궁금한 점이 있으시면 [문의하기](/about/)를 통해 연락해 주세요.
