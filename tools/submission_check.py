#!/usr/bin/env python3
from pathlib import Path
import json,re,sys,yaml
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/"src/project.v").read_text()
info=yaml.safe_load((ROOT/"info.yaml").read_text())
cfg=json.loads((ROOT/"src/config.json").read_text())
errors=[]
def req(c,m):
    if not c: errors.append(m)
p=info["project"]; pin=info["pinout"]
req(p["top_module"]=="tt_um_forge01_forgecpu_tt1","wrong top module")
req(str(p["tiles"])=="1x1","tiles must be 1x1")
req(info["yaml_version"]==6,"yaml version must be 6")
req(p["clock_hz"]==10_000_000,"clock_hz must be 10MHz")
for g in ("ui","uo","uio"):
    for i in range(8): req(f"{g}[{i}]" in pin,f"missing pin {g}[{i}]")
req(cfg["CLOCK_PORT"]=="clk","CLOCK_PORT must be clk")
req(cfg["CLOCK_PERIOD"]==100,"CLOCK_PERIOD must be 100ns")
m=re.search(r"module\s+tt_um_forge01_forgecpu_tt1\s*\((.*?)\);",text,re.S)
req(m is not None,"top module missing")
if m:
    ports=[x.strip() for x in m.group(1).replace("\n"," ").split(",") if x.strip()]
    req(ports==["ui_in","uo_out","uio_in","uio_out","uio_oe","ena","clk","rst_n"],f"wrong ports: {ports}")
for pat,msg in [(r"assign uio_out = 0;","uio_out"),(r"assign uio_oe = 0;","uio_oe"),
                (r"mode == MODE_LOAD && ena == 1","ena load gate"),
                (r"mode == MODE_RUN && ena == 1","ena run gate")]:
    req(re.search(pat,text) is not None,msg)
for banned in [r"\binitial\b",r"\$display",r"\$finish",r"\$fatal",r"#[0-9]"]:
    req(re.search(banned,text) is None,f"non-synthesis construct {banned}")
if errors:
    print("FORGECPU-TT1 SUBMISSION CHECK FAIL")
    for e in errors: print(" -",e)
    sys.exit(1)
print("FORGECPU-TT1 SUBMISSION CHECK PASS")
