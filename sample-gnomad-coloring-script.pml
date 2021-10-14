color gray80
select benign/likely_benign, resi 280
color nan, benign/likely_benign
select likely_benign, resi 28+299+331
color lightblue, likely_benign
select likely_pathogenic, resi 281
color salmon, likely_pathogenic
select no_annotation, resi 3+4+10+13+3+4+4+4+5+5+6+7+7+8+8+10+11+12+12+14+18+18+22+23+28+30+32+45+52+58+59+68+68+75+77+81+82+84+92+103+107+111+112+113+114+116+120+120+123+123+124+124+125+127+130+133+135+136+138+143+143+149+156+157+158+160+160+164+165+169+169+169+170+171+171+177+177+177+179+180+184+186+187+194+195+197+197+197+200+202+206+207+216+219+220+220+225+225+225+226+229+231+232+233+234+235+237+237+238+239+240+241+242+248+250+252+257+258+258+260+260+262+263+269+271+272+272+273+275+278+281+283+290+291+291+292+294+296+300+303+305+305+308+311+311+316+317+318+320+321+321+325+330+143+143+146+148+149+149+157+158
color gray60, no_annotation
select pathogenic, resi 269
color firebrick, pathogenic
select uncertain_significance, resi 3+33+39+109+124+128+178+214+222+230+248+258+270+292
color paleyellow, uncertain_significance
show surface
set transparency, 0.2
bg_color white