---
title: "CCTV Recording Storage Calculator"
date: 2026-03-29
description: "Calculate CCTV storage requirements based on camera channels, resolution, FPS, and recording hours. A free online tool for NVR/DVR storage planning."
tags: ["CCTV", "NVR", "Storage", "Calculator", "Security", "FPS"]
---

One of the most common questions when setting up a CCTV system is **"How much HDD storage do I need?"**

Storage requirements vary greatly depending on the number of cameras, resolution, and recording hours. Use the calculator below to quickly find out.

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

<div class="sc-wrap" id="sc-app-en">
<div class="sc-tabs">
<div class="sc-tab active" onclick="scModeEn(0)">📦 Storage → Duration</div>
<div class="sc-tab" onclick="scModeEn(1)">📅 Duration → Storage</div>
</div>
<div class="sc-body">

<div class="sc-row">
<div class="sc-field">
<label>Number of Cameras</label>
<input type="number" id="sc-ch-en" value="4" min="1" max="256">
</div>
<div class="sc-field">
<label>Resolution / Quality</label>
<select id="sc-preset-en" onchange="scPresetEn()">
<option value="25">4K Ultra — 25 Mbps</option>
<option value="16">4K — 16 Mbps</option>
<option value="8">1080p High — 8 Mbps</option>
<option value="4" selected>1080p Standard — 4 Mbps</option>
<option value="2">720p — 2 Mbps</option>
<option value="custom">Custom (enter manually)</option>
</select>
<input type="number" class="sc-custom-br" id="sc-br-custom-en" value="4" min="0.1" max="100" step="0.1" placeholder="Mbps">
</div>
</div>

<div class="sc-row">
<div class="sc-field">
<label>Frame Rate (FPS)</label>
<input type="number" id="sc-fps-en" value="20" min="1" max="60">
<span style="font-size:12px;color:#666;">Default 20fps / Presets based on 30fps</span>
</div>
</div>

<div class="sc-row">
<div class="sc-field">
<label>Daily Recording Hours</label>
<input type="number" id="sc-hours-en" value="24" min="1" max="24">
</div>
<div class="sc-field" id="sc-cap-field-en">
<label>Total Storage (TB)</label>
<input type="number" id="sc-cap-en" value="4" min="0.1" step="0.1">
</div>
<div class="sc-field" id="sc-days-field-en" style="display:none">
<label>Desired Retention (days)</label>
<input type="number" id="sc-days-en" value="30" min="1" max="3650">
</div>
</div>

<div class="sc-results" id="sc-results-en"></div>
<div class="sc-hdd" id="sc-hdd-en" style="display:none"></div>
</div>

<details class="sc-ref">
<summary>📋 Bitrate Reference Guide by Resolution</summary>
<table>
<tr><th>Resolution</th><th>Quality</th><th>Bitrate</th><th>Daily per Channel (30fps)</th></tr>
<tr><td>4K (8MP)</td><td>Ultra</td><td>25 Mbps</td><td>~270 GB</td></tr>
<tr><td>4K (8MP)</td><td>Standard</td><td>16 Mbps</td><td>~173 GB</td></tr>
<tr><td>1080p (2MP)</td><td>High</td><td>8 Mbps</td><td>~86 GB</td></tr>
<tr><td>1080p (2MP)</td><td>Standard</td><td>4 Mbps</td><td>~43 GB</td></tr>
<tr><td>720p (1MP)</td><td>Standard</td><td>2 Mbps</td><td>~22 GB</td></tr>
</table>
<p style="font-size:13px;color:#666;margin-top:8px;">※ Actual storage may vary depending on codec (H.264/H.265), scene complexity, and motion detection settings. H.265 can reduce storage by 30-50%.</p>
</details>
</div>

