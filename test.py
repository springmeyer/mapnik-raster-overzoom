import mapnik

m = mapnik.Map(256,256)
mapnik.load_map(m,'map.xml')

boxes = [
 { 'name': '0/0/0', 'box': mapnik.Box2d(-20037508.342789244,-20037508.342789244,20037508.342789244,20037508.342789244) },
 { 'name': '1/0/0', 'box': mapnik.Box2d(-20037508.342789244,0,0,20037508.342789244) },
 { 'name': '2/0/1', 'box': mapnik.Box2d(-20037508.342789244,0,-10018754.171394622,10018754.17139462) },
 { 'name': '13/4062/2710 (charlbury)', 'box':mapnik.Box2d(-166326.9735485427,6775378.187198024,-161435.00373829156,6780270.157008275)}
]

for b in boxes:
    m.zoom_to_box(b['box'])
    im = mapnik.Image(256,256)
    mapnik.render(m,im)