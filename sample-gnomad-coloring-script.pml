color gray80
select likely_benign, resi 331+28+280+299
color lightblue, likely_benign
select likely_pathogenic, resi 281
color salmon, likely_pathogenic
select no_annotation, resi 238+257+240+241+250+252+239+242+235+237+200+202+206+207+216+219+220+225+226+229+231+232+233+234+260+262+308+311+316+317+318+320+321+325+330+143+146+148+149+305+300+263+197+271+272+273+275+278+283+290+291+294+296+303+187+195+23+30+32+45+52+58+59+68+75+77+81+82+84+92+103+22+18+14+4+10+13+5+107+7+8+11+12+6+111+112+113+160+164+165+169+170+171+177+179+180+184+186+157+194+158+156+114+116+120+123+125+130+133+135+136+138+127
color gray60, no_annotation
select pathogenic, resi 269
color firebrick, pathogenic
select uncertain_significance, resi 270+292+258+230+33+128+222+248+39+109+214+124+3+178
color paleyellow, uncertain_significance
show surface
set transparency, 0.2
bg_color white