<script>
(function(){
var mode=0;
function $(id){return document.getElementById(id)}
function getBr(){
  var p=$('sc-preset-en');
  if(p.value==='custom')return parseFloat($('sc-br-custom-en').value)||4;
  return parseFloat(p.value);
}
function calc(){
  var ch=Math.max(1,Math.min(256,parseInt($('sc-ch-en').value)||1));
  var br=getBr();
  var hrs=Math.max(1,Math.min(24,parseInt($('sc-hours-en').value)||24));
  var fps=Math.max(1,Math.min(60,parseInt($('sc-fps-en').value)||20));
  var daily=br*(fps/30)*3600*hrs*ch/8/1000;
  var monthly=daily*30;
  var r=$('sc-results-en');
  var h=$('sc-hdd-en');
  if(mode===0){
    var cap=parseFloat($('sc-cap-en').value)||1;
    var days=cap*1000/daily;
    r.innerHTML=
      '<div class="sc-card"><div class="sc-lbl">Estimated Retention</div><div class="sc-val">'+days.toFixed(1)+' days</div><div class="sc-lbl">≈ '+(days/30).toFixed(1)+' months</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">Daily Data</div><div class="sc-val">'+daily.toFixed(1)+'</div><div class="sc-lbl">GB / day</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">Monthly Data</div><div class="sc-val">'+(monthly>=1000?(monthly/1000).toFixed(2)+' TB':monthly.toFixed(1)+' GB')+'</div><div class="sc-lbl">per 30 days</div></div>';
    h.style.display='none';
  }else{
    var d=Math.max(1,parseInt($('sc-days-en').value)||30);
    var need=daily*d/1000;
    r.innerHTML=
      '<div class="sc-card"><div class="sc-lbl">Required Storage</div><div class="sc-val">'+need.toFixed(2)+'</div><div class="sc-lbl">TB</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">Daily Data</div><div class="sc-val">'+daily.toFixed(1)+'</div><div class="sc-lbl">GB / day</div></div>'+
      '<div class="sc-card"><div class="sc-lbl">Total Data</div><div class="sc-val">'+(daily*d>=1000?(daily*d/1000).toFixed(2)+' TB':(daily*d).toFixed(1)+' GB')+'</div><div class="sc-lbl">for '+d+' days</div></div>';
    var hddSizes=[2,4,6,8,10,12,14,16,18,20];
    var rec='';
    for(var i=0;i<hddSizes.length;i++){
      var s=hddSizes[i];
      var cnt=Math.ceil(need/s);
      if(cnt<=8){rec+='💾 '+s+'TB HDD × '+cnt+' = '+(s*cnt)+'TB';if(cnt>1)rec+=' (RAID capable)';rec+='<br>';if(cnt<=2)break;}
    }
    if(!rec)rec='💾 Large-scale storage or NAS configuration required.';
    h.innerHTML='<strong>💡 Recommended HDD Configuration:</strong><br>'+rec;
    h.style.display='block';
  }
}
window.scModeEn=function(m){
  mode=m;
  var tabs=document.querySelectorAll('#sc-app-en .sc-tab');
  tabs[0].className='sc-tab'+(m===0?' active':'');
  tabs[1].className='sc-tab'+(m===1?' active':'');
  $('sc-cap-field-en').style.display=m===0?'':'none';
  $('sc-days-field-en').style.display=m===1?'':'none';
  calc();
};
window.scPresetEn=function(){
  var c=$('sc-br-custom-en');
  c.className='sc-custom-br'+($('sc-preset-en').value==='custom'?' show':'');
  calc();
};
var inputs=document.querySelectorAll('#sc-app-en input, #sc-app-en select');
for(var i=0;i<inputs.length;i++)inputs[i].addEventListener('input',calc);
calc();
})();
</script>

---

## Tips

- Using **H.265 (HEVC)** codec-supported NVRs can **reduce storage by 30-50%** at the same quality.
- **Motion detection recording** significantly reduces actual recording volume compared to continuous recording.
- Optimize costs by using **mixed configurations** — high quality for critical channels, lower quality for secondary ones.
- For reliable operation, it's recommended to have **10-20% extra capacity** beyond the calculated amount.

Have questions? [Contact us](/about/) for more information.